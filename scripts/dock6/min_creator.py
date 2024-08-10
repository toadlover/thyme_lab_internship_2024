
import os

for r,d,f in os.walk(os.getcwd()):
    for dir in d:
        print(dir)
        os.chdir(r + "/" + dir)
        min_path = "min.in"
    
        with open(min_path, 'w') as file:
            file.write("conformer_search_type rigid\n"
                       "use_internal_energy yes\n"
                       "internal_energy_rep_exp 12\n"
                       "internal_energy_cutoff 100.0\n"
                       f"ligand_atom_file crystal_ligand.mol2\n"
                       "limit_max_ligands no\n"
                       "skip_molecule no\n"
                       "read_mol_solvation no \n"
                       "calculate_rmsd yes\n"
                       "use_rmsd_reference_mol yes\n"
                       f"rmsd_reference_filename crystal_ligand.mol2\n"
                       "use_database_filter no\n"
                       "orient_ligand no\n"
                       "bump_filter no\n"
                       "score_molecules yes\n"
                       "contact_score_primary no \n"
                       "contact_score_secondary no \n"
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
                       "simplex_restraint_min yes\n"
                       "simplex_coefficient_restraint 10.0\n"
                       "atom_model all\n"
                       "vdw_defn_file /home/laura.lee5-umw/dock6/parameters/vdw_AMBER_parm99.defn\n"
                       "flex_defn_file /home/laura.lee5-umw/dock6/parameters/flex.defn\n"
                       "flex_drive_file /home/laura.lee5-umw/dock6/parameters/flex_drive.tbl\n"
                       f"ligand_outfile_prefix {dir}.lig.min\n"
                       "write_orientations no\n"
                       "num_scored_conformers 1\n"
                       "rank_ligands no")
        os.chdir("..")

                   




