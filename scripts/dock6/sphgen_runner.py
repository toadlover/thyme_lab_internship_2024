
import os

os.chdir(pi/summer.thyme-umw/2024_intern_lab_space/thyme_lab_internship_2024/dock6/input_files)

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        # testing w/ aa2ar
        if dir == "aa2ar":
            os.chdir(dir)
            os.system("../../../dock6/bin/sphgen -i INSPH -o OUTSPH)
            
