
# file that prints the Linux command to run AutoDock for all ligands in the AutoDock Vina Benchmarking folder.

import os, sys

# takes note of which directory to start on given user input and changes to that directory
os.chdir(sys.argv[1])

folder_list = []

# iterates through each folder in parent directory
for r_1,d_1,f_1 in os.walk(os.getcwd()):
    for dir in d_1:  
        os.chdir(dir)


        # Construct the path to the args.txt file
        vina_path = r"\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe"
        config_path = os.path.join(os.getcwd(), 'args.txt')
        
        

    
        # prints command for command line
        print(f'"{vina_path}" --config "{config_path}"' + ' > AutoDock_Vina_Benchmarking/')
        # os.system(f'"{vina_path}" --config "{config_path}"')
 
        
        # goes back to parent directory before moving to next iteration
        os.chdir("..")



