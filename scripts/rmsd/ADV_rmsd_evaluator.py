
import os, sys

os.chdir(sys.argv[1])

best_rmsds_path = "ADV_best_rmsds.csv"

rmsd_dict = {}

# walk through each directory and collect an RMSD that compares all ligands in output.pdbqt against {name}-lig.pdbqt
for r_1,d_1,f_1 in os.walk(os.getcwd()):
    for dir in d_1:
        # read the {name}-lig.pdbqt file and get coordinates of all non-hydrogen atoms
		# store coordinates with atom ID in 4 index list [id, x, y, z]
		# store in dictionary

        native_ligand = {}
    
        lig_path = f'{dir}/{dir}-lig.pdb'
    

        with open(lig_path, 'r') as lig_file:
            for line in lig_file:

                # isolates lines that have atom data
                if line.startswith("ATOM"):
                    atom_id = line.split()[2]

                    # adds coordinates of atoms that are not hydrogens into native_ligand dictionary
                    if atom_id[0] != "H":
                        native_ligand[atom_id] = [float(line.split()[5]),float(line.split()[6]),float(line.split()[7])]
        
        lig_file.close()
    
    
        # make a list of dictionaries for each model in the output.pdbqt file
        placed_ligands = []
        working_placement = {}

        out_path = f'{dir}/output.pdbqt'

        with open(out_path, 'r') as out_file:
            for line in out_file:
                # notes when a new model begins
                if line.startswith("MODEL"):
                    # generate clear working placement
                    working_placement = {}
                if line.startswith("ENDMDL"):
                    # add to placed_ligands at end of model
                    placed_ligands.append(working_placement)
                if line.startswith("ATOM"):
                    atom_id = line.split()[2]

                    # adds coordinates of atoms that are not hydrogens into working_placement dictionary
                    if atom_id[0] != "H":
                        working_placement[atom_id] = [float(line.split()[5]),float(line.split()[6]),float(line.split()[7])]

        out_file.close()

        # print(placed_ligands)

        # get RMSD for each placement against native ligand and store in rmsd_list

        rmsd_list = []

        for placement in placed_ligands:
            distance_sum = 0
            atom_counter = 0
            
            # work through each atom in placement for the comparison
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
        # print(dir, rmsd_list)

        # determine the best RMSD
        best_rmsd = None
        best_rmsd_model = None
        
        for curr_rmsd in rmsd_list:
            if best_rmsd == None:
                best_rmsd = curr_rmsd
            else:
                if curr_rmsd <= best_rmsd:
                    best_rmsd = curr_rmsd
        best_rmsd_model = rmsd_list.index(best_rmsd)

        # add best_rmsd to rmsd_dict
        rmsd_dict[dir] = best_rmsd

        # print("Best RMSD model is: " + str(best_rmsd_model) + " with an RMSD of " + str(best_rmsd))

with open(best_rmsds_path, 'a') as file:
    for key in rmsd_dict.keys():
        file.write(str(key) + "," + str(rmsd_dict[key]) + "\n")
                
 


