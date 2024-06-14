
import os

path_01 = "001-011.txt"
path_02 = "012-021.txt"
path_03 = "022-031.txt"
path_04 = "032-041.txt"
path_05 = "042-051.txt"
path_06 = "052-061.txt"
path_07 = "062-071.txt"
path_08 = "072-081.txt"
path_09 = "082-091.txt"
path_10 = "092-102.txt"

system_count = 0

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        system_count += 1
        if 1 <= system_count <= 11:
            with open(path_01, 'a') as file:
                file.write(f"{dir}\n")
        if 12 <= system_count <= 21:
            with open(path_02, 'a') as file:
                file.write(f"{dir}\n")
        if 22 <= system_count <= 31:
            with open(path_03, 'a') as file:
                file.write(f"{dir}\n")
        if 32 <= system_count <= 41:
            with open(path_04, 'a') as file:
                file.write(f"{dir}\n")
        if 41 <= system_count <= 51:
            with open(path_05, 'a') as file:
                file.write(f"{dir}\n")
        if 52 <= system_count <= 61:
            with open(path_06, 'a') as file:
                file.write(f"{dir}\n")
        if 62 <= system_count <= 71:
            with open(path_07, 'a') as file:
                file.write(f"{dir}\n")
        if 72 <= system_count <= 81:
            with open(path_08, 'a') as file:
                file.write(f"{dir}\n")
        if 82 <= system_count <= 91:
            with open(path_09, 'a') as file:
                file.write(f"{dir}\n")
        if 92 <= system_count <= 102:
            with open(path_10, 'a') as file:
                file.write(f"{dir}\n")
    


