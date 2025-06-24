#the purpose of this script is to derive the rmsd of the alphafold placement rmsd from native
#this will create csv files that note the closest placement to native for the closest of all placements, the closest of the top 10 by confidence, and the closeness of the most confident placement. These files will note the placement as well. A summary csv for the top rmsd will also be made for porting for figure making
#Since the placements are not aligned with the dude library (due to being made by alphafold), we need to align them. The ligand atom indices also do not match, so we will use a heuristic method from rdkit to get rmsd.

#import os,sys
import os,sys
import pymol2
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign
import numpy as np
from openbabel import openbabel as ob
from openbabel import pybel
import re
from rdkit.Chem import SanitizeFlags

#this script acts locally, and looks for placement files from alphafold and the native files from DUD-E
this_script_path = os.path.dirname(os.path.abspath(__file__))

#begin a pymol session
with pymol2.PyMOL() as pymol:
	cmd = pymol.cmd

	#write csv files for the different metrics and write a header line for the system, the placement file, confidence, and the rmsd
	best_all = open("best_placements_all.csv", "w")
	best_all.write("system,placement,confidence,rmsd\n")

	best_10 = open("best_placements_10.csv", "w")
	best_10.write("system,placement,confidence,rmsd\n")

	best_1 = open("best_placements_1.csv", "w")
	best_1.write("system,placement,confidence,rmsd\n")

	best_summary = open("best_placements_summary.csv", "w")
	best_summary.write("system,all,10,1\n")

	#iterate over each system in the dude library
	for r,d,f in os.walk(this_script_path + "/../../dude_library_simple"):
		for dire in d:
			print(dire)

			#temporary filter so we only test this on aa2ar until it is time to run on the full set
			#comment/delete when done testing!
			#if dire != "aa2ar":
			#	continue

			#open a file to write pairings of the files with confidence values and rmsd
			#open it in the respective folder in the alphafold section of the repository
			system_file = open("../../alphafold3/" + dire + "/" + dire + "_placements_summary.csv", "w")
			system_file.write("file,confidence,rmsd\n")

			#declare placeholder variables to hold the best placements for each group
			blank_list = ["X","X","X"]
			best_rmsd_all = ["X","X","X"]
			best_rmsd_10 = ["X","X","X"]
			best_rmsd_1 = ["X","X","X"]
			
			#get the original placement from the dude library and open it in pymol, the file we want is the "name"_orig.pdb
			cmd.load(r + "/" + dire + "/" + dire + "_orig.pdb", "reference")

			#create a dictionary the holds the placement files and the corresponding confidence and rmsd values
			#the file is the key and the value is a 2 entry list of confidence then rmsd
			placements_data = {}

			#create another dictionary for the placement confidence values for accession
			#the key is a 2 value list for the seed (1-10) and sample (0-4), and the value is the corresponding confidence
			#this will be used for deriving the confidence values for given placements after iterating over all files
			confidences = {}

			#now, iterate over the placements
			for r2,d2,f2 in os.walk(this_script_path + "/../../alphafold3"):
				for file in f2:
					#if it is the confidence file
					if file == (dire + "_ranking_scores.csv"):
						#read the file
						confidences_file = open(r2 + "/" + dire + "_ranking_scores.csv", "r")

						for line in confidences_file:
							#skip the header
							if "seed,sample" in line:
								continue
							#get the values line by line
							seed = line.split(",")[0]
							sample = line.split(",")[1]
							conf = line.split(",")[2].strip()
							#assign
							confidences[(seed,sample)] = conf

					#if it is a placement file for the system
					if file.startswith(dire + "_") and file.endswith("_model.cif") and "seed" in file and "sample" in file:
						#load it into pymol
						cmd.load(r2 + "/" + file, "placement")

						#align the placement to the reference
						cmd.align("placement", "reference")

						#select the ligand one aligned and save it as a pdb
						cmd.select("aligned_lig", "placement and not polymer.protein")

						#derive a name to save the aligned ligand as
						file_basename = file.split(".")[0]

						cmd.save(r2 + "/" + file_basename + "_aligned_lig.pdb", "aligned_lig")

						#clear the aligned ligand and the placement from the session, but keep the reference
						cmd.delete("aligned_lig")
						cmd.delete("placement")

						#next, work on getting the rmsd
						#remove hydrogens

						#write new ligand pdb to mol2 for easier readability
						#mol = next(pybel.readfile("pdb", r + "/" + dire + "/" + dire + "-lig.pdb"))
						#mol.addh()  
						#mol.write("mol2", r + "/" + dire + "/" + dire + "-lig.mol2", overwrite=True)
						#mol = next(pybel.readfile("pdb", r + "/" + dire + "/" + dire + "-lig.pdb"))
						#mol.addh()  
						#mol.write("pdb", r + "/" + dire + "/" + dire + "-lig_fixed.pdb", overwrite=True)

						#os.system("cat " + r + "/" + dire + "/" + dire + "-lig.mol2")

						#make a fixed version of the reference from the original so that the element is regognized
						old_reference_file = open(r + "/" + dire + "/" + dire + "-lig.pdb", "r")
						fixed_reference_file = open(r + "/" + dire + "/" + dire + "-lig_fixed.pdb", "w")

						for line in old_reference_file.readlines():
							#remove waters
							if " HOH " in line:
								continue

							if line.startswith(('ATOM', 'HETATM')):
								atom_name = line[12:16]

								#derive element
								element = re.match(r"[A-Za-z]+", atom_name.strip()).group(0).capitalize()
								#print(element)

								#skip hydrogens
								if element == "H":
									continue

								stripped_line = line.rstrip("\n")

								fixed_line = stripped_line[:76].ljust(76) + element.rjust(2) 
								#fixed_line = stripped_line[:76].ljust(76) + element.rjust(2) + stripped_line[78:]

								fixed_reference_file.write(fixed_line + "\n")

						#close streams
						old_reference_file.close()
						fixed_reference_file.close()




						#reference_ligand = Chem.MolFromPDBFile(r + "/" + dire + "/" + dire + "-lig.pdb", removeHs=True)
						reference_ligand = Chem.MolFromPDBFile(r + "/" + dire + "/" + dire + "-lig_fixed.pdb", removeHs=True, sanitize=False)
						#reference_ligand = Chem.MolFromMol2File(r + "/" + dire + "/" + dire + "-lig.mol2", removeHs=True)
						#reference_ligand = Chem.MolFromMol2File(r + "/" + dire + "/crystal_ligand.mol2", removeHs=True)
						

						#sanitize the reference in case there are waters in it
						#frags = Chem.GetMolFrags(reference_ligand, asMols=True)
						#ligand = max(frags, key=lambda m: m.GetNumAtoms())
						#reference_ligand = ligand


						placement_ligand = Chem.MolFromPDBFile(r2 + "/" + file_basename + "_aligned_lig.pdb", removeHs=True, sanitize=False)

						try:
							Chem.SanitizeMol(mol, sanitizeOps=SanitizeFlags.SANITIZE_ALL ^ SanitizeFlags.SANITIZE_PROPERTIES)
						except Exception as e:
							print("Sanitization failed:", e)

						ref_smiles = Chem.MolToSmiles(reference_ligand)
						pla_smiles = Chem.MolToSmiles(placement_ligand)

						print("reference",ref_smiles,"placement",pla_smiles)

						rmsd = "X"

						#use the get best RMS function to derive the rmsd
						if reference_ligand and placement_ligand:
							try:
								rmsd = rdMolAlign.GetBestRMS(reference_ligand, placement_ligand)
								print(r2 + "/" + file_basename + "_aligned_lig.pdb", rmsd)
							except RuntimeError as e:
								print("Alignment failed:", e)


						#if the rmsd is X, don't add it
						if str(rmsd) == "X":
							continue

						#store the rmsd in the dictionary by the file name
						placements_data[file] = ["X",rmsd]

						#we are now done with the placement, and can move to the next

			#done with all placements for the system, correlate rmsd and confidence and update dictionaries and finish the system-specific csv

			#make a list that we can sort by confidence so we can derive the top rmsd from the single best, top 10, and all, and we will use it to write
			#format is file,confidence,rmsd
			placements_list = []

			for system in placements_data.keys():
				#remember, the keys are file names, so we can derive the placement seed and sample

				#now, derive the seed and sample of the file, so we can note and write it and correlate to confidence
				placement_seed = system.split("-")[1].split("_")[0]
				placement_sample = system.split("-")[2].split("_")[0]

				#obtain the corresponding confidence from the dictionary
				system_confidence = confidences[(placement_seed,placement_sample)]

				#add the confidence to the placements_data dictionary
				placements_data[system][0] = float(system_confidence)

				placements_list.append([system,float(system_confidence),float(placements_data[system][1])])

			#now, sort placements_list by confidence score in descending order
			sorted_list = sorted(placements_list, key=lambda x: x[1], reverse=True)

			#iterate down the sorted list to derive the best values and write the the system file

			#have a counter for the number of systems seen so we can cut off looking for the top 1 and top 10
			counter = 1

			for system in sorted_list:

				#for top 1
				if counter == 1:
					best_rmsd_1 = system

				#for top 10
				if counter <= 10:
					#if first encounter, a blank list, write current
					if best_rmsd_10 == blank_list:
						best_rmsd_10 = system
					else:
						#otherwise, see if the rmsd is better and overwrite
						if best_rmsd_10[2] > system[2]:
							best_rmsd_10 = system

				#for all
				if best_rmsd_all == blank_list:
					best_rmsd_all = system

				if best_rmsd_all[2] > system[2]:
					best_rmsd_all = system

				#write the system to the system file
				system_file.write(system[0] + "," + str(system[1]) + "," + str(system[2]) + "\n")

				counter = counter + 1

			#now that we have iterated over all systems, write the best of each category to the other csv files
			best_all.write(dire + "," + best_rmsd_all[0] + "," + str(best_rmsd_all[1]) + "," + str(best_rmsd_all[2]) + "\n")
			best_10.write(dire + "," + best_rmsd_10[0] + "," + str(best_rmsd_10[1]) + "," + str(best_rmsd_10[2]) + "\n")
			best_1.write(dire + "," + best_rmsd_1[0] + "," + str(best_rmsd_1[1]) + "," + str(best_rmsd_1[2]) + "\n")

			best_summary.write(dire + "," + str(best_rmsd_all[2]) + "," + str(best_rmsd_10[2]) + "," + str(best_rmsd_1[2]) + "\n")

			#clear the reference from the pymol session:
			cmd.delete("reference")