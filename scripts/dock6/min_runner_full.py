
# runs min creation for ALL benchmarking directories

import os

import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        print(f"Working on {dir}...")
        os.chdir(dir)
        os.system("../../../../dock6/bin/dock6 -i min.in -o min.out")
        print(f"{dir} done!")
        os.chdir("..")
        
