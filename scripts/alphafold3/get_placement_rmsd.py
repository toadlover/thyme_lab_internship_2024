#the purpose of this script is to derive the rmsd of the alphafold placement rmsd from native
#this will create csv files that note the closest placement to native for the closest of all placements, the closest of the top 10 by confidence, and the closeness of the most confident placement. These files will note the placement as well. A summary csv for the top rmsd will also be made for porting for figure making
#Since the placements are not aligned with the dude library (due to being made by alphafold), we need to align them. The ligand atom indices also do not match, so we will use a heuristic method from rdkit to get rmsd.

#import os,sys
import os,sys
import pymol2
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign
import numpy as np

#this script acts locally, and looks for placement files from alphafold and the native files from DUD-E
this_script_path = os.path.dirname(os.path.abspath(__file__))

#begin a pymol session
with pymol2.PyMOL() as pymol:
	cmd = pymol.cmd

	#write csv files for the different metrics and write a header line for the system, the placement file, and the rmsd
	best_all = open("best_placements_all.csv", "w")
	best_all.write("system,placement,rmsd\n")

	best_10 = open("best_placements_10.csv", "w")
	best_10.write("system,placement,rmsd\n")

	best_10 = open("best_placements_10.csv", "w")
	best_10.write("system,placement,rmsd\n")

	best_summary = open("best_placements_summary.csv", "w")
	best_all.write("system,all,10,1\n")

	#iterate over each system in the dude library
	for r,d,f in os.walk(this_script_path + "/../../dude_library_simple"):
		for dire in d:
			print(dire)

			#temporary filter so we only test this on aa2ar until it is time to run on the full set
			#comment/delete when done testing!
			if dire != "aa2ar":
				continue

			#open a file to write pairings of the files with confidence values and rmsd
			#open it in the respective folder in the alphafold section of the repository
			system_file = open("../../alphafold3/" + dire + "/" + dire + "_placements_summary.csv", "w")
			system_file.write("file,confidence,rmsd\n")

			#declare placeholder variables to hold the best placements for each group
			best_rmsd_all = "X"
			best_rmsd_10 = "X"
			best_rmsd_1 = "X"
			
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
					if file.startswith(dire + "_") and file.endswith("_model.cif"):
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

						#next work on getting the rmsd
