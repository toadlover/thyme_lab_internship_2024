#Ari Ginsparg
#6/4/2024
#Schrodinger rmsd calculation script

#usage: run this script from within the scripts/rmsd directory for all location-based operations to work
#run: python schrodinger_rmsd.py

import os,sys

#initial check to ensure that user is running script out of correct directory:
if os.getcwd().endswith("/thyme_lab_internship_2024/scripts/rmsd") == False:
	print("You are not working in the right location for this script to work!")
	print("You are working out of: " + os.getcwd())
	print("You need to work out of /(path to repository)/thyme_lab_internship_2024/scripts/rmsd")
	quit()

#initial declaration of a dictionary to hold all of the rmsd values per system
best_rmsd_dict = {}

#read through all of the dude ligands and attempt to collect rmsd off of them
#the running of the script makes a difference, as the script won't work if you do not run this script from the right location
for r,d,f in os.walk("../../dude_library_simple/"):
	for dire in d:
		print(dire)

		#for this system, create a dictionary that holds the ligand atoms and their coordinates; atom name is the key and the coordinates are stored in a list as x,y,z
		#ignore hydrogens
		native_atoms = {}

		#open the corresponding ligand mol2 file
		crystal_lig = open("../../dude_library_simple/" + dire + "/crystal_ligand.mol2", "r")

		#boolean to determine whether to record atom data; start recording at @<TRIPOS>ATOM and stop at @<TRIPOS>BOND
		read = False

		for line in crystal_lig.readlines():

			#turn off reading if we hit the bond line
			if "@<TRIPOS>BOND" in line:
				break

			#set atom coordinates for atom id in native
			if read:
				native_atoms[line.split()[1]] = [float(line.split()[2]), float(line.split()[3]), float(line.split()[4])]

			#control reading at end of loop
			if "@<TRIPOS>ATOM" in line:
				read = True

		crystal_lig.close()

		#now read through all schrodinger ligand placements
		#check if there is a corresponding -pose.mol2 file
		if os.path.isfile("../../schrodinger_glide/binding_poses" + dire + "-poses.mol2"):
			#read the file
			#count the number of poses collected
			#print all rmsds to a unique file for the system, and keep + note the best rmsd in the dictionary to compile all best
			rmsd_file = open("../../schrodinger_glide/binding_poses/rmsd/" + dire + "_rmsd.csv", "w")

			pose_file = open("../../schrodinger_glide/binding_poses" + dire + "-poses.mol2", "r")

			#pose counter
			pose_counter = 0

			#variable to hold the best pose and the best rmsd
			best_pose = 0
			best_rmsd = 100

			#determine when to read atoms, once we are determined to be in the atom block
			read = False

			#variable to hold the sum of distances for rmsd
			distance_sum = 0

			#variable to holdthe count of atoms being used in calculating rmsd (will be used to derive an average distance)
			atom_count = 0

			for line in pose_file.readlines():
				#when we hit @<TRIPOS>MOLECULE, that means that we are on a new pose
				#increment the pose counter
				if "@<TRIPOS>MOLECULE" in line:
					pose_counter = pose_counter + 1

				#turn off reading if we hit the bond line
				#calculate RMSD for this molecule
				if "@<TRIPOS>BOND" in line:
					read = False
					#derive the rmsd (distance sum/atom count)
					rmsd = distance_sum/atom_count
					print(rmsd)
					#write the rmsd and pose numebr to the write file
					rmsd_file.write(str(pose_counter) + "," + str(rmsd) + "\n")
					#determine if this is the best rmsd so far
					if rmsd < best_rmsd:
						best_rmsd = rmsd
						best_pose = pose_counter
					#reset variables for next pose
					atom_count = 0
					distance_sum = 0

				#if we can read, read in the atom line and get the atom's distance from the native position
				if read:

					#get difference of x,y,z coordinates and square
					x = (native_atoms[line.split()[1]][0] - float(line.split()[2])) ** 2
					y = (native_atoms[line.split()[1]][1] - float(line.split()[3])) ** 2
					z = (native_atoms[line.split()[1]][2] - float(line.split()[4])) ** 2

					#take sum of xyz square distances and get square root
					distance = (x + y + z) ** 0.5

					#add distance to distance sum
					distance_sum = distance_sum + distance

					#increment the atom count
					atom_count = atom_count + 1

				if "@<TRIPOS>ATOM" in line:
					read = True

			#write the best rmsd, best pose, and total number of poses to the best dictionary
			best_rmsd_dict[dire] = str(best_rmsd) + "," + str(best_pose) + "," + str(pose_counter)

			#close the file streams
			rmsd_file.close()
			pose_file.close()
		else:
			#write a filler line into the dictionary
			best_rmsd_dict[dire] = "NA,NA,NA"

#turn the best rmsd dictionary into a list of strings for writing in alphabetical order
best_rmsd_list = []

for key in best_rmsd_dict.keys():
	best_rmsd_list.append(str(key) + "," + best_rmsd_dict[key])

#sort the list
best_rmsd_list = best_rmsd_list.sort()

rmsd_file = open("../../schrodinger_glide/binding_poses/rmsd/glide_best_rmsd.csv", "w")

for lig in best_rmsd_list:
	rmsd_file.write(lig + "\n")

rmsd_file.close()