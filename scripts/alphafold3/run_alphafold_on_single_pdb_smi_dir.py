#!/usr/bin/env python3
"""
Create AlphaFold3 input JSON files and runnable shell scripts for one protein PDB
against every .smi ligand file in a directory.

Example:
    python run_alphafold_on_single_pdb_smi_dir.py receptor.pdb /path/to/smi_dir \
        --output_dir /path/to/alphafold3/receptor_screen

Optionally submit each generated shell script to LSF:
    python run_alphafold_on_single_pdb_smi_dir.py receptor.pdb /path/to/smi_dir --submit
"""

import argparse
import json
import os
import re
import shlex
import subprocess
from pathlib import Path


THREE_TO_ONE = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    # Common PDB variants / protonation states
    "MSE": "M", "SEC": "U", "PYL": "O", "HID": "H", "HIE": "H", "HIP": "H",
    "CYX": "C", "CYM": "C", "ASH": "D", "GLH": "E", "LYN": "K",
}


def safe_name(name: str) -> str:
    """Make a conservative filename/job-name-safe string."""
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_")


def read_smiles_file(smi_path: Path) -> str:
    """Return the first SMILES token from the first non-empty, non-comment line."""
    with smi_path.open() as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            return line.split()[0]
    raise ValueError(f"No SMILES string found in {smi_path}")


def pdb_sequences(pdb_path: Path):
    """
    Extract protein sequences from ATOM records in a PDB file.

    Returns a list of {id: [chain_id], sequence: sequence} dictionaries in the
    format AlphaFold3 expects for protein entries. Duplicate atom records for the
    same residue are collapsed using chain/residue number/insertion code.
    """
    chain_order = []
    residues_by_chain = {}
    seen_residues = set()

    with pdb_path.open(errors="replace") as handle:
        for line in handle:
            if not line.startswith("ATOM"):
                continue

            resname = line[17:20].strip().upper()
            if resname not in THREE_TO_ONE:
                continue

            raw_chain = line[21].strip()
            chain = raw_chain if raw_chain else "_blank_"
            resseq = line[22:26].strip()
            icode = line[26].strip()
            resid_key = (chain, resseq, icode)

            if resid_key in seen_residues:
                continue
            seen_residues.add(resid_key)

            if chain not in residues_by_chain:
                residues_by_chain[chain] = []
                chain_order.append(chain)
            residues_by_chain[chain].append(THREE_TO_ONE[resname])

    if not chain_order:
        raise ValueError(f"No protein ATOM records with recognized residues found in {pdb_path}")

    # AF3 chain IDs should be simple labels. Preserve normal one-character chain IDs
    # when possible; otherwise assign A, B, C, ... in file order.
    fallback_ids = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    protein_entries = []
    used_ids = set()

    for idx, chain in enumerate(chain_order):
        if len(chain) == 1 and chain.isalnum() and chain not in used_ids:
            af3_chain_id = chain
        else:
            af3_chain_id = fallback_ids[idx] if idx < len(fallback_ids) else f"P{idx + 1}"
            while af3_chain_id in used_ids:
                idx += 1
                af3_chain_id = fallback_ids[idx] if idx < len(fallback_ids) else f"P{idx + 1}"

        used_ids.add(af3_chain_id)
        protein_entries.append({
            "protein": {
                "id": [af3_chain_id],
                "sequence": "".join(residues_by_chain[chain]),
            }
        })

    return protein_entries


def make_af3_json(job_name: str, protein_entries, smiles: str, seeds):
    return {
        "name": job_name,
        "dialect": "alphafold3",
        "version": 3,
        "modelSeeds": seeds,
        "sequences": protein_entries + [
            {
                "ligand": {
                    "id": "L",
                    "smiles": smiles,
                }
            }
        ],
    }


