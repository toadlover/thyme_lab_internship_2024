
import os, sys

# takes note of which directory to start on given user input and changes to that directory
# os.chdir(sys.argv[1])

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        grid_path = "grid.in"
        with open(grid_path, 'w') as file:
            file.write(f"allow_non_integral_charges yes \ncompute_grids yes \ngrid_spacing 0.4 \noutput_molecule no \ncontact_score no \nenergy_score yes \nenergy_cutoff_distance 9999 \natom_model a \nattractive_exponent 6 \nrepulsive_exponent 9 \ndistance_dielectric yes \ndielectric_factor 4 \nbump_filter yes \nbump_overlap 0.75 \nreceptor_file {dir}.mol2 \nbox_file {dir}.box.pdb \nvdw_definition_file /home/laura.lee5-umw/dock6/parameters/vdw_AMBER_parm99.defn \nscore_grid_prefix grid")
        os.chdir("..")
