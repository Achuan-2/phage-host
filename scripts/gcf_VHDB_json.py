from opcode import opname
import pandas as pd
from soupsieve import match
from ncbi_assembly import name_to_gcfs
from ncbi_utils import simplify_name
from tqdm import tqdm
import  json


def main():
    input = "../data/virushostdb_phage.tsv"

    output_f = open("../data/host.json",
                    mode="r", encoding="utf-8")
    try:
        host_dict = json.load(output_f)
    except:
        host_dict={}

    output_f.close()

    df=pd.read_table(input, sep="\t")
    report_hosts = df['host name']
    host_lineages = df['host lineage']
    host_info=set(zip(report_hosts, host_lineages))
    
    for report_host,host_lineage in tqdm(host_info):
        # 读取一行数据

        if report_host in host_dict:
            continue
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
            with open("../data/host.json", mode="w", encoding="utf-8") as output_f:
                # dumps()方法将dict转化为json格式
                json_str = json.dumps(host_dict, indent=4)
                output_f.write(json_str)
                output_f.flush()


if __name__ == "__main__":
    main()
