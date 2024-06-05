import os, sys

#load in files with rmsd data
#motif rmsd file to use located in benchmark data in /data/project/thymelab/running_Rosetta/ari_work/REU_shared_space/benchmark/runs/(run_dir)/rmsd_out/rmsd_total.txt
motif_rmsd_file = sys.argv[1]
#autodock rmsd file to use located in autodock benchmark data at "/data/project/thymelab/running_Rosetta/ari_work/REU_shared_space/AutoDock Vina Benchmarking/final_rmsd.txt"
autodock_rmsd_file = sys.argv[2]

#create dictionaries to hold all proteins with rmsd from each set
motif_set = {}
autodock_set = {}

#create a third dictionary for comparison of systems present in the motif and autodock sets
comparison_set = {}

#read the motif rmsd file to fill its dictionary
motif_file = open(motif_rmsd_file, 'r')

#format of this file is a pattern every 4 lines
#line 1 has the system name, line 2 has the best rmsd, line 3 has the file name, line 4 is blank
#only need info from lines 1 and 2

line_counter = 1
name_holder = ""
rmsd_holder = 0

for line in motif_file.readlines():
	if line_counter % 4 == 1:
		name_holder = line.strip("\n")
	if line_counter % 4 == 2:
		rmsd_holder = float(line.strip("\n"))

		#add entry to dictionary
		motif_set[name_holder] = rmsd_holder
	line_counter = line_counter + 1
motif_file.close()
#print(motif_set)

#get data from the autodock file
#system with rmsd is located on individual lines. Ignore lines with a semicolon
autodock_file = open(autodock_rmsd_file, "r")

for line in autodock_file.readlines():
	if ":" not in line and len(line) > 5:
		autodock_set[line.split()[0]] = float(line.split()[1].strip("\n"))

#print(autodock_set)

#run through motif set and see if system is also present in autodock set
#if hits in both, then will run a comparison
for system in motif_set.keys():
	if system in autodock_set.keys():
		#print(system)

		#determine which system has the better rmsd and by how much
		#add it to the comparison set
		# a negative value indicates that motif has better rmsd, positive indicates that autodock is better
		comparison_set[system] = motif_set[system] - autodock_set[system]

#split up comparison set into brackets of differentials for which method got a lower rmsd and by how much
#rmsd differential breakpoints at 0.2, 0.5, 1, 2, >2
#also tie if diff is 0
#indices are as follows:
"""
0 - motif better, 0-0.2
1 - motif better, 0.2-0.5
2 - motif better, 0.5-1
3 - motif better, 1-2
4 - motif better, >2
5 - autodock better, 0-0.2
6 - autodock better, 0.2-0.5
7 - autodock better, 0.5-1
8 - autodock better, 1-2
9 - autodock better, >2
10 - tie
"""
breakpoints = [[],[],[],[],[],[],[],[],[],[],[]]

for system in comparison_set.keys():
	#motif better, 0-0.2
	if comparison_set[system] < 0 and comparison_set[system] >= -0.2:
		breakpoints[0].append([system, -1 * comparison_set[system]])
	#motif better, 0.2-0.5
	if comparison_set[system] < -0.2 and comparison_set[system] >= -0.5:
		breakpoints[1].append([system, -1 * comparison_set[system]])
	#motif better, 0.5-1
	if comparison_set[system] < -0.5 and comparison_set[system] >= -1:
		breakpoints[2].append([system, -1 * comparison_set[system]])
	#motif better, 1-2
	if comparison_set[system] < -1 and comparison_set[system] >= -2:
		breakpoints[3].append([system, -1 * comparison_set[system]])
	#motif better, >2
	if comparison_set[system] < -2:
		breakpoints[4].append([system, -1 * comparison_set[system]])
	#autodock better, 0-0.2 
	if comparison_set[system] > 0 and comparison_set[system] <= 0.2:
		breakpoints[5].append([system, comparison_set[system]])
	#autodock better, 0.2-0.5
	if comparison_set[system] > 0.2 and comparison_set[system] <= 0.5:
		breakpoints[6].append([system, comparison_set[system]])
	#autodock better, 0.5-1
	if comparison_set[system] > 0.5 and comparison_set[system] <= 1:
		breakpoints[7].append([system, comparison_set[system]])
	#autodock better, 1-2
	if comparison_set[system] > 1 and comparison_set[system] <= 2:
		breakpoints[8].append([system, comparison_set[system]])
	#autodock better, >2
	if comparison_set[system] > 2:
		breakpoints[9].append([system, comparison_set[system]])
	#tie, 0
	if comparison_set[system] == 0:
		breakpoints[10].append([system, comparison_set[system]])

#write differentials to out file
diff_file = open("differentials.txt", "w")

for i in range(11):
	if i == 0:
		diff_file.write("Motifs better within 0.2: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 1:
		diff_file.write("Motifs better from 0.2-0.5: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 2:
		diff_file.write("Motifs better from 0.5-1: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 3:
		diff_file.write("Motifs better from 1-2: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 4:
		diff_file.write("Motifs better by more than 2: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 5:
		diff_file.write("AutoDock better within 0.2: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 6:
		diff_file.write("AutoDock better from 0.2-0.5: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 7:
		diff_file.write("AutoDock better from 0.5-1: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 8:
		diff_file.write("AutoDock better from 1-2: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 9:
		diff_file.write("AutoDock better by more than 2: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
	if i == 10:
		diff_file.write("Tie: " + str(len(breakpoints[i])) + "\n")
		for system in breakpoints[i]:
			diff_file.write(system[0] + " " + str(system[1]) + "\n")
