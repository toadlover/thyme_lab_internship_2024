#the purpose of this script is to run a build of alphafold3 on all systems in out copy of the dude library
#This script uses the scripts get_smiles_of_ligand_file.py and get_residue_sequences_from_pdb_file.py in the ginsparg_thymelab_thesis repository in order to have our ligands be in SMILES format and derive a residue sequence of all chains of the proteins
#This script uses the Slurm job scheduler to run individual jobs for alphafold for each system. If using a different scheduler, the job writing logic will need to be changed

#Instructions to build the alphafold build that was used for this:
#singularity pull alphafold3.sif docker://gitlab.rc.uab.edu:4567/rc-data-science/community-containers/alphafold3/alphafold3:f0bc27f5

#import os and sys
import os,sys

#argument for path to ginsparg_thymelab_thesis repository
repo_location = sys.argv[1]

#iterate over each dude system to runalphafold
#iterate over each system folder in thyme_lab_internship_2024/dude_library_simple
for r,d,f in os.walk(os.path.dirname(os.path.abspath(__file__)) + "/../../dude_library_simple/"):
	for dire in d:
		#only look at directories at the level within dude_library_simple
		if r == os.path.dirname(os.path.abspath(__file__)) + "/../../dude_library_simple/":
			print(dire)