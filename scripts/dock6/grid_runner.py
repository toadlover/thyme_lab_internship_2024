
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        os.system("../../../../dock6/bin/grid grid -i grid.in -o gridinfo.out")

        os.chdir("..")


        