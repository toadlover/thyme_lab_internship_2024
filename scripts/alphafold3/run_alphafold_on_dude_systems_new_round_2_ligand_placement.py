#the purpose of this script is to run a build of alphafold3 on all systems in out copy of the dude library
#This script uses the scripts get_smiles_of_ligand_file.py and get_residue_sequences_from_pdb_file.py in the ginsparg_thymelab_thesis repository in order to have our ligands be in SMILES format and derive a residue sequence of all chains of the proteins

############Pick up with this on Monday and update the script to write and submit jobs that use the created json files and add the ligand smiles strings for placements

#Credit to Dr. Ji Cheng for helping with writing the general protocol and assembling the alphafold image

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

			#make folders called af_input and af_output for inputs and outputs
			os.system("mkdir " + this_script_path + "/../../alphafold3/" + dire + "/af_input")
			os.system("mkdir " + this_script_path + "/../../alphafold3/" + dire + "/af_output")

			#open the previously made data file, which should exist in the af_output location
			#this will be used as a template to write most of the new input file, and we just need to insert the ligand smiles data for a rerun

			#check and make sure the file exists, since there were a handful of cases where alphafold died from a segfault
			if not os.path.exists(this_script_path + "/../../alphafold3/" + dire + "/af_output/" + dire + "/" + dire +  "_data.json"):
				print(this_script_path + "/../../alphafold3/" + dire + "/af_output/" + dire + "/" + dire +  "_data.json does not exist! Moving to next file.")
				continue

			msa_json_file = open(this_script_path + "/../../alphafold3/" + dire + "/af_output/" + dire + "/" + dire +  "_data.json", "r")

			#now, create the json data file that has the msa data from an initial run of alphafold, and we include the corresponding smiles data
			json_file = open(this_script_path + "/../../alphafold3/" + dire + "/af_input/" + dire + "_data.json", "w")

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

			#tracker to see if we have written the ligand data, so we only write it ones
			#bool to hijack the write stream so that after we write the sequences line, we write the open curly bracket and then write the ligand data before we write the protein data (since order should not matter)
			hit_sequence_declaration = False

			for line in msa_json_file.readlines():
				#write the line to the new json file
				json_file.write(line)

				#check if "sequences": is in the line, since we will want to hijack here to insert the ligand lines
				if "\"sequences\":" in line and "[" in line:
					hit_sequence_declaration = True

					#new open bracket
					#json_file.write("\t{\n")

					#write the ligand data
					json_file.write("\t\t{\n")
					json_file.write("\t\t\"ligand\": {\n")
					json_file.write("\t\t\t\"id\": \"B\",\n")
					json_file.write("\t\t\t\"smiles\": \"" + lig_smiles + "\"\n")
					json_file.write("\t\t\t}\n")
					json_file.write("\t\t},\n")


				#case to get things back on track after the sequence, if the hits_sequence_declaration is true and we hit the {, continue, since we are in the sequences block now and do not want the dangling bracket
				if "{" in line and hit_sequence_declaration == True:
					hit_sequence_declaration = False
					continue



			#startign bracket
			#json_file.write("{\n")
			#job name
			#json_file.write("\t\"name\": \"" + dire + "\",\n")
			#write dialect and version
			#json_file.write("\t\"dialect\": \"alphafold3\",\n")
			#json_file.write("\t\"version\": 3,\n")
			#model seeds, we want to give each system 10 attempts, so we will give all seeds 1-10
			#json_file.write("\t\"modelSeeds\": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],\n")
			#protein and ligand data
			#json_file.write("\t\"sequences\": [\n")
			#iterate over each chain
			#for chain in residue_sequences:
				#declare beginning of protein
			#	json_file.write("\t\t{\n")
			#	json_file.write("\t\t\t\"protein\": {\n")
				#declare chain id

			#	json_file.write("\t\t\t\t\"id\": [\"A\"],\n")
			#	json_file.write("\t\t\t\t\"sequence\": \"" + chain[1] + "\"\n")
				#end declaration, at least for now will not use unpaired/paired msa or templates
			#	json_file.write("\t\t\t}\n")
			#	json_file.write("\t\t}\n")


			#ligand
			#json_file.write("\t\t{\n")
			#json_file.write("\t\t\t\"ligand\": {\n")
			#write id, name after system
			#json_file.write("\t\t\t\t\"id\": \"L\",\n")
			#declare smiles string
			#json_file.write("\t\t\t\t\"smiles\": \"" + lig_smiles + "\"\n")
			#json_file.write("\t\t\t}\n")
			#end declaration
			#json_file.write("\t\t}\n")
			#json_file.write("\t]\n")


			#skipping bondedatompairs and userccd at least for now


			#close statement
			#json_file.write("}\n")
			json_file.close()
			msa_json_file.close()

			#now write the corresponding shell script
			shell_file = open(this_script_path + "/../../alphafold3/" + dire + "/" + dire + "_docking.sh", "w")

			#for now at least, I'm just going to hard code the path variables, since I'm not sure if this will really be reused

			shell_file.write("module load apptainer\n")
			shell_file.write("export AF3_RESOURCES_DIR=/pi/summer.thyme-umw/alphafold3\n")
			shell_file.write("export AF3_IMAGE=${AF3_RESOURCES_DIR}/alphafold3_cuda7.sif\n")
			shell_file.write("export AF3_CODE_DIR=${AF3_RESOURCES_DIR}/code\n")
			shell_file.write("export AF3_INPUT_DIR=/pi/summer.thyme-umw/2024_intern_lab_space/thyme_lab_internship_2024/alphafold3/" + dire + "/af_input\n")
			shell_file.write("export AF3_OUTPUT_DIR=/pi/summer.thyme-umw/2024_intern_lab_space/thyme_lab_internship_2024/alphafold3/" + dire + "/af_output\n")
			shell_file.write("export AF3_MODEL_PARAMETERS_DIR=${AF3_RESOURCES_DIR}/params\n")
			shell_file.write("export AF3_DATABASES_DIR=${AF3_RESOURCES_DIR}/db\n")
			shell_file.write("\n")
			shell_file.write("apptainer exec \\\n")
			shell_file.write("     --nv \\\n")
			shell_file.write("     --env XLA_PYTHON_CLIENT_PREALLOCATE=false,TF_FORCE_UNIFIED_MEMORY=true,XLA_CLIENT_MEM_FRACTION=3.2 \\\n")
			shell_file.write("     --bind $AF3_INPUT_DIR:/root/af_input \\\n")
			shell_file.write("     --bind $AF3_OUTPUT_DIR:/root/af_output \\\n")
			shell_file.write("     --bind $AF3_MODEL_PARAMETERS_DIR:/root/models \\\n")
			shell_file.write("     --bind $AF3_DATABASES_DIR:/root/public_databases \\\n")
			shell_file.write("     $AF3_IMAGE \\\n")
			#use run data pipeline instead of inference
			shell_file.write("     python ${AF3_CODE_DIR}/alphafold3/run_alphafold.py --run_data_pipeline=FALSE --flash_attention_implementation=xla \\\n")
			shell_file.write("     --json_path=/root/af_input/" + dire + "_data.json" + " \\\n")
			shell_file.write("     --model_dir=/root/models \\\n")
			shell_file.write("     --db_dir=/root/public_databases \\\n")
			shell_file.write("     --output_dir=/root/af_output\\\n")
			shell_file.write("\n")
			shell_file.write("\n")
			shell_file.write("\n")
			shell_file.write("\n")
			shell_file.write("\n")
			shell_file.write("\n")
			shell_file.write("\n")
			shell_file.write("\n")

			shell_file.close()

			#chmod the shell file so it can be executed
			os.system("chmod 777 " + this_script_path + "/../../alphafold3/" + dire + "/" + dire + "_docking.sh")

			#run a bsub job with the shell file
			os.system("bsub -n 8 -R \"rusage[mem=2048]\" -W 300 -gpu \"num=1:gmodel=TeslaV100_SXM2_32GB-30G:mode=shared:j_exclusive=no\" -q gpu  -o " + this_script_path + "/../../alphafold3/" + dire + "/" + dire + "_docking_log.txt bash " + this_script_path + "/../../alphafold3/" + dire + "/" + dire + "_docking.sh")