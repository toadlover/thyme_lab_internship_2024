
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        if dir == "aa2ar":
            os.chdir(dir)
            os.system(f"../../../../dock6/bin/sphere_selector {dir}.sph {dir}.mol2 10.0")
        os.chdir("..")
            
