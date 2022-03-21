"""
AB746912.1:{'Nitratiruptor sp. SB155-2': [387092]}，有strain水平的taxi
AJ748296.1:Sulfolobus islandicus LAL14/1，有strain水平的taxi
NC_020479: Bacillus pumilus BL8，有strain水平的taxi
NC_027125：Flavobacterium columnare B185，没有strain水平的taxid,只有species水平的taxid
NC_008583
1. 直接显示phage的host name信息
2. 有host 基因组的taxnomy 层级是多少

lab_host: JQ809701
host: AB746912.1
"""


from ete3 import NCBITaxa
from ncbi_download import download_gb
import re
import requests
from lxml import etree
from tqdm import tqdm


def main():
    print(get_taxid('Streptomyces scabiei RL-34'))
    print(get_taxid('Streptomyces scabiei'))
    # phage_ncid = 'NC_015457'
    # hosts, host_name, taxid, (host_ncid, host_genome_url) = get_host_gcfid(phage_ncid)
    # print(hosts, host_name, taxid, host_ncid, host_genome_url)

    # file2=open('../wang_output.txt','w')
    # input="../wang_train.txt"
    # num_lines = sum(1 for line in open(input, 'r'))
    # with open(input, mode='r', encoding='utf-8') as f:
    #     for line in tqdm(f, total=num_lines):
    #         phage_ncid=line.strip()
    #         try:
    #             hosts, host_name, taxid,(host_ncid, host_genome_url) = get_host_gcfid(phage_ncid)
    #         except:
    #             file2.write(
    #                 f"{phage_ncid},-, -, -,-,-\n")
    #             file2.flush()
    #         else:
    #             file2.write(f"{phage_ncid},{hosts}, {host_name}, {taxid},{host_ncid},{host_genome_url}\n")
    #             file2.flush()


def get_host_gcfid(phage_ncid):
    text = download_gb(phage_ncid)
    hosts = re.findall('(\w+host|host)="(.+)"', text)
    host_dict={source[0]:source[1] for source in hosts}
    hosts = [source[1] for source in hosts]
    print(host_dict)
    # #! 思考下如何同时存在host和labhost的情况
    host_num = len(hosts)
    if host_num:
        name = hosts[0]
        if not get_taxid(name):
            while True:
                name = simplify_name(name)
                if get_taxid(name):
                    host_name, taxid = get_taxid(name)
                    break
        else:
            host_name, taxid = get_taxid(name)
        return host_dict, host_name, taxid, get_ref_gcf(taxid)


def get_taxid(name):
    ncbi = NCBITaxa()
    id = ncbi.get_name_translator([name])
    if id:
        taxid = id[name][0]
        return name,taxid


def simplify_name(name):
    index = name.rfind(' ')
    species=name[0:index]
    return species


def get_ref_gcf(taxid):
    """
    根据taxid获取reference genome的GCF id
    返回的gcf链接
    https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/002/216/815/GCF_002216815.1_ASM221681v1/GCF_002216815.1_ASM221681v1_genomic.fna.gz

    """
    url = 'https://www.ncbi.nlm.nih.gov/genome/?term=txid' + \
        str(taxid) + '[Organism:noexp]'
    res = requests.get(url, timeout=1000)
    html = res.text.encode('utf-8')
    xp = etree.HTML(html)
    try:
        genome_link = xp.xpath(
            '//div[@class="refgenome_sensor"]/span[@class="shifted"][1]/a[1] /@href')[0]
    except:
        return '-', url
    else:
        protein_link = xp.xpath(
            '//div[@class="refgenome_sensor"]/span[@class="shifted"][1]/a[2] /@href')[0]
        gcf_id = genome_link.rsplit('/', 1)[1].rsplit('_', 2)[0]
        return gcf_id, url

def get_assembly_accession(taxid):
    """
    直接根据物种名获取assembly accession
    测试：
    - Mycobacterium smegmatis mc2 155
    - Synechococcus sp. WH8109, 166314

    https://www.ncbi.nlm.nih.gov/assembly/?term="Synechococcus sp. WH 8109"[Organism]AND"complete genome"
    https://www.ncbi.nlm.nih.gov/assembly/?term="Mycobacterium smegmatis mc2 155"[Organism]AND"complete genome"
    """
    url = 'https://www.ncbi.nlm.nih.gov/genome/?term=txid'+str(taxid) +'[Organism:noexp]'
    # print(url)
    res=requests.get(url, timeout=1000)
    html = res.text.encode('utf-8')
    xp = etree.HTML(html)
    table = xp.xpath('//table[@class="GenomeList2"]')
    if table:
        assembly_accession=table[0].xpath('tbody/tr[1]/td[3]/a/text()')[0]
        return assembly_accession,url
    else:
        return '-',url
def get_ref_ncid(taxid):
    """
    根据taxid获取reference genome的ncid
    """
    url = 'https://www.ncbi.nlm.nih.gov/genome/?term=txid'+str(taxid) +'[Organism:noexp]'
    # print(url)
    res=requests.get(url, timeout=1000)
    html = res.text.encode('utf-8')
    xp = etree.HTML(html)
    table = xp.xpath('//table[@class="GenomeList2"]')
    if table:
        ref_ncid=table[0].xpath('tbody/tr[1]/td[3]/a/text()')[0].split('.')[0]
        return ref_ncid,url
    else:
        return '-',url


def get_host_ncid(phage_ncid):
    text = download_gb(phage_ncid)
    hosts = re.findall('host="(.+)"', text)
    #! 思考下如何同时存在host和labhost的情况
    host_num = len(hosts)
    if host_num:
        name = hosts[0]
        if not get_taxid(name):
            while True:
                name = simplify_name(name)
                if get_taxid(name):
                    host_name, taxid = get_taxid(name)
                    break
        else:
            host_name, taxid = get_taxid(name)
        return hosts, host_name, taxid, get_ref_ncid(taxid)
    else:
        return '-', '-', '-', '-', '-'

if __name__=="__main__":
    main()
    # get_ref_gcf(537021)
