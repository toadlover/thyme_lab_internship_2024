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

			#hold the path for the smiles file so we can access later
			ligand_smile_location = this_script_path + "/../../dude_library_simple/" + dire + "/" + dire + ".smi"

			#now, derive the residue chain(s) for the system and write it to a file
			os.system("python " + repo_location + "misc/alphafold_prep/get_residue_sequences_from_pdb_file.py " + this_script_path + "/../../dude_library_simple/" + dire + "/" + dire + ".pdb " + this_script_path + "/../../dude_library_simple/" + dire + "/" + dire + "_residue_sequences.csv")

			#hold the path for the residue sequences file so we can access later
			residue_sequence_file_location = this_script_path + "/../../dude_library_simple/" + dire + "/" + dire + "_residue_sequences.csv"

			#make folder in alphafold section of repo to runalphafold for the system
			os.system("mkdir " + this_script_path + "/../../alphafold3/" + dire)

			#now, create the json file to run alphafold
			json_file = open(this_script_path + "/../../alphafold3/" + dire + "/" + dire + ".json", "w")

			#open the smiles and residue sequence files to get that dat afor the json file as well
			smiles_file = open(ligand_smile_location, "r")
			residue_file = open(residue_sequence_file_location, "r")

			#extract the smiles and residue sequence(s) so that we can write them into the json file
			#extract smiles, file should only be a single line, so extraction is easy
			lig_smiles = ""
			for line in smiles_file.readlines():
				lig_smiles = line.strip()

			#extract residue sequence(s), store as a list in case there is more than one sequence, and we will iteratively add each sequence to the json file
			#store as tuple of chain id in index 0 and the chain sequence in index 1
			residue_sequences = []
			for line in residue_file.readlines():
				#each line is comma separated with the chain id in index 0 and the sequnce in index 1 (I think for the whole DUDE set, everything is just 1 chain that is a space, but other pdbs may have letter chain ids; this does mess up if the chain was named ',', but you probably shouldn't be naming a chain that anyway)
				cur_sequence = line.split(",")[1].strip()

				cur_chain = line.split(",")[0]

				residue_sequences.append([cur_chain,cur_sequence])

			#write the json file

			#startign bracket
			json_file.write("{\n")
			#job name
			json_file.write("\t\"name\": \"" + dire + "\",\n")
			#model seeds, we want to give each system 10 attempts, so we will give all seeds 1-10
			json_file.write("\t\"modelSeeds\": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],\n")
			#protein and ligand data
			json_file.write("\t\"sequences\": [\n")
			#iterate over each chain
			for chain in residue_sequences:
				#declare beginning of protein
				json_file.write("\t\t{\n")
				json_file.write("\t\t\t\"protein\": {\n")
				#declare chain id
				json_file.write("\t\t\t\t\"id\": \"" + chain[0] + "\",\n")
				json_file.write("\t\t\t\t\"sequence\": \"" + chain[1] + "\",\n")
				#end declaration, at least for now will not use unpaired/paired msa or templates
				json_file.write("\t\t\t}n")
				json_file.write("\t\t}n")

			#declare the ligand
			json_file.write("\t\t{\n")
			json_file.write("\t\t\t\"ligand\": {\n")
			#write id, name after system
			json_file.write("\t\t\t\t\"id\": \"" + dire + "\",\n")
			#declare smiles string
			json_file.write("\t\t\t\t\"smiles\": \"" + lig_smiles + "\",\n")
			#end declaration
			json_file.write("\t\t\t}\n")
			json_file.write("\t\t}\n")

			#skipping bondedatompairs and userccd at least for now

			#write dialect and version
			json_file.write("\t\"dialect\": \"alphafold3\",\n")
			json_file.write("\t\"version\": 2\n")
			#close statement
			json_file.write("}\n")

