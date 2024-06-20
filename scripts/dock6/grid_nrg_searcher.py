
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        nrg = False
        for r_2,d_2,f_2 in os.walk(os.getcwd()):
            for file in f_2:
                if file == "grid.nrg":
                    nrg = True
        if nrg == False:
            print(dir)
        os.chdir("..")
                    
