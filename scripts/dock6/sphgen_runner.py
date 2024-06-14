
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        if f"{dir}.sph" not in dir:
            print(f'{dir} is free')
                
        # os.system("../../../../dock6/bin/sphgen sphgen -i INSPH -o OUTSPH")
        os.chdir("..")
            
