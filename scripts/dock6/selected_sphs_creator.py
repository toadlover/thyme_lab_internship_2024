
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        print(dir)
        os.system(f"../../../../dock6/bin/sphere_selector {dir}.sph crystal_ligand.mol2 7.0")
        os.chdir("..")
            
