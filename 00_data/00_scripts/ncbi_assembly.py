from Bio import Entrez
from datetime import datetime


Entrez.email = "270992395@qq.com"
def name_to_gcfs(term):
    term=term.replace('(',' ').replace(')',' ')
    #provide your own mail here
    
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
    # retmax ???????????????????????????????????????
    handle = Entrez.esearch(db="assembly", term=term, retmax='200')
    record = Entrez.read(handle)
    ids = record['IdList']
    return ids


def get_gcf_dict(ids):
    """
    ?????????????????????date???GCF????????????
    {'GCF_000008865.2': '2018/10/04 00:00', 'GCF_000005845.2': '2013/11/06 00:00'}
    """
    gcf_dict = {}
    # print(ids)
    # ?????????complete genome???????????????Chromosome genome
    complete_flag=0
    for id in ids:
        # print(summary)
        try:
            summary = get_assembly_summary(
                id)['DocumentSummarySet']['DocumentSummary'][0]
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
    host_name = "Shewanella"
    gcf_info = name_to_gcfs(host_name)
    print(host_name)
    print(gcf_info)
    
    # get_gcf_dict([42708])
    """Test
    Escherichia coli :?????????reference?????????
    Vibrio natriegens :???1???Representative?????????
    Mycobacterium smegmatis mc2 155 : ??????Representative???reference?????????,???3????????????
    Streptomyces scabiei RL-34 ?????????host name????????????assembly???,?????????Streptomyces scabiei?????????representative genomes

    Bacillus alcalophilus CGMCC 1.3604 ?????????host name????????????assembly,???????????????complete genome ?????????representative genome???Assembly level???Scaffold
    Providencia stuartii isolate MRSN 2154 ??????ValueError: time data '1/01/01 00:00' does not match format '%Y/%m/%d %H:%M', 
    ????????????Providencia stuartii GCA_018128385.1?????????AsmReleaseDate_RefSeq???????????????
    Candidatus Hamiltonella defensa 5AT (Acyrthosiphon pisum) ????????????????????????????????????????????????

    Acholeplasma laidlawii represent genome???scaffold????????????????????????unreference genome???complete genome???????????????????????????scaffold level?????????scaffold?????????????????????
    Arthrobacter sp. ATCC 21022 ????????????anomalous genome???????????????AND (NOT anomalous[filter])
    Cronobacter turicensis z3032 ????????????GCF_000027065.2 (suppressed)
    Planktothrix agardhii HAB637 ??????['GCA_003609755.1', 'GCF_000710505.1']???GCA??????GCF???????????????->???????????????(['GCF_000710505.1'], 'Unreference', 'Chromosome')
    """
