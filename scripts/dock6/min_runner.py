
import os, sys

lists = ["001-011.txt", "012-021.txt", "022-031.txt", "032-041.txt", "042-051.txt", "052-061.txt", "062-071.txt", "072-081.txt", "082-091.txt", "092-102.txt"]

target_list = lists[int(sys.argv[1])]

system_list = []

with open(target_list, 'r') as file:
    for system in file:
        system_list.append(system.strip("\n"))


for r,d,f in os.walk(os.getcwd()):
    # walk through system dirs in input_files 
    for dir in d:
        if dir in system_list:
            os.chdir(dir)
            print(f"working on {dir}")
            os.system("tar -xvzf grid_nrg.tar.gz")
    
            # run min
            os.system(f"../../../../dock6/bin/dock6 dock6 -i min.in -o min.out")
            print(f"{dir} min done")
    
            # return to input_files system dir and delete .nrg file
            os.system("rm grid.nrg")
            print(f"{dir} nrg cleaned")
    
            os.chdir("..")
            
        
            
