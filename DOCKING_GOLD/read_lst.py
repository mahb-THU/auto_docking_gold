import re
import os
import json
import shutil
    
def SELECT_pose(home_path,top=3):
    rnk_datas = []
    output_path = os.path.join(home_path,'GOLD_dockfiles')
    rnk_list = []
    os.chdir(output_path)
    datas = os.listdir(output_path)
    for data in datas:
        if os.path.splitext(data)[1] == '.rnk' and data is not None:
            rnk_list.append(data)
    for rnk_file in rnk_list:
        rnk_path = os.path.join(output_path,rnk_file)
        file = open(rnk_path,'r')
        lines = file.readlines()
        file.close()
        start_index = 4
        if len(lines) <= (top + 9):
            end_index = len(lines) - 5
            lines = lines[:end_index]
            lines = lines[start_index:]
        else:
            end_index = top + 4
            lines = lines[:end_index]
            lines = lines[start_index:]
        dic = {}
        ligand_name = os.path.splitext(rnk_file)[0]
        for line in lines:
            result = line.split()
            key = 'gold_soln_'+ligand_name+'_'+result[0]+'.sdf'
            value = result[1]
            dic[key] = value
            newdic = {}
            key = ligand_name
            value = dic
            newdic[key] = value
        rnk_datas.append(newdic)
    os.chdir(home_path)
    try:
        os.mkdir('GOLD_docked_pdb') # 约定：所有文件下均为此名称
    except:
        pass
    data_path = os.path.join(home_path,'GOLD_docked_pdb') #约定：所有文件下均为此名称
    os.chdir(data_path)
    with open("data.json","w",encoding="utf-8") as f:
        json.dump(rnk_datas,f,indent=2,ensure_ascii=False)
    for rnk_data in rnk_datas:
        for key ,value in rnk_data.items():
            os.chdir(data_path)
            try:
                os.mkdir(key)
            except:
                pass
            new_path = os.path.join(data_path,key)
            os.chdir(output_path)
            for keys in value.keys():
                try:
                    shutil.copy(keys,new_path)
                except:
                    pass
            os.chdir(data_path)




