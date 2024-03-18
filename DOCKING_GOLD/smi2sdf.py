import argparse
import copy
import multiprocessing as mp
import os
import pickle
import random
import string
import subprocess
#partial function
from functools import partial

import numpy as np
import tqdm
from rdkit import Chem
from rdkit.Chem import QED, AllChem, RDConfig
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem.rdForceFieldHelpers import UFFOptimizeMolecule
from rdkit.Chem.rdMolAlign import CalcRMS
from rdkit.Geometry import Point3D

def gen_conformation(mol, num_conf=20, num_worker=8, prune_rmsd=2):

    mol = Chem.AddHs(mol)
    AllChem.EmbedMultipleConfs(mol, numConfs=num_conf, numThreads=num_worker, pruneRmsThresh=prune_rmsd, maxAttempts=500, useRandomCoords=False)
    if mol.GetNumConformers() == 0:
        return None
    return mol

def gen_conformation_sdf(smi,ligand_name,num_conf=20, num_worker=8, prune_rmsd=2, tmp_dir='tmp'):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None
    mol = gen_conformation(mol, num_conf=num_conf, num_worker=num_worker, prune_rmsd=prune_rmsd)
    if mol is None:
        return None
    sdf_path = os.path.join(tmp_dir,  f'{ligand_name}.sdf')
    writer = Chem.SDWriter(sdf_path)
    for i in range(mol.GetNumConformers()):
        writer.write(mol, confId=i)
    writer.close()
    return sdf_path

