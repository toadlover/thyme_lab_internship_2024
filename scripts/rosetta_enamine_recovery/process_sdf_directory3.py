import os
import subprocess

# Paths
conformator_path = "/pi/summer.thyme-umw/2024_intern_lab_space/conformator_1.2.1/conformator"
sdf_directory = "/home/raheel.sarwar-umw/SDF-Folder-12"
output_sdf_directory = os.path.join(sdf_directory, "Processed-SDFs")
params_directory = os.path.join(sdf_directory, "Params-Files")
molfile_to_params_script = "/pi/summer.thyme-umw/2024_intern_lab_space/rosetta/source/scripts/python/public/molfile_to_params.py"  # Update this path

# Ensure output directories exist
os.makedirs(output_sdf_directory, exist_ok=True)
os.makedirs(params_directory, exist_ok=True)

# Function to process each SDF file
def process_sdf(starting_file):
    # Extract filename without extension
    starting_file_no_ext = os.path.splitext(os.path.basename(starting_file))[0]
    
    print(f"Processing file: {starting_file}")

    # Run conformator on the starting file
    result = subprocess.run([conformator_path, "-i", starting_file, "-o", f"{output_sdf_directory}/confs.sdf", "--keep3d", "--hydrogens", "-n", "15"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

    # Check if confs.sdf was created
    if not os.path.exists(f"{output_sdf_directory}/confs.sdf"):
        print(f"Error: confs.sdf was not created for {starting_file}")
    else:
        print(f"confs.sdf created for {starting_file}")

        # Move confs.sdf to the current file's directory
        os.rename(f"{output_sdf_directory}/confs.sdf", f"{output_sdf_directory}/{starting_file_no_ext}_confs.sdf")

        # Use babel to break the confs.sdf file into individual sdf files
        result = subprocess.run(["obabel", f"{output_sdf_directory}/{starting_file_no_ext}_confs.sdf", "-O", f"{output_sdf_directory}/{starting_file_no_ext}_conf.sdf", "-m"], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)

        # Convert individual conformer SDF files to .params files
        for sdf_file in os.listdir(output_sdf_directory):
            if sdf_file.startswith(f"{starting_file_no_ext}_conf") and sdf_file.endswith(".sdf"):
                sdf_path = os.path.join(output_sdf_directory, sdf_file)
                params_path = os.path.join(params_directory, os.path.splitext(sdf_file)[0] + ".params")
                
                # Call molfile_to_params.py script
                result = subprocess.run(["python", molfile_to_params_script, "--no-pdb", "--clobber", sdf_path], capture_output=True, text=True)
                print(result.stdout)
                print(result.stderr)
                
                # Move the generated params file to the params directory and rename it
                if os.path.exists("LG.params"):
                    os.rename("LG.params", params_path)

# Main script to process all SDF files in the directory
if __name__ == "__main__":
    # Loop through each SDF file in sdf_directory
    for sdf_file in os.listdir(sdf_directory):
        if sdf_file.endswith(".sdf") and not sdf_file.startswith("confs"):
            starting_file = os.path.join(sdf_directory, sdf_file)
            process_sdf(starting_file)

print("Processing of SDF files is complete.")
