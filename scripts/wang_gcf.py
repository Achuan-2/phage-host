import pandas as pd
from soupsieve import match
from ncbi_assembly import name_to_gcfs
from ncbi_utils import simplify_name
from tqdm import tqdm
def main():
    input="../data/wang_train_pairs.csv"
    output_f=open("../data/wang_train_pairs_output.tsv",mode="w",encoding="utf-8")
    # host_gcfs=[]
    # find_names=[]
    num_lines = sum(1 for line in open(input, 'r'))-1
    header = ['viral_acc', 'virus_name', 'report_host',
            'matched_name', 'find_name','gcfs', 'new_gcf','assembly_category', 'assembly_level']
    output_f.write("\t".join(header)+"\n")
    output_f.flush()
    with open(input, mode='r', encoding='utf-8') as f:
        f.readline()
        for line in tqdm(f, total=num_lines):
            # 尝试直接根据name获得host gcf
            viral_acc, virus_name, report_host,matched_name = line.strip().split(",")
            find_name = matched_name
            gcfs, assembly_category,assembly_level = name_to_gcfs(find_name)
            # 如果获取不到则进入尝试精简搜索
            while not gcfs:
                name_temp = simplify_name(find_name)
                if name_temp==find_name:
                    break
                find_name=name_temp
                gcfs, assembly_category, assembly_level = name_to_gcfs(find_name)
            # 如果还是获取不到则返回-
            if not gcfs:
                gcfs=['-']
                find_name='-'
                assembly_category='-'
                assembly_level='-'
            # host_gcfs.append(gcfs)
            # find_names.append(find_name)
            new_gcf=gcfs[0]
            data_list = [viral_acc, virus_name, report_host,matched_name,
                        find_name, gcfs, new_gcf,assembly_category, assembly_level]
    
            output_f.write("\t".join(str(i) for i in data_list)+"\n")
            output_f.flush()
        #     print(gcfs)
        # df["host_gcfs"]=host_gcfs
        # df["find_name"]=find_names


if __name__ == "__main__":
    main()
