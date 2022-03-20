from Bio import Entrez
from datetime import datetime


# def name_to_gcfs(term):
#     """Download genbank assemblies for a given search term.
#     【脚本逻辑】reference genome 优先：
#     先根据host name找reference genome，
#     如果没有则找representative genome，
#     如果还没有就不加其他筛选关键词，
#     默认筛选关键词为"complete genome"[All Fields] 。
#     鉴于可能会返回多个gcf，将得到的gcf根据时间顺序排列，最新的gcf在最前面

#     """
#     try_times = 0
#     while try_times<10:
#         try:
#             gcfs,level=main_function(term)
#         except:
#             try_times += 1
#             continue
#         else:
#             return gcfs,level
#     gcfs=['-']
#     level='-'
#     return


def name_to_gcfs(term):
    #provide your own mail here
    Entrez.email = "achuan-2@outlook.com"
    term += ' (AND "complete genome"[All Fields] OR "chromosome level"[filter] OR "scaffold level"[filter])'
    refer_term = term + ' AND "reference genome"[filter]'
    ids = search_assembly(refer_term)
    if ids:
        # print('Found {} reference genomes'.format(len(ids)))
        # return ids
        gcfs,assembly_level = get_gcf(ids)
        category = "Reference"
    else:
        # print('No reference genomes found')
        represent_term = term + ' AND "representative genome"[filter]'
        ids = search_assembly(represent_term)
        # print(ids)
        if ids:
            # print('Found {} representative genomes'.format(len(ids)))
            gcfs,assembly_level = get_gcf(ids)
            category = "Represent"
        else:
            # complete_term =term+ ' AND "complete genome"[All Fields]'
            ids = search_assembly(term)
            gcfs, assembly_level = get_gcf(ids)
            category = "Unreference" if gcfs else "-"
            # if ids:
            #     chromosome_term = term+ ' AND "chromosome level"[filter]'
            #     ids = search_assembly(chromosome_term)
            #     gcfs = get_gcf(ids)
            #     level = "complete"if gcfs else "-"
    return gcfs, category, assembly_level


def search_assembly(term):
    """Search NCBI assembly database for a given search term.
    Args:
        term: search term, usually organism name
    """
    # retmax 代表搜的结果展示的最大数量
    handle = Entrez.esearch(db="assembly", term=term, retmax='200')
    record = Entrez.read(handle)
    ids = record['IdList']
    return ids


def get_gcf_dict(ids):
    """
    难点：如何根据date对GCF进行排序
    {'GCF_000008865.2': '2018/10/04 00:00', 'GCF_000005845.2': '2013/11/06 00:00'}
    """
    gcf_dict = {}
    # print(ids)
    # 如果有complete genome，就不返回Chromosome genome
    complete_flag=0
    for id in ids:
        summary = get_assembly_summary(id)
        assembly_level=summary['DocumentSummarySet']['DocumentSummary'][0]['AssemblyStatus']

        accession = summary['DocumentSummarySet']['DocumentSummary'][0]['AssemblyAccession']
        update_time = summary['DocumentSummarySet']['DocumentSummary'][0]['AsmReleaseDate_RefSeq']
        try:
            update_time= datetime.strptime(
                update_time, '%Y/%m/%d %H:%M')
        except:
            update_time = datetime.strptime(
                "1990/01/01 01:00", '%Y/%m/%d %H:%M')
        assembly_dict={'Complete Genome':2,'Chromosome':1,'Scaffold':0}
        assembly_order=assembly_dict.get(assembly_level,0)
        if assembly_order:
            complete_flag=1 
        gcf_dict[accession] = {'update_time': update_time, 'assembly_level': assembly_level,'assembly_order':assembly_order}
    if complete_flag:
        gcf_dict = {key:gcf_dict[key] for key in gcf_dict if gcf_dict[key]['assembly_level'] == 'Complete Genome'}
    gcf_dict = dict(sorted(gcf_dict.items(), key=lambda x: (x[1]['assembly_order'],x[1]['update_time']), reverse=True))
    return gcf_dict
def get_gcf(ids):

    sort_dict=get_gcf_dict(ids)
    if sort_dict:
        for key, value in sort_dict.items():
            assembly_level=sort_dict[key]['assembly_level']
            break
        gcfs = [i for i in sort_dict]
    else:
        gcfs = []
        assembly_level='-'
    return gcfs, assembly_level

def get_assembly_url(id):
    summary = get_assembly_summary(id)
    url = summary['DocumentSummarySet']['DocumentSummary'][0]['FtpPath_RefSeq']
    return url


def get_assembly_summary(id):
    """Get esummary for an entrez id"""
    esummary_handle = Entrez.esummary(
        db="assembly", id=id, report="full", validate=False)
    esummary_record = Entrez.read(esummary_handle)
    return esummary_record


if __name__ == "__main__":
    host_name = "Alkalihalobacillus alcalophilus"
    gcf_info = name_to_gcfs(host_name)
    print(host_name)
    print(gcf_info)
    """Test
    Escherichia coli :有两个reference基因组
    Vibrio natriegens :有1个Representative基因组
    Mycobacterium smegmatis mc2 155 : 没有Representative和reference基因组,有3个基因组
    Streptomyces scabiei RL-34 直接靠host name是得不到assembly的,但是用Streptomyces scabiei能得到representative genomes

    Bacillus alcalophilus CGMCC 1.3604 直接靠host name是得不到assembly,发现是没有complete genome ，但有representative genome，Assembly level是Scaffold
    Providencia stuartii isolate MRSN 2154 报错ValueError: time data '1/01/01 00:00' does not match format '%Y/%m/%d %H:%M', 
    原来这个Providencia stuartii GCA_018128385.1这个的AsmReleaseDate_RefSeq字段有问题
    """
