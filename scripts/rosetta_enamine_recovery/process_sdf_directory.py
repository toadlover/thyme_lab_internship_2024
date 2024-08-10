import os
import sys
import subprocess

# Check if the directory argument is provided
if len(sys.argv) < 2:
    print("Usage: python3 process_sdf_directory.py /path/to/sdf/directory")
    sys.exit(1)

# Define the directory containing the SDF files
input_directory = sys.argv[1]

# Define the path to the conformator tool and the license
conformator_path = "/Applications/conformator.app/Contents/MacOS/conformator"
license_key = #Add license key here

# Function to process each SDF file
def process_sdf(starting_file):
    # Split name to remove extension
    starting_file_no_ext = starting_file.split(".")[0]

    # Make a directory to perform all operations in and then move into it
    os.makedirs(starting_file_no_ext, exist_ok=True)
    subprocess.run(["mv", starting_file, starting_file_no_ext])
    os.chdir(starting_file_no_ext)

    # Activate conformator
    subprocess.run([conformator_path, "--license", license_key])

    # Run conformator on the starting file
    subprocess.run([conformator_path, "-i", starting_file, "-o", "confs.sdf", "--keep3d", "--hydrogens", "-n", "15", "-v", "0"])

    # Use babel to break the confs.sdf file into individual sdf files; also apply unique names to the ligand name (per conformer)
    subprocess.run(["obabel", "confs.sdf", "-O", "individual_conf.sdf", "-m"])

    # Make a molecule name dictionary to hold the molecule name and number of times that it has been encountered
    molecule_name_dict = {}

    # Make directories to hold single ligand conformer SDFs and params
    os.makedirs("single_conf_sdfs", exist_ok=True)
    os.makedirs("single_conf_params", exist_ok=True)

    # Run through each individual_conf#.sdf, get the molecule name and assign it a unique number identifier, rename the file with the unique name and append the file to a confs file with the unique name
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.startswith("individual_conf") and file.endswith(".sdf"):
                # Get the first line of the file, which has the molecule name
                with open(file, "r") as read_file:
                    molecule_name = read_file.readline().strip("\n")
                    if not molecule_name:
                        continue

                    # Add molecule name to molecule name dict if not present (with count of 1), otherwise increment 1 to the count
                    if molecule_name not in molecule_name_dict:
                        molecule_name_dict[molecule_name] = 1
                    else:
                        molecule_name_dict[molecule_name] += 1

                    unique_name = f"{molecule_name}_{molecule_name_dict[molecule_name]}"

                    # Re-write the file with the unique number identifier after it in the name (also name the file with it)
                    with open(unique_name + ".sdf", "w") as write_file:
                        write_file.write(unique_name + "\n")
                        read_file.seek(0)
                        next(read_file)  # Skip the first line (already written)
                        for line in read_file:
                            write_file.write(line)

                    # Append the written file with the updated name to a master confs list
                    with open("confs_named.sdf", "a") as master_confs:
                        with open(unique_name + ".sdf", "r") as unique_file:
                            master_confs.write(unique_file.read())

                    # Append the unique name to a file list for being able to access file names when we do stuff with shape.db/VAMS
                    with open(f"{starting_file_no_ext}_lig_name_list.txt", "a") as name_list:
                        name_list.write(unique_name + "\n")

                    # Make a params file of the unique file
                    subprocess.run(["python3", "/conformator_for_container/molfile_to_params.py", unique_name + ".sdf", "-n", unique_name, "--keep-names", "--long-names", "--clobber", "--no-pdb"])

                    # Move the sdf and param to their own folders
                    subprocess.run(["mv", unique_name + ".sdf", "single_conf_sdfs"])
                    subprocess.run(["mv", unique_name + ".params", "single_conf_params"])

                    # Delete the individual_conf#.sdf since we don't need it and have a better copy with the unique name sdf
                    os.remove(file)

    # Remove confs.sdf since we have built confs_named.sdf
    os.remove("confs.sdf")

    os.chdir("..")

    # Tar confs_named, single_conf_sdfs, and single_conf_params
    subprocess.run(["tar", "-czvf", f"{starting_file_no_ext}.tar.gz", starting_file_no_ext])
    subprocess.run(["rm", "-dr", starting_file_no_ext])


# Iterate over each file in the input directory
for sdf_file in os.listdir(input_directory):
    if sdf_file.endswith(".sdf"):
        process_sdf(os.path.join(input_directory, sdf_file))
