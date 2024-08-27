#this script reads through the rmsd out files txt files for individual systems and determines the best rmsd for system out of the top x (passed by command line argument) placements by ddg

#run as (number at end can be changed): python rosetta_top_x_rmsd_by_ddg.py 10
#run this script within thyme_lab_internship_2024/scripts/rmsd to get the paths correct

#this script will create a file named rmsd_total_best_X.csv where X is the inputted value

import os,sys

#read in the argument for the top x placements
top_x = int(sys.argv[1])

#dictionary to hold the list of the top x ddg placement rmsds
best_rmsds_dict = {}

#run through all files in ../../rosetta_motifs/rmsd_out
for r,d,f in os.walk("../../rosetta_motifs/rmsd_out"):
	for file in f:
		if file.endswith("_rmsd_out.txt"):
			#get the system name from the front of the file
			sys_name = file.split("_")[0]

			#set file line counter at 0
			line_counter = 0

			#set temp tuples to mepty
			temp = []

			#read through the rmsd total file
			#open file stream
			read_file = open(r + "/" + file,"r")

			for line in read_file.readlines():
				
				#skip the line that says BEST
				if "BEST" in line:
					continue

				line_counter = line_counter + 1

				print(line,line_counter)

				if line_counter % 4 == 0:
					
					#handling to potentially add a temp tuple to the best_rmsds_dict
					#if the system is not already in the dictionary, make a blank list and append the first temp system
					if sys_name not in best_rmsds_dict.keys():
						best_rmsds_dict[sys_name] = []
						best_rmsds_dict[sys_name].append(temp)

					#handle if the amount of entries in the list for the system is within or at the maximum number of allowed entries
					#le
					if len(best_rmsds_dict[sys_name]) < top_x:
						best_rmsds_dict[sys_name].append(temp)
					else:
						#handle selecting the top x once we are at the cap

						#append the system to the list
						best_rmsds_dict[sys_name].append(temp)

						#sort the system list by ddg
						#sort the system list
						temp_list = sorted(best_rmsds_dict[sys_name], key=lambda x: x[0])
						best_rmsds_dict[sys_name] = temp_list

						#pop off the worst (highest value) ddg
						best_rmsds_dict[sys_name].pop()

					#clear the tuple after potentially adding it
					temp = []
				else:
					#strip the newline and add the data to the temp tuple
					temp_str = line.strip()

					#if line_counter % 2 = 0, it is the placement name with the ddg inside, get the ddg and append it to the temp tuple
					if line_counter % 2 == 0:
						ddg = temp_str.split("_delta_")[1].split("_")[0]

						#append the ddg and then temp string
						temp.append(ddg)

					temp.append(temp_str)

#now, run through each system, obtain the best rmsd from the top x ddg placements and write them to a csv file
for system in best_rmsds_dict.keys():
	#run a sort on the list and get the best placement by rmsd
	print(best_rmsds_dict[system])