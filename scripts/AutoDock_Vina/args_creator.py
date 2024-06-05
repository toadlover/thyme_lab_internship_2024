
# file intended to run through inputted location and create args.txt for each molecule folder.

import os, sys

# takes note of which directory to start on given user input and changes to that directory
os.chdir(sys.argv[1])


folder_list = []

# iterates through each folder in parent directory
for r_1,d_1,f_1 in os.walk(os.getcwd()):
    for dir in d_1:  
        folder_list.append(dir)
        os.chdir(dir)
        args_path = "args.txt"
        receptor_path = None
        ligand_path = None
        out_path = None
        center_path = None
        center = []
        center_x = None
        center_y = None
        center_z = None

        # opens args.txt
        with open(args_path, 'w') as file:
            for r_2,d_2,f_2 in os.walk(os.getcwd()):

                # gets required paths
                for data_file in f_2:
                    if "-lig" in data_file:

                        # calls center_finder.py on ligand
                        os.system("python /Users/laura/ThymeLab/AutoDockVinaBenchmarking/PythonScripts/center_finder.py" + f" /Users/laura/ThymeLab/AutoDockVinaBenchmarking/PythonScripts/AutoDock_Vina_Benchmarking/{dir}/{data_file}" + " > center.txt")
                        center_path = os.path.abspath("center.txt")
                    elif "receptor.pdbqt" in data_file:
                        receptor_path = os.path.abspath(data_file)
                    elif "ligand.pdbqt" in data_file:
                        ligand_path = os.path.abspath(data_file)
                    elif "output.pdbqt" in data_file:
                        output_path = os.path.abspath(data_file)

                # gets x/y/z center coordinates of ligand 
                with open(os.path.abspath("center.txt"), 'r') as center_file:
                    for line in center_file:
                        center.append(line.strip("\n"))
                center_x = center[0]
                center_y = center[1]
                center_z = center[2]

            # writes args.txt
            file.write(f'receptor = "{receptor_path}" \nligand = "{ligand_path}" \n \ncenter_x = {center_x} \ncenter_y = {center_y} \ncenter_z = {center_z} \n \nsize_x = 20 \nsize_y = 20 \nsize_z = 20 \n \nout = "{output_path}"')

        # deletes center.txt
        os.system("rm center.txt")
                            
        # goes back to parent directory before moving to next iteration
        os.chdir("..")
        
    



