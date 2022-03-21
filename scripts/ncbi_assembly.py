from Bio import Entrez
from datetime import datetime



def name_to_gcfs(term):
    term=term.replace('(',' ').replace(')',' ')
    #provide your own mail here
    Entrez.email = "270992395@qq.com"
    term += ' AND (latest[filter] AND all[filter] NOT anomalous[filter] "refseq has annotation"[Properties])'
    refer_term = term + ' AND ("complete genome"[filter] OR "chromosome level"[filter])   AND "reference genome"[filter]'
    # refer_term = term + ' AND ("complete genome"[filter] OR "chromosome level"[filter]  OR "scaffold level"[filter]) AND "reference genome"[filter]'
    ids = search_assembly(refer_term)
    if ids:
        # print('Found {} reference genomes'.format(len(ids)))
        # return ids
        gcfs,assembly_level = get_gcf(ids)
        category = "Reference"
    else:
        # print('No reference genomes found')
        represent_term = term + \
            ' AND ("complete genome"[filter] OR "chromosome level"[filter] ) AND "representative genome"[filter]'
            # ' AND ("complete genome"[filter] OR "chromosome level"[filter]  OR "scaffold level"[filter]) AND "representative genome"[filter]'
        ids = search_assembly(represent_term)
        # print(ids)
        if ids:
            # print(ids)
            # print('Found {} representative genomes'.format(len(ids)))
            gcfs,assembly_level = get_gcf(ids)
            category = "Represent"
        else:
            # complete_term =term+ ' AND "complete genome"[All Fields]'
            term += ' AND ("complete genome"[filter] OR "chromosome level"[filter])'
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
        summary = get_assembly_summary(
            id)['DocumentSummarySet']['DocumentSummary'][0]
        # print(summary)
        try:
            assembly_level=summary['AssemblyStatus']

            accession = summary['AssemblyAccession']
            update_time = summary['AsmReleaseDate_RefSeq']
            if 'suppressed_refseq' in summary['PropertyList']:
                accession+='(suppressed)'
        except:
            continue
        try:
            update_time= datetime.strptime(
                update_time, '%Y/%m/%d %H:%M')
        except:
            update_time = datetime.strptime(
                "1990/01/01 01:00", '%Y/%m/%d %H:%M')
        assembly_dict={'Complete Genome':2,'Chromosome':1,'Scaffold':0}
        assembly_order=assembly_dict.get(assembly_level,0)
        gcf_dict[accession] = {'update_time': update_time, 'assembly_level': assembly_level,'assembly_order':assembly_order}

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
    esummary_record = Entrez.read(esummary_handle,validate=False)
    return esummary_record


if __name__ == "__main__":
    host_name = "Planktothrix agardhii"
    gcf_info = name_to_gcfs(host_name)
    print(host_name)
    print(gcf_info)
    # get_gcf_dict([42708])
    """Test
    Escherichia coli :有两个reference基因组
    Vibrio natriegens :有1个Representative基因组
    Mycobacterium smegmatis mc2 155 : 没有Representative和reference基因组,有3个基因组
    Streptomyces scabiei RL-34 直接靠host name是得不到assembly的,但是用Streptomyces scabiei能得到representative genomes

    Bacillus alcalophilus CGMCC 1.3604 直接靠host name是得不到assembly,发现是没有complete genome ，但有representative genome，Assembly level是Scaffold
    Providencia stuartii isolate MRSN 2154 报错ValueError: time data '1/01/01 00:00' does not match format '%Y/%m/%d %H:%M', 
    原来这个Providencia stuartii GCA_018128385.1这个的AsmReleaseDate_RefSeq字段有问题
    Candidatus Hamiltonella defensa 5AT (Acyrthosiphon pisum) 意识到要有英文括号的应该换成空格

    Acholeplasma laidlawii represent genome是scaffold的，结果返回的是unreference genome的complete genome，发现是脚本没有把scaffold level写成了scaffold，导致出现问题
    Arthrobacter sp. ATCC 21022 返回的是anomalous genome发现要添加AND (NOT anomalous[filter])
    Cronobacter turicensis z3032 返回的是GCF_000027065.2 (suppressed)
    Planktothrix agardhii HAB637 返回['GCA_003609755.1', 'GCF_000710505.1']，GCA排在GCF前面不合理->改动后输出(['GCF_000710505.1'], 'Unreference', 'Chromosome')
    """
