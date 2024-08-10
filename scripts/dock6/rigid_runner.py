
# runs rigid docking for ALL benchmarking directories

import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        print(f"Working on {dir}...")
        os.chdir(dir)
        os.system(f"../../../../dock6/bin/dock6 -i rigid.in -o ../../output_files/{dir}/rigid.out")
        print(f"{dir} done!")
        os.chdir("..")
