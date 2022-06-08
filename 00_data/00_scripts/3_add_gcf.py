from tqdm import tqdm
import json
input = '../virushostdb.daily.phage(filtered).tsv'
fp = open('../report_host.json', 'r')
host_dict = json.load(fp)
num_lines = sum(1 for line in open(input, 'r'))-1
output_f = open("../virushostdb_output.tsv",
                mode="w", encoding="utf-8")
num_lines = sum(1 for line in open(input, 'r'))-1
header = ['virus_name', 'viral_acc', 'virus_taxid', 'virus_lineage', 'evidence', 'report_host',
        'host_taxid', 'host_lineage', 'host_tax_rank', 'find_name', 'gcfs', 'new_gcf', 'assembly_category', 'assembly_level']
output_f.write("\t".join(header)+"\n")
with open(input, mode='r', encoding='utf-8') as f:
    f.readline()
    for line in tqdm(f, total=num_lines):
        virus_name, viral_acc, virus_taxid, virus_lineage, evidence, report_host, host_taxid, host_lineage, host_tax_rank = line.strip().split("\t")
        find_name = host_dict[report_host]["find_name"]
        gcfs = host_dict[report_host]["gcfs"]
        new_gcf = host_dict[report_host]["new_gcf"]
        assembly_category = host_dict[report_host]["assembly_category"]
        assembly_level = host_dict[report_host]["assembly_level"]
        data_list = [virus_name, viral_acc, virus_taxid, virus_lineage,evidence, report_host, host_taxid, host_lineage, host_tax_rank,
                    find_name, gcfs, new_gcf, assembly_category, assembly_level]

        output_f.write("\t".join(str(i) for i in data_list)+"\n")
        output_f.flush()
