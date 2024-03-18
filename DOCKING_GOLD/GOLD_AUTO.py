import os
from gold_docking import GOLD_docking
from read_smi import read_smi
from read_lst import SELECT_pose
import tqdm

def MAIN_MISSION (args,num_worker=4):
    file_path,_protein_name,_lig_file,_ligand_path = args
    # 对smiles文件进行预处理
    read_smi(file_path)
    # 进行docking
    GOLD_docking(ligand_path = _ligand_path,
                protein_name = _protein_name,
                protein_path = file_path,
                output_path= file_path,
                lig_file = _lig_file)
    # 对于每一个docking的protein-ligand的pair筛选出top4的结果
    SELECT_pose(file_path,top=3)
    
if __name__ == '__main__':
    num_workers = 16
    args_list = []
    DATA_PATH = '/data4msa/hd1/ChEMBL/ChEMBL_dataset_v2'
    # 切换至工作文件夹
    os.chdir(DATA_PATH)
    DATAS = os.listdir(DATA_PATH)
    #DATAS[0] = 'P00669' ; DATAS[1] = 'P09211' 测试用
    for data in DATAS:
        data_newpath1 = os.path.join(DATA_PATH,data)
        files = os.listdir(data_newpath1)
        for file in files:
            file_path = os.path.join(data_newpath1,file)
            # 切换至最底层工作路径
            os.chdir(file_path)
            # 获取蛋白质名称
            all = os.listdir(file_path)
            _protein_name = ''
            for f in all:
                if f.endswith('_rmW.pdb'):
                    # 获取protein的name
                    _protein_name = f
                if f.endswith('_ligand.pdb'):
                    # 获取lig_file的name
                    _lig_file = f
            if _protein_name.endswith('_rmW.pdb'):
                continue 
            # 获取配体路径
            _ligand_path = os.path.join(file_path,'GOLD_ligands') # 约定为此名称
            args = (file_path,_protein_name,_lig_file,_ligand_path)
            args_list.append(args)
    
    results = []
    if num_workers > 1:
        import _multiprocessing as mp
        pool = mp.Pool(num_workers)
        for result in tqdm.tqdm(pool.imap_unordered(MAIN_MISSION, args_list), total=len(args_list)):
            results.append(result)
     