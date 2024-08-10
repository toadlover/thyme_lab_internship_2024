
# checks for discrepancies between directory name and .mol2

import os

for r,d,f in os.walk(os.getcwd()):
    dir_list = []
    wrong_sys_list = []
    for dir in d:
        dir_list.append(dir)
        os.chdir(dir)
        line_list = []
        mol2_line = []
        dir_path = f"{dir}.mol2"
        with open(dir_path, 'r') as file:
            for line in file:
                line_list.append(line.strip("\n"))
        if f"{dir}" in line_list[1]:
            dir_list.remove(dir)
        else:
            mol2_line = line_list[1].split(".")
            wrong_sys = mol2_line[0]
            wrong_sys_list.append(wrong_sys)
            print(f"{dir} WRONG; {wrong_sys}")
        os.chdir("..")
           

print(wrong_sys_list)




