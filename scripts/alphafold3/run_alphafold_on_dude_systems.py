#the purpose of this script is to run a build of alphafold3 on all systems in out copy of the dude library
#This script uses the scripts get_smiles_of_ligand_file.py and get_residue_sequences_from_pdb_file.py in the ginsparg_thymelab_thesis repository in order to have our ligands be in SMILES format and derive a residue sequence of all chains of the proteins
#This script uses the Slurm job scheduler to run individual jobs for alphafold for each system. If using a different scheduler, the job writing logic will need to be changed

#Instructions to build the alphafold build that was used for this:
#singularity pull alphafold3.sif docker://gitlab.rc.uab.edu:4567/rc-data-science/community-containers/alphafold3/alphafold3:f0bc27f5

#import os and sys
import os,sys

#argument for path to ginsparg_thymelab_thesis repository
#provide the location of the top of the ginsparg_thymelab_thesis directory (trailing slash optional, will be appended if not included)
repo_location = sys.argv[1]
if repo_location.endswith("/ginsparg_thymelab_thesis") == False and repo_location.endswith("/ginsparg_thymelab_thesis/") == False:
	print("You need to provide the location of a copy of ginsparg_thymelab_thesis, please provide the location up to the top of the repository.")
	quit()

#add trailing slash if missing
if repo_location.endswith("/") == False:
	repo_location = repo_location + "/"

#record this script path for referencing it and other files by relative location
this_script_path = os.path.dirname(os.path.abspath(__file__))

#iterate over each dude system to runalphafold
#iterate over each system folder in thyme_lab_internship_2024/dude_library_simple
for r,d,f in os.walk(this_script_path + "/../../dude_library_simple/"):
	for dire in d:
		#only look at directories at the level within dude_library_simple
		if r == this_script_path + "/../../dude_library_simple/":
			print(dire)

			#derive the smiles string of the ligand and get the residue sequence(s) of the peptide
			#derive smiles string first
			#write the smiles string to the location where the ligand came from, and name it after the folder (instead of crystal_ligand)
			os.system("python " + repo_location + "misc/alphafold_prep/get_smiles_of_ligand_file.py " + this_script_path + "/../../dude_library_simple/" + dire + "/crystal_ligand.mol2 " + this_script_path + "/../../dude_library_simple/" + dire + " " + dire)