import pandas as pd
import numpy as np

def summary(df_score):
    summary_dict = {'species': {}, 'genus': {}}
    summary_dict['species'] = {"病毒数目": len(df_score['virus'].unique()), "宿主数目": len(
        df_score['host'].unique()), '总样本': len(df_score),  "正样本": sum(df_score['species_tag'] == 1), "负样本": sum(df_score['species_tag'] == 0),
        "正确率": 0,
        "找到正确宿主的病毒": len(df_score.loc[df_score['species_tag'] == 1, 'virus'].unique()),
    }
    summary_dict['genus'] = {'总样本': len(df_score), "病毒数目": len(df_score['virus'].unique()), "宿主数目": len(
        df_score['host'].unique()), "正样本": sum(df_score['genus_tag'] == 1), "负样本": sum(df_score['genus_tag'] == 0),
        "正确率": 0,
        "找到正确宿主的病毒": len(df_score.loc[df_score['genus_tag'] == 1, 'virus'].unique()),
    }
    # summary_dict to df
    df_summary = pd.DataFrame(summary_dict)
    df_summary = df_summary.T.copy()
    df_summary['正确率'] = round(
        df_summary['正样本']/(df_summary['正样本']+df_summary['负样本']), 4)
    df_summary['病毒Recover-in'] = round(
        df_summary['找到正确宿主的病毒']/df_summary['病毒数目'], 4)
    df_summary['病毒Recover-all'] = round(
        df_summary['找到正确宿主的病毒']/4295, 4)
    return df_summary


def highest_host(df_score):
    df_score["rank"] = df_score.groupby("virus")["score"].rank(
        method="min", ascending=False).astype(np.int64)
    df_only = df_score[df_score["rank"] == 1]
    return df_only


def species_tag(df):
    host_id = df['host']
    virus_id = df['virus'].split('.')[0]
    host_taxonomy = host_lineage_dict[host_id].split(';')[6]
    virus_taxonomy_list = virus_host_dict[virus_id]['split_lineage']["species"]
    if host_taxonomy in virus_taxonomy_list:
        return 1
    else:
        return 0


def genus_tag(df):
    host_id = df['host']
    virus_id = df['virus'].split('.')[0]
    host_taxonomy = host_lineage_dict[host_id].split(';')[5]
    virus_taxonomy_list = virus_host_dict[virus_id]['split_lineage']["genus"]
    if host_taxonomy in virus_taxonomy_list:
        return 1
    else:
        return 0


def add_tag(df_score):
    df_score['species_tag'] = df_score.apply(lambda x: species_tag(x), axis=1)
    df_score['genus_tag'] = df_score.apply(lambda x: genus_tag(x), axis=1)
    return df_score

def mkdir(path):
    import os
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False