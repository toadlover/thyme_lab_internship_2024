#Ari Ginsparg
#6/4/2024

import os,sys

#open stream for rmsd_total.txt
read_file = open("rmsd_total.txt", "r")

#open write stream
write_file = open("motifs_rmsds.csv", "w")

#line counter since every 4 lines in rmsd_total has data for a single system
line_counter = 0

#list to hold all of the systems (will sort alphabetically before writing to file)
system_list = []

#temporary list to store a tuple of data for each system (system name, best rmsd, name of pdb file that produced the placement)
temp = []

#read through the rmsd total file
for line in read_file.readlines():
	line_counter = line_counter + 1

	if line_counter % 4 == 0:
		#the line should be blank, add the complete tuple to the system list
		system_list.append(temp)
		temp = []
	else:
		#strip the newline and add the data to the temp tuple
		temp_str = line.strip()
		temp.append(temp_str)

#sort the system list
temp_list = sorted(system_list, key=lambda x: x[0])
system_list = temp_list

write_file.write("system,rmsd,placement_pdb\n")

#write the system list
for item in system_list:
	write_file.write(item[0] + "," + item[1] + "," + item[2] + "\n")
