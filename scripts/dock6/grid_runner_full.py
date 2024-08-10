
# runs grid creation for ALL benchmarking directories

import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        print(f"Working on {dir}...")
        os.chdir(dir)
        os.system("../../../../dock6/bin/grid -i grid.in -o gridinfo.out")
        print(f"{dir} done!")
        os.chdir("..")
        
