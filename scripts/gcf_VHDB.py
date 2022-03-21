import pandas as pd
from soupsieve import match
from ncbi_assembly import name_to_gcfs
from ncbi_utils import simplify_name
from tqdm import tqdm



def main():
    input = "../data/virushostdb_phage.tsv"
    output_f = open("../data/virushostdb_phage_output.tsv",
                    mode="w", encoding="utf-8")

    num_lines = sum(1 for line in open(input, 'r'))-1
    header = ['virus_name', 'viral_acc', 'evidence', 'report_host',
            'host_taxid','host_lineage', 'host_tax_rank','find_name', 'gcfs', 'new_gcf', 'assembly_category', 'assembly_level']
    output_f.write("\t".join(header)+"\n")
    output_f.flush()
    host_dict = {}
    with open(input, mode='r', encoding='utf-8') as f:
        f.readline()
        for line in tqdm(f, total=num_lines):
            # 读取一行数据
            virus_name, viral_acc, evidence,report_host, host_taxid, host_lineage, host_tax_rank = line.strip().split("\t")
            if report_host in host_dict:
                find_name = host_dict[report_host]["find_name"]
                gcfs = host_dict[report_host]["gcfs"]
                new_gcf = host_dict[report_host]["new_gcf"]
                assembly_category = host_dict[report_host]["assembly_category"]
                assembly_level = host_dict[report_host]["assembly_level"]
            else:
                # 尝试直接根据name获得host gcf
                find_name = report_host
                gcfs, assembly_category, assembly_level = name_to_gcfs(find_name)
                # 如果获取不到则进入尝试使用上一层级的tax名
                lineage_list=host_lineage.split('; ')
                while not gcfs and lineage_list:
                    find_name = lineage_list.pop(-1)
                    gcfs, assembly_category, assembly_level = name_to_gcfs(
                        find_name)
                # 如果还是获取不到则返回-
                if not gcfs:
                    gcfs = ['-']
                    find_name = '-'
                    assembly_category = '-'
                    assembly_level = '-'
                # host_gcfs.append(gcfs)
                # find_names.append(find_name)
                new_gcf = gcfs[0]
                
                host_dict[report_host]={"find_name":find_name,"gcfs":gcfs,"new_gcf":new_gcf,"assembly_category":assembly_category,"assembly_level":assembly_level}

            data_list = [virus_name, viral_acc,evidence, report_host, host_taxid, host_lineage, host_tax_rank,
                        find_name, gcfs, new_gcf, assembly_category, assembly_level]

            output_f.write("\t".join(str(i) for i in data_list)+"\n")
            output_f.flush()
        #     print(gcfs)
        # df["host_gcfs"]=host_gcfs
        # df["find_name"]=find_names


if __name__ == "__main__":
    main()
