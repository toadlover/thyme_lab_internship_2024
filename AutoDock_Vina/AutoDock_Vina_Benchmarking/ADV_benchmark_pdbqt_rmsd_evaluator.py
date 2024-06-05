import os, sys

location = os.getcwd()

rmsd_dict = {}

#walk through each directory and collect an RMSD that compares all ligands in output.pdbqt against ligand.pdbqt
for r,d,f in os.walk(location):
	for dire in d:
		#read the ligand.pdbqt file and get coordinates of all non-hydrogen atoms
		#store coordinates with atom ID in 4 index list [id, x, y, z]
		#store in dictionary
		native_ligand = {}

		if os.path.isfile(r + "/" + dire + "/ligand.pdbqt") == False:
			continue

		nat_file = open(r + "/" + dire + "/ligand.pdbqt" )

		print(r + "/" + dire + "/ligand.pdbqt")
		for line in nat_file.readlines():
			#print(line)
			#if line starts with ATOM, has data on an atom for us to collect
			if line.startswith("ATOM"):
				#atom id at split index 2, xyz at 5-7
				at_id = line.split()[2]
				#continue if hydrogen (ignore if first char is H)
				if at_id[0] == 'H':
					continue

				#if good, push list to native_ligand dictionary
				native_ligand[at_id] = [float(line.split()[5]),float(line.split()[6]),float(line.split()[7])]

		nat_file.close()

		#print(native_ligand)

		#make a list of dictionaries for each model in the optput pdbqt file
		placed_ligands = []

		working_placement = {}

		if os.path.isfile(r + "/" + dire + "/output.pdbqt") == False:
			continue

		place_file = open(r + "/" + dire + "/output.pdbqt" )

		for line in place_file.readlines():
			#handling for hitting a MODEL line, indicating a new placement
			if line.startswith("MODEL"):
				#generate/clear working_placement
				working_placement = {}

			#at end of model, push to placed_ligands
			if line.startswith("ENDMDL"):
				placed_ligands.append(working_placement)

			#get atom data for non-hydrogens, like above
			#if line starts with ATOM, has data on an atom for us to collect
			if line.startswith("ATOM"):
				#atom id at split index 2, xyz at 5-7
				at_id = line.split()[2]
				#continue if hydrogen (ignore if first char is H)
				if at_id[0] == 'H':
					continue

				#if good, push list to native_ligand dictionary
				working_placement[at_id] = [float(line.split()[5]),float(line.split()[6]),float(line.split()[7])]

		place_file.close()

		print(len(placed_ligands))

		#get RMSD for each placement against native
		#store RMSD in rmsd_list

		rmsd_list = []

		for placement in placed_ligands:
			#print(len(placement),len(native_ligand))

			distance_sum = 0
			atom_counter = 0

			#work through each atom in placement for the comparison
			for atom in placement.keys():
				
				dist = 0


				if atom in placement and atom in native_ligand:

					a1 = placement[atom]
					a2 = native_ligand[atom]

					x = (a1[0] - a2[0])**2
					y = (a1[1] - a2[1])**2
					z = (a1[2] - a2[2])**2

					dist = (x + y + z) ** 0.5

					distance_sum = distance_sum + dist
					atom_counter = atom_counter + 1

			#rmsd = average of distance sum (distance_sum/atom_counter)
			rmsd = distance_sum / atom_counter

			rmsd_list.append(rmsd)
			print(rmsd)

		#determine the best RMSD
		best_rmsd = rmsd_list[0]
		best_rmsd_model = 1

		for rmsd_val in range(len(rmsd_list)):
			if rmsd_list[rmsd_val] <= best_rmsd:
				best_rmsd = rmsd_list[rmsd_val]
				best_rmsd_model = rmsd_val + 1

		print("Best RMSD model is model: " + str(best_rmsd_model) + " with an RMSD of " + str(best_rmsd))

		#write RMSD with indication of best in rmsd.txt in the directory being used
		write_rmsd = open(r + "/" + dire + "/rmsd.txt", "w")
		write_rmsd.write("Best: " + str (best_rmsd) + "\n")
		for val in rmsd_list:
			write_rmsd.write(str(val) + "\n")

		write_rmsd.close()

		#add rmsd to dict
		rmsd_dict[dire] = best_rmsd

#after collecting all rmsd values, cluster them into groups based on rmsd
#groups are <1, 1-2, 2-5, 5-10, 10+
#each correspond to indiced in rmsd_breakdown in listed order

rmsd_breakdown = [[],[],[],[],[]]

for prot in rmsd_dict.keys():
	if float(rmsd_dict[prot]) < 1:
		rmsd_breakdown[0].append([prot,rmsd_dict[prot]])
	if float(rmsd_dict[prot]) >= 1 and float(rmsd_dict[prot]) < 2:
		rmsd_breakdown[1].append([prot,rmsd_dict[prot]])
	if float(rmsd_dict[prot]) >= 2 and float(rmsd_dict[prot]) < 5:
		rmsd_breakdown[2].append([prot,rmsd_dict[prot]])
	if float(rmsd_dict[prot]) >= 5 and float(rmsd_dict[prot]) < 10:
		rmsd_breakdown[3].append([prot,rmsd_dict[prot]])
	if float(rmsd_dict[prot]) >= 10:
		rmsd_breakdown[4].append([prot,rmsd_dict[prot]])

#output breakdown
print("<1: " + str(len(rmsd_breakdown[0])))
print(rmsd_breakdown[0])
print("1-2: " + str(len(rmsd_breakdown[1])))
print(rmsd_breakdown[1])
print("2-5: " + str(len(rmsd_breakdown[2])))
print(rmsd_breakdown[2])
print("5-10: " + str(len(rmsd_breakdown[3])))
print(rmsd_breakdown[3])
print(">10: " + str(len(rmsd_breakdown[4])))
print(rmsd_breakdown[4])

#write to an output file too
final_out = open("final_rmsd.txt", "w")
final_out.write("<1: " + str(len(rmsd_breakdown[0])))
final_out.write("\n")
for entry in rmsd_breakdown[0]:
	final_out.write(str(entry[0]) + " " + str(entry[1]))
	final_out.write("\n")
final_out.write("1-2: " + str(len(rmsd_breakdown[1])))
final_out.write("\n")
for entry in rmsd_breakdown[1]:
	final_out.write(str(entry[0]) + " " + str(entry[1]))
	final_out.write("\n")
final_out.write("2-5: " + str(len(rmsd_breakdown[2])))
final_out.write("\n")
for entry in rmsd_breakdown[2]:
	final_out.write(str(entry[0]) + " " + str(entry[1]))
	final_out.write("\n")
final_out.write("5-10: " + str(len(rmsd_breakdown[3])))
final_out.write("\n")
for entry in rmsd_breakdown[3]:
	final_out.write(str(entry[0]) + " " + str(entry[1]))
	final_out.write("\n")
final_out.write(">10: " + str(len(rmsd_breakdown[4])))
final_out.write("\n")
for entry in rmsd_breakdown[4]:
	final_out.write(str(entry[0]) + " " + str(entry[1]))
	final_out.write("\n")
