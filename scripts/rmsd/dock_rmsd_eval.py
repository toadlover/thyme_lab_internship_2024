
# calculates the best RMSD for the outputs of each system and stores it in a .csv file (format SYSTEM, BEST_RMSD)

import os

csv_path = "dock6_best_rmsds.csv"

rmsds_dict = {}

for r_1,d_1,f_1 in os.walk(os.getcwd()):
    for dir in d_1:

        print(dir)

        num_atoms = 0
        os.chdir(dir)
        native_ligand = {}
        
        lig_path = f"../../input_files/{dir}/crystal_ligand.mol2"

        rmsd_list = []
        best_rmsd = None
        
        # reads native ligand file for reference coordinates
        with open(lig_path, 'r') as lig_file:
            
            atom_start_index = 7
            
            for i, line in enumerate(lig_file):
                # reads number of atoms in ligand from file
                if i == 2:
                    atom_count_line = line.strip()
                    atom_count_line_clean = line.split("    ")
                    num_atoms = int(atom_count_line_clean[0])
                    

                # adds coordinates of atoms in native ligand to native_ligand dictionary
                if atom_start_index <= i < (atom_start_index + num_atoms):
                    atom_id = line.strip()[:8].strip()
                    atom_coordinates = line.strip()[8:].strip().split("  ")

                    
                    #atom_line_clean = line.split("        ")
                    #atom_id = atom_line_clean[0].strip()
                    #atom_coordinates = atom_line_clean[1].split("   ")

                    for value in atom_coordinates:
                        if value == "":
                            atom_coordinates.pop(atom_coordinates.index(value))
                    
                    if "H" not in atom_id:
                        atom_x = float(atom_coordinates[0].strip())
                        atom_y = float(atom_coordinates[1].strip())
                        atom_z = float(atom_coordinates[2].strip(" ").split()[0])                           
                        native_ligand[atom_id] = [atom_x, atom_y, atom_z]
        lig_file.close()



        for r_2,d_2,f_2 in os.walk(os.getcwd()):
            file_list = []
            for file in f_2:
                if ".mol2" in file and os.path.getsize(file) > 0:
                    file_list.append(file)
                    
        

        
        for out_file in file_list:
            
            print(out_file)

            lines = []
            placement = {}
            with open(out_file, 'r') as output:

                atom_start_index_out = 0
                atom_end_index_out = 0

                for j, line in enumerate(output):
                    if "@<TRIPOS>ATOM" in line:
                        atom_start_index_out = j

                    if "@<TRIPOS>BOND" in line:
                        atom_end_index_out = j
                 
            output.close()

            with open(out_file, 'r') as output:
                
                
                for k, line in enumerate(output):
                    


                    # adds coordinates of atoms in output to placement dictionary
                    if atom_start_index_out < k < atom_end_index_out:


                        out_atom_id = line.strip()[:8].strip()
                        out_atom_coordinates = line.strip()[8:].strip().split("  ")
                        
                        for value in out_atom_coordinates:
                            if value == "":
                                out_atom_coordinates.pop(out_atom_coordinates.index(value))

                        if "H" not in out_atom_id:
                            out_atom_x = float(out_atom_coordinates[0].strip())
                            out_atom_y = float(out_atom_coordinates[1].strip())
                            out_atom_z = float(out_atom_coordinates[2].strip().split(" ")[0])
                            placement[out_atom_id] = [out_atom_x, out_atom_y, out_atom_z]


                

                
                non_hydrogen_atoms = len(placement)

                distance_sum = 0

                # iterates through all atoms and calculate distance between output and native placement
                for atom in placement.keys():
                    a1 = placement[atom]
                    a2 = native_ligand[atom]

                    x = (a1[0] - a2[0])**2
                    y = (a1[1] - a2[1])**2
                    z = (a1[2] - a2[2])**2

                    dist = x+y+z

                    sqrt_dist = dist**0.5
                    
                    distance_sum += sqrt_dist

                    print(atom,a1,a2,dist,sqrt_dist)
                
                #print(distance_sum, non_hydrogen_atoms)
                rmsd = distance_sum/non_hydrogen_atoms

                print(distance_sum,non_hydrogen_atoms,rmsd)

                rmsd_list.append(rmsd)

        print(rmsd_list)

        best_rmsd = min(rmsd_list)

        print("Best: ", best_rmsd)

        rmsds_dict[dir] = best_rmsd

        print(rmsds_dict[dir])

        os.chdir("..")


with open(csv_path, 'a') as rmsd_file:
    for key in rmsds_dict.keys():
        rmsd_file.write(str(key) + "," + str(rmsds_dict[key]) + "\n")
        






                    

                    
                            
                    

                    

                

            
                 
        







                                                                                       