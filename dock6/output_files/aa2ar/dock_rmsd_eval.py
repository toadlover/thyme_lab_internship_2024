
# calculates the best RMSD for the outputs of each system and stores it in a .csv file (format SYSTEM, BEST_RMSD)

import os

csv_path = "dock6_best_rmsds.csv"

rmsds_dict = {}

for r_1,d_1,f_1 in os.walk(os.getcwd()):
    for dir in d_1:
        if dir == "aa2ar":
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
                        atom_line_clean = line.split("        ")
                        atom_id = atom_line_clean[0].strip()
                        atom_coordinates = atom_line_clean[1].split("   ")
                        if "H" not in atom_id:
                            atom_x = float(atom_coordinates[0].strip())
                            atom_y = float(atom_coordinates[1].strip())
                            atom_z = float(atom_coordinates[2].split(" ")[0])                           
                            native_ligand[atom_id] = [atom_x, atom_y, atom_z]
            lig_file.close()


            for r_2,d_2,f_2 in os.walk(os.getcwd()):
                file_list = []
                for file in f_2:
                    if ".mol2" in file:
                        file_list.append(file)

            for out_file in file_list:
                print(f"READING {out_file} \n\n\n")
                with open(out_file, 'r') as out_file:
                    atom_start_index_out = 24
                    placement = {}

                    for j, line in enumerate(out_file):
                        if atom_start_index_out <= j < (atom_start_index_out + num_atoms):
                            out_atom_line_clean = line.split("        ")
                            out_atom_id = out_atom_line_clean[0].strip()
                            out_atom_coordinates = out_atom_line_clean[out_atom_line_clean.index(out_atom_id):]
                            
                            #out_atom_coordinates = [out_atom_line_clean[1].split("   ")]
                            print(out_atom_id, out_atom_coordinates)
                            if "H" not in atom_id:
                                out_atom_x = float(out_atom_coordinates[0])
                                out_atom_y = float(out_atom_coordinates[1])
                                out_atom_z = float(out_atom_coordinates[2].split(" ")[0])                           
                                placement[out_atom_id] = [out_atom_x, out_atom_y, out_atom_z]
                    print(placement)
                            
                    

                    

                

            
                 
        







                                                                                       
