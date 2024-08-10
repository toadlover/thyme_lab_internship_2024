#/pi/summer.thyme-umw/2024_intern_lab_space/rosetta/source/bin/ligand_discovery_search_protocol.linuxgccrelease @example_rosetta_flags
#example run command on hpc cluster
#first argument is the complete path to the Rosetta ligand_discovery_search_protocol.linuxgccrelease executable
#second argument is to the flags file (which is called with an @ in calling the Rosetta executable, as seen in line 1 of the comments in this file)
#./run.sh /pi/summer.thyme-umw/2024_intern_lab_space/rosetta/source/bin/ligand_discovery_search_protocol.linuxgccrelease example_rosetta_flags
$1 @$2
