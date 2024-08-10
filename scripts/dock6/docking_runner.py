
# runs rigid docking for all directories given a specified selected_sphs radius

import os, sys

# run selected_sphs with given radius

sph_radius = sys.argv[1]
print(f'generating selected_sphs with radius of {sph_radius}...')

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        print(f'{dir} sph')
        os.chdir(dir)
        os.system(f"../../../../dock6/bin/sphere_selector {dir}.sph crystal_ligand.mol2 {sph_radius}")
        print(f'{dir} sph DONE')
        os.chdir("..")

print("selected_sphs generated for all systems.")

# generate boxes for all systems

print("generating boxes...")

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        os.chdir(dir)
        print(dir)
        os.system("../../../../dock6/bin/showbox < showbox.in")
        os.chdir("..")

print("boxes generated for all systems.")

# generate grids for all systems
        
print("generating grids...")

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        print(f"Working on {dir}...")
        os.chdir(dir)
        os.system("../../../../dock6/bin/grid -i grid.in -o gridinfo.out")
        print(f"{dir} done!")
        os.chdir("..")

print("grids generated for all systems.")

# generate energy min ligands for all systems

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        print(f"Working on {dir}...")
        os.chdir(dir)
        os.system("../../../../dock6/bin/dock6 -i min.in -o min.out")
        print(f"{dir} done!")
        os.chdir("..")

print("energy minimized ligands generated for all systems.")

# generate radius_specific rigid.in files for all systems

print("generating rigid.ins...")

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        rigid_path = f"rigid{sph_radius}.in"
        print(f"generating for {dir}")
        os.chdir(dir)
        with open(rigid_path, 'w') as file:
            file.write("conformer_search_type rigid\n"
                        "use_internal_energy yes\n"
                        f"ligand_atom_file crystal_ligand.mol2\n"
                        "limit_max_ligands no\n"
                        "skip_molecule no\n"
                        "read_mol_solvation no\n"
                        "calculate_rmsd yes\n"
                        "use_rmsd_reference_mol yes\n"
                        f"rmsd_reference_filename crystal_ligand.mol2\n"
                        "use_database_filter no\n"
                        "orient_ligand yes\n"
                        "automated_matching yes\n"
                        "receptor_site_file selected_spheres.sph\n"
                        "max_orientations 1000\n"
                        "critical_points no\n"
                        "chemical_matching no\n"
                        "use_ligand_spheres no\n"
                        "bump_filter no\n"
                        "score_molecules yes\n"
                        "contact_score_primary no\n"
                        "contact_score_secondary no\n"
                        "grid_score_primary yes\n"
                        "grid_score_secondary no\n"
                        "grid_score_rep_rad_scale 1\n"
                        "grid_score_vdw_scale 1\n"
                        "grid_score_es_scale 1\n"
                        "grid_score_grid_prefix grid\n"
                        "multigrid_score_secondary no\n"
                        "dock3.5_score_secondary no\n"
                        "continuous_score_secondary no\n"
                        "footprint_similarity_score_secondary no\n"
                        "pharmacophore_score_secondary no\n"
                        "descriptor_score_secondary no\n"
                        "gbsa_zou_score_secondary no\n"
                        "gbsa_hawkins_score_secondary no\n"
                        "SASA_score_secondary no\n"
                        "amber_score_secondary no\n"
                        "minimize_ligand yes\n"
                        "simplex_max_iterations 1000\n"
                        "simplex_tors_premin_iterations 0\n"
                        "simplex_max_cycles 1\n"
                        "simplex_score_converge 0.1\n"
                        "simplex_cycle_converge 1.0\n"
                        "simplex_trans_step 1.0\n"
                        "simplex_rot_step 0.1\n"
                        "simplex_tors_step 10.0\n"
                        "simplex_random_seed 0\n"
                        "simplex_restraint_min no\n"
                        "atom_model all\n"
                        "vdw_defn_file /home/laura.lee5-umw/dock6/parameters/vdw_AMBER_parm99.defn\n"
                        "flex_defn_file /home/laura.lee5-umw/dock6/parameters/flex.defn\n"
                        "flex_drive_file /home/laura.lee5-umw/dock6/parameters/flex_drive.tbl\n"
                        f"ligand_outfile_prefix /home/laura.lee5-umw/thyme_lab_internship_2024/dock6/output_files/{dir}/rigid{sph_radius}.out\n"
                        "write_orientations no\n"
                        "num_scored_conformers 1\n"
                        "rank_ligands no\n")
        print(f"{dir} done")
        os.chdir("..")

print("rigid.ins generated for all systems.")


# run rigid docking for all systems

print("running docking...")

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        print(f"docking {dir}...")
        os.chdir(dir)
        os.system(f"../../../../dock6/bin/dock6 -i rigid{sph_radius}.in -o ../../output_files/{dir}/rigid{sph_radius}.out")
        print(f"{dir} done!")
        os.chdir("..")

print("docking finished for all systems.")

