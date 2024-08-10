
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        os.system(f"mv min.in ../../input_files/{dir}/")
        os.chdir("..")
