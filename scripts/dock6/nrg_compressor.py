
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        if dir == "aa2ar":
            os.chdir(dir)
            for r_2,d_2,f_2 in os.walk(os.getcwd()):
                for file in f_2:
                    if file == "grid.nrg":
                        os.system("tar -czvf grid_nrg.tar.gz grid.nrg")
            os.chdir("..")
            

