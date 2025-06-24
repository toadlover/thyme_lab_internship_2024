#the purpose of this script is to derive the rmsd of the alphafold placement rmsd from native
#this will create csv files that note the closest placement to native for the closest of all placements, the closest of the top 10 by confidence, and the closeness of the most confident placement. These files will note the placement as well. A summary csv for the top rmsd will also be made for porting for figure making
#Since the placements are not aligned with the dude library (due to being made by alphafold), we need to align them. The ligand atom indices also do not match, so we will use a heuristic method from rdkit to get rmsd.

#import os,sys
import os,sys
import pymol2
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign
import numpy as np

#this script acts locally, and looks for placement files from alphafold and the native files from DUD-E
this_script_path = os.path.dirname(os.path.abspath(__file__))

#begin a pymol session
with pymol2.PyMOL() as pymol:
	cmd = pymol.cmd

	#iterate over each system in the dude library
	for r,d,f in os.walk(this_script_path + "/../../dude_library_simple"):
		for dire in d:
			print(dire)
