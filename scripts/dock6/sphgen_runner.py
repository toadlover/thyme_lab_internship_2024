
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        done = False
        for r_2,d_2,f_2 in os.walk(os.getcwd()):
            for file in f_2:
                if ".sph" in file:
                    done = True
            if done == False:
                print(f"{dir} is free")
        
                
        # os.system("../../../../dock6/bin/sphgen sphgen -i INSPH -o OUTSPH")
        os.chdir("..")
            
