
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        os.system("rm rigid.out")
        os.system("rm rigid.out_scored.mol2")
        os.chdir("..")


