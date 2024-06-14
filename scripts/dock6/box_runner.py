
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        if dir == "aa2ar":
            os.chdir(dir)
            os.system("../../../../dock6/bin/showbox < showbox.in")
        os.chdir("..")
