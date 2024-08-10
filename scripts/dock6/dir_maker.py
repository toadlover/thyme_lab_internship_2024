
# adds empty directories for all of the systems into output_files

import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        if dir != "aa2ar" and dir != "abl1" and dir != "ace":
            os.system(f"mkdir ../output_files/{dir}")
