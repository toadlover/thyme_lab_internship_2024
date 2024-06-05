
# file that compiles center coordinate data of all molecules in benchmarking folder into a .csv file.

import os, sys

# takes note of which directory to start on given user input and changes to that directory
os.chdir(sys.argv[1])

center_data_path = "center_data.csv"

with open(center_data_path, 'a') as file:
    
    for r_1,d_1,f_1 in os.walk(os.getcwd()):
        for dir in d_1:
            center = []
            center_x = None
            center_y = None
            center_z = None

            os.chdir(dir)

            for r_2,d_2,f_2 in os.walk(os.getcwd()):
            
                for data_file in f_2:
                    if "-lig" in data_file:
                        # calls center_finder.py on ligand and puts data in a temporary file
                                os.system("python /Users/laura/ThymeLab/AutoDockVinaBenchmarking/PythonScripts/center_finder.py" + f" /Users/laura/ThymeLab/AutoDockVinaBenchmarking/PythonScripts/AutoDock_Vina_Benchmarking/{dir}/{data_file}" + " > center.txt")
                                center_path = os.path.abspath("center.txt")
                        
    
                # gets x/y/z center coordinates of ligand 
                with open(os.path.abspath("center.txt"), 'r') as center_file:
                    for line in center_file:
                        center.append(line.strip("\n"))
                center_x = center[0]
                center_y = center[1]
                center_z = center[2]

            # adds coordinates in format name,x,y,z to center_data.csv
            file.write(f'{dir},{center_x},{center_y},{center_z}\n')

            # deletes temp file
            os.system("rm center.txt")

            # goes back to parent directory before moving to next iteration
            os.chdir("..")

    

