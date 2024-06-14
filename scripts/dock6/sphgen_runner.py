
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        sph_done = False
        outsph_done = False
        for r_2,d_2,f_2 in os.walk(os.getcwd()):
            for file in f_2:
                if ".sph" in file:
                    sph_done = True
                if "OUTSPH" in file:
                    outsph_done = True
            if sph_done == True and outsph_done == False:
                print(f"{dir} needs OUTSPH")
            if sph_done == False and outsph_done == True:
                print(f"{dir} needs .sph")
        
                
        # os.system("../../../../dock6/bin/sphgen sphgen -i INSPH -o OUTSPH")
        os.chdir("..")
            
