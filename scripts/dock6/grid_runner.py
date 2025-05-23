
import os, sys

path_01 = "001-011.txt"
path_02 = "012-021.txt"
path_03 = "022-031.txt"
path_04 = "032-041.txt"
path_05 = "042-051.txt"
path_06 = "052-061.txt"
path_07 = "062-071.txt"
path_08 = "072-081.txt"
path_09 = "082-091.txt"
path_10 = "092-102.txt"

target_list = int(sys.argv[1])


system_list = []

if target_list == 1:
    with open(path_01, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))

elif target_list == 2:
    with open(path_02, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))

elif target_list == 3:
    with open(path_03, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))

elif target_list == 4:
    with open(path_04, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))

elif target_list == 5:
    with open(path_05, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))

elif target_list == 6:
    with open(path_06, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))

elif target_list == 7:
    with open(path_07, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))

elif target_list == 8:
    with open(path_08, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))

elif target_list == 9:
    with open(path_09, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))

elif target_list == 10:
    with open(path_10, 'r') as file:
        for system in file:
            system_list.append(system.strip("\n"))


for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        if dir in system_list:
            print(f"Working on {dir}...")
            os.chdir(dir)
            os.system("../../../../dock6/bin/grid -i grid.in -o gridinfo.out")
            print(f"{dir} done!")
            os.chdir("..")



        
