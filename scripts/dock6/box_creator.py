
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        box_path = "showbox.in"
        with open(box_path, 'w') as file:
            file.write(f"Y \n8.0 \n../002_surface_spheres/selected_spheres.sph \n1 \n{dir}.box.pdb")
        os.chdir("..")
