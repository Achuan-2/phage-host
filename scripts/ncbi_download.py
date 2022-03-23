"""Usage
PHAGE_DB=$PWD/db/phage
SCRIPTS=$PWD/scripts
ID_TXT=virus.ids.txt
ALL_NUM=$(cut -f 1 ${ID_TXT}|uniq|wc -l)
COUNT=0
for PHAGE_ID in $(cut -f 1 ${ID_TXT}|uniq);do
    python ${SCRIPTS}/ncbi_download.py faa ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
    python ${SCRIPTS}/ncbi_download.py fna ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
done

singe
python ncbi_download.py gb  KP791807 ./
python ncbi_download.py gff3 NC_051678 ./
"""


import sys
import os
import requests
from Bio import Entrez
from Bio import SeqIO

Entrez.email = "achuan-2@outlook.com"


def main():

    mode = sys.argv[1]
    id = sys.argv[2].strip()
    output = sys.argv[3].strip()
    mkdir(output)
    mode_dict = {'faa': download_faa, 'fna': download_fna,
                 'gff': download_gff, 'gb': download_gb}
    func = mode_dict.get(mode, 0)
    if not func:
        print("Error")
        return
    filename = f'{output}/{id}.{mode}'
    if os.path.exists(filename):
        return
    content = func(id)
    if not content:
        return
    writefile(filename, content)


def download_fna(i):
    try:
        handle = Entrez.efetch(db="nuccore", id=i, rettype="fasta")
        content = handle.read()
    except:
        print("Error:", i)
    else:
        return content


def download_faa(i):
    try:
        handle = Entrez.efetch(db="nuccore", id=i, rettype="fasta_cds_aa")
        content = handle.read()
    except:
        print("Error:", i)
    else:
        return content


def download_gb(i):
    try:
        handle = Entrez.efetch(db="nuccore", id=i, rettype="gb")
        content = handle.read()
    except:
        print("Error:", i)
    else:
        return content


def download_gff(id):
    url = f"https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=gff3&id={id}"
    try:
        res = requests.get(url=url)
    except:
        print("Error:", id)
    else:
        content = res.content.decode('utf-8')
        return content


def writefile(filename, content):
    file = open(filename, mode='w', encoding='utf-8')
    file.write(content)
    file.close()


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    main()
    # download_gff("KP791807")
    # download_gcf('GCF_900637085.1', 'GCF_900637085.1')
