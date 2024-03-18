import os
import numpy as np
import biotite.structure.io.pdb as pdb

def GOLD_docking(ligand_path,protein_name,protein_path,output_path,lig_file=None,center=None):
    #[START]:自动化寻找原子坐标
    assert (lig_file is not None) or (center is not None)
    if lig_file is None:
        x, y, z = center
    else:
        ori_lig = pdb.PDBFile.read(os.path.join(protein_path, lig_file))
        atoms = ori_lig.get_structure()[0]
        x, y, z = np.mean(atoms.coord, axis=0).astype(np.float64)
    #[END]:自动化寻找原子坐标
    # GOLD软件路径
    GOLD_AUTO = '/opt/goldsuite-5.3.0/bin/gold_auto'
    output = os.path.join(output_path,'GOLD_dockfiles') #约定
    try:
        os.mkdir(output)
    except:
        pass
    os.chdir(output)
    lig_conf = os.path.join(output,'gold.conf')
    # 写gold的配置文件  
    with open(lig_conf,'w') as f:
        f.write(
            f'''  GOLD CONFIGURATION FILE

  AUTOMATIC SETTINGS
autoscale = 1

  POPULATION
popsiz = auto
select_pressure = auto
n_islands = auto
maxops = auto
niche_siz = auto

  GENETIC OPERATORS
pt_crosswt = auto
allele_mutatewt = auto
migratewt = auto

  FLOOD FILL
radius = 10
origin = {x} {y} {z}
do_cavity = 0
floodfill_atom_no = 0
cavity_file = 
floodfill_center = point

  DATA FILES''')
    dir = os.listdir(ligand_path) 
    for file in dir:
        with open(lig_conf,'a') as f:
            f.write(
                f'''
ligand_data_file {ligand_path}/{file} 10'''
            )  
    with open(lig_conf,'a') as f:
        f.write(
            f'''
param_file = DEFAULT
set_ligand_atom_types = 1
set_protein_atom_types = 0
directory = .
tordist_file = DEFAULT
make_subdirs = 0
save_lone_pairs = 1
fit_points_file = fit_pts.mol2
read_fitpts = 0

  FLAGS
internal_ligand_h_bonds = 0
flip_free_corners = 0
match_ring_templates = 0
flip_amide_bonds = 0
flip_planar_n = 1 flip_ring_NRR flip_ring_NHR
flip_pyramidal_n = 0
rotate_carboxylic_oh = flip
use_tordist = 1
postprocess_bonds = 1
rotatable_bond_override_file = DEFAULT

  TERMINATION
early_termination = 1
n_top_solutions = 3
rms_tolerance = 1.5

  CONSTRAINTS
force_constraints = 0

  COVALENT BONDING
covalent = 0

  SAVE OPTIONS
save_score_in_file = 1
save_protein_torsions = 1

  FITNESS FUNCTION SETTINGS
initial_virtual_pt_match_max = 3
relative_ligand_energy = 1
gold_fitfunc_path = plp
score_param_file = DEFAULT

  PROTEIN DATA
protein_datafile = {protein_path}/{protein_name}

'''
        )
    # 加载环境变量
    os.system('export LD_LIBRARY_PATH=/opt/goldsuite-5.3.0/c_linux/lib/:/opt/goldsuite-5.3.0/c_linux/lib/CCDC:/opt/goldsuite-5.3.0/c_linux/lib/GCC:/opt/goldsuite-5.3.0/c_linux/lib/qt:/opt/goldsuite-5.3.0/c_linux/lib/MesaGL')
    os.system(f'{GOLD_AUTO} {lig_conf}')