def write_shell_script(
    shell_path: Path,
    json_name: str,
    af_input_dir: Path,
    af_output_dir: Path,
    af3_resources_dir: str,
    af3_image_name: str,
    run_inference: bool,
):
    run_inference_string = "TRUE" if run_inference else "FALSE"
    text = f"""#!/usr/bin/env bash
set -euo pipefail

module load apptainer

export AF3_RESOURCES_DIR={shlex.quote(af3_resources_dir)}
export AF3_IMAGE=${{AF3_RESOURCES_DIR}}/{shlex.quote(af3_image_name)}
export AF3_CODE_DIR=${{AF3_RESOURCES_DIR}}/code
export AF3_INPUT_DIR={shlex.quote(str(af_input_dir.resolve()))}
export AF3_OUTPUT_DIR={shlex.quote(str(af_output_dir.resolve()))}
export AF3_MODEL_PARAMETERS_DIR=${{AF3_RESOURCES_DIR}}/params
export AF3_DATABASES_DIR=${{AF3_RESOURCES_DIR}}/db

apptainer exec \\
     --nv \\
     --env XLA_PYTHON_CLIENT_PREALLOCATE=false,TF_FORCE_UNIFIED_MEMORY=true,XLA_CLIENT_MEM_FRACTION=3.2 \\
     --bind $AF3_INPUT_DIR:/root/af_input \\
     --bind $AF3_OUTPUT_DIR:/root/af_output \\
     --bind $AF3_MODEL_PARAMETERS_DIR:/root/models \\
     --bind $AF3_DATABASES_DIR:/root/public_databases \\
     $AF3_IMAGE \\
     python ${{AF3_CODE_DIR}}/alphafold3/run_alphafold.py --run_inference={run_inference_string} --flash_attention_implementation=xla \\
     --json_path=/root/af_input/{shlex.quote(json_name)} \\
     --model_dir=/root/models \\
     --db_dir=/root/public_databases \\
     --output_dir=/root/af_output
"""
    shell_path.write_text(text)
    shell_path.chmod(0o755)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build AlphaFold3 JSON/shell inputs for one PDB and a directory of .smi ligands."
    )
    parser.add_argument("pdb_file", help="Single protein PDB file to use for all ligand placements.")
    parser.add_argument("smi_dir", help="Directory containing ligand .smi files. Each file should contain one SMILES string.")
    parser.add_argument(
        "--output_dir",
        default=None,
        help="Output directory. Default: ./alphafold3_<pdb_stem>",
    )
    parser.add_argument(
        "--seeds",
        default="1,2,3,4,5,6,7,8,9,10",
        help="Comma-separated AF3 model seeds. Default: 1,2,3,4,5,6,7,8,9,10",
    )
    parser.add_argument(
        "--run_inference",
        action="store_true",
        help="Run full AF3 inference. By default scripts use --run_inference=FALSE, matching the original prep-only script.",
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Submit each generated shell script to LSF with bsub after writing it.",
    )
    parser.add_argument("--queue", default="gpu", help="LSF queue for --submit. Default: gpu")
    parser.add_argument("--cores", default="8", help="LSF core count for --submit. Default: 8")
    parser.add_argument("--memory", default="2048", help="LSF rusage[mem=...] value. Default: 2048")
    parser.add_argument("--walltime", default="300", help="LSF -W walltime value. Default: 300")
    parser.add_argument(
        "--gpu_string",
        default="num=1:gmodel=TeslaV100_SXM2_32GB-30G:mode=shared:j_exclusive=no",
        help="LSF -gpu resource string.",
    )
    parser.add_argument(
        "--af3_resources_dir",
        default="/pi/summer.thyme-umw/alphafold3",
        help="Directory containing AF3 image, code, params, and db directories.",
    )
    parser.add_argument(
        "--af3_image_name",
        default="alphafold3_cuda7.sif",
        help="AF3 Apptainer image filename inside --af3_resources_dir.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    pdb_file = Path(args.pdb_file).expanduser().resolve()
    smi_dir = Path(args.smi_dir).expanduser().resolve()

    if not pdb_file.is_file():
        raise FileNotFoundError(f"PDB file not found: {pdb_file}")
    if not smi_dir.is_dir():
        raise NotADirectoryError(f"SMILES directory not found: {smi_dir}")

    smi_files = sorted(smi_dir.glob("*.smi"))
    if not smi_files:
        raise FileNotFoundError(f"No .smi files found in {smi_dir}")

    seeds = [int(x.strip()) for x in args.seeds.split(",") if x.strip()]
    protein_entries = pdb_sequences(pdb_file)

    pdb_stem = safe_name(pdb_file.stem)
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else Path.cwd() / f"alphafold3_{pdb_stem}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Protein: {pdb_file}")
    print(f"Protein chains found: {len(protein_entries)}")
    print(f"Ligands found: {len(smi_files)}")
    print(f"Output: {output_dir}")

    for smi_file in smi_files:
        ligand_name = safe_name(smi_file.stem)
        job_name = safe_name(f"{pdb_stem}_{ligand_name}")
        ligand_run_dir = output_dir / ligand_name
        af_input_dir = ligand_run_dir / "af_input"
        af_output_dir = ligand_run_dir / "af_output"
        af_input_dir.mkdir(parents=True, exist_ok=True)
        af_output_dir.mkdir(parents=True, exist_ok=True)

        smiles = read_smiles_file(smi_file)
        json_data = make_af3_json(job_name, protein_entries, smiles, seeds)
        json_path = af_input_dir / f"{job_name}.json"
        json_path.write_text(json.dumps(json_data, indent=2) + "\n")

        shell_path = ligand_run_dir / f"{job_name}.sh"
        write_shell_script(
            shell_path=shell_path,
            json_name=json_path.name,
            af_input_dir=af_input_dir,
            af_output_dir=af_output_dir,
            af3_resources_dir=args.af3_resources_dir,
            af3_image_name=args.af3_image_name,
            run_inference=args.run_inference,
        )

        print(f"Wrote {json_path}")
        print(f"Wrote {shell_path}")

        if args.submit:
            log_path = ligand_run_dir / f"{job_name}_log.txt"
            bsub_cmd = [
                "bsub",
                "-n", str(args.cores),
                "-R", f"rusage[mem={args.memory}]",
                "-W", str(args.walltime),
                "-gpu", args.gpu_string,
                "-q", args.queue,
                "-o", str(log_path),
                "bash", str(shell_path),
            ]
            subprocess.run(bsub_cmd, check=True)


if __name__ == "__main__":
    main()
