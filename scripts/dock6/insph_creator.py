
import os, sys

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        insph_path = "INSPH"
        with open(insph_path, 'w') as file:
            file.write(f"{dir}.dms\nR\nX\n0\n2.0\n1.4\n{dir}.sph")
        os.chdir("..")
        
