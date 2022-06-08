import json
import pandas as pd
from collections import Counter


df_info = pd.read_table("../virushostdb_output(filtered).tsv", sep='\t')

# df_info to dict
virus_dict = {}
for i in range(len(df_info)):
    virus_ids = df_info.iloc[i, 1]
    virus_ids = virus_ids.replace('(', ',').replace(')', '')
    for virus_id in virus_ids.split(','):
        virus_id = virus_id.strip()
        host_num = 1
        virus_name = df_info.iloc[i, 0]
        virus_taxid = str(df_info.iloc[i, 2])
        virus_lineage=df_info.iloc[i, 3]
        host_info = {
            'host_name': df_info.iloc[i, 5],
            'host_taxid': str(df_info.iloc[i, 6]),
            'host_lineage': df_info.iloc[i, 7],
            'host_taxrank': df_info.iloc[i, 8],
            }
        if virus_id not in virus_dict:
            virus_dict[virus_id] = {
                'virus_name': virus_name,
                'virus_taxid': virus_taxid,
                'virus_lineage': virus_lineage,
                'host_num': host_num, 'host_info': [host_info]}
        else:
            virus_dict[virus_id]['host_num'] += 1
            virus_dict[virus_id]['host_info'].append(host_info)
# 初始化一个字典，用来存放每个索引的taxonomy level
taxonomy_level = {6: 'species', 5: 'genus',
                4: 'family', 3: 'order', 2: 'class', 1: 'phylum', 0: 'kingdom'}
for virus_id in virus_dict:
    lca_flag = False
    virus_info = virus_dict[virus_id]
    host_num = virus_info['host_num']
    virus_dict[virus_id]['lca_info'] = {}
    virus_dict[virus_id]['most_common_taxonomy'] = {'kingdom': None, 'phylum': None, 'class': None,
                                                    'order': None, 'family': None, 'genus': None, 'species': None}
    virus_dict[virus_id]['purity'] = {'kingdom': None, 'phylum': None, 'class': None,
                                    'order': None, 'family': None, 'genus': None, 'species': None}
    # 先把每个病毒的host lineage合并为表格，方便后面统计
    lineage_list = [host_info['host_lineage']
                    for host_info in virus_info['host_info']]
    # 从右往左数，获取各个层级的最多相同次数，一旦哪个最多相同次数为host num数就是LCA level
    for i in taxonomy_level.keys():
        taxonomy_list = sorted([lineage.split(';')[i].split('__')[1]
                                for lineage in lineage_list], reverse=True)  # reverse=True表示为了让空的排后面

        maxcounttax = Counter(taxonomy_list).most_common(1)[0][0]
        maxcount = Counter(taxonomy_list).most_common(1)[0][1]
        # 计算purity
        purity = round(maxcount / host_num*100, 2)
        level = taxonomy_level[i]
        virus_dict[virus_id]['purity'][level] = purity
        # 保存maxcounttax
        virus_dict[virus_id]['most_common_taxonomy'][level] = maxcounttax
        # 计算lca
        if not lca_flag and maxcount == host_num and maxcounttax:
            lca_level = taxonomy_level[i]
            lca_name = maxcounttax
            lca_lineage = ';'.join(lineage_list[0].split(';')[:i+1])
            lca_flag = True

    # 把LCA 信息补充放入字典
    virus_dict[virus_id]['lca_info']['lca_level'] = lca_level
    virus_dict[virus_id]['lca_info']['lca_name'] = lca_name
    virus_dict[virus_id]['lca_info']['lca_lineage'] = lca_lineage

for virus_id in virus_dict:
    virus_info = virus_dict[virus_id]
    virus_info['split_lineage'] = {'kingdom': [], 'phylum': [
    ], 'class': [], 'order': [], 'family': [], 'genus': [], 'species': []}
    # 先把每个病毒的host lineage合并为表格，方便后面统计
    lineage_list = [host_info['host_lineage']
                    for host_info in virus_info['host_info']]
    for i, level in taxonomy_level.items():
        virus_info['split_lineage'][level] = list(set(
            sorted([lineage.split(';')[i].split('__')[1] for lineage in lineage_list], reverse=True)))
# save to json
with open('../gold_virus_info.json', 'w') as f:
    json.dump(virus_dict, f, indent=4)
