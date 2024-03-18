import os
from smi2sdf import gen_conformation_sdf,gen_conformation

def read_smi(smi_path):
    smi = os.path.join(smi_path,'ligands.smi') #'ligands.smi'
    file = open(smi,'r')
    lines = file.readlines()
    file.close()
    os.chdir(smi_path)
    try:
        os.mkdir('GOLD_ligands') # 约定：gold专用的数据处理方式
    except:
        pass 
    ligands_path = os.path.join(smi_path,'GOLD_ligands')
    _count = 0
    for line in lines:
        result = line.split()
        gen_conformation_sdf(smi=result[0],tmp_dir=ligands_path,ligand_name=result[1])
        _count = _count + 1

