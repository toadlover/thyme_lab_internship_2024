#Ari Ginsparg
#6/4/2024
#Schrodinger rmsd calculation script

#usage: run this script from within the scripts/rmsd directory for all location-based operations to work
#run: python schrodinger_rmsd.py

import os,sys

#initial check to ensure that user is running script out of correct directory:
if os.getcwd().endswith("/thyme_lab_internship_2024/scripts/rmsd") == False:
	print("You are not working in the right location for this script to work!")
	print("You are working out of: " + os.getcwd())
	print("You need to work out of .../thyme_lab_internship_2024/scripts/rmsd")
	quit()

#initial declaration of a dictionary to hold all of the rmsd values per system
rmsd_dict = {}

#read through all of the dude ligands and attempt to collect rmsd off of them
#the running of the script makes a difference, as the script won't work if you do not run this script from the right location
for r,d,f in os.walk("../../dude_library_simple/"):
	for dire in d:
		print(dire)