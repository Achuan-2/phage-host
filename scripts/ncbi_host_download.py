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
python ncbi_download.py gff3 KP791807 ./
"""


import sys
import os
import urllib
from Bio import Entrez
from ncbi_assembly import search_assembly, get_assembly_url
from ncbi_utils import mkdir

Entrez.email = "achuan-2@outlook.com"


def main():

    gcf = sys.argv[1].strip()
    output = sys.argv[2].strip()
    mkdir(output)
    download_gcf(gcf, output)


def download_gcf(gcf, output_dir):
    id = search_assembly(gcf)
    url = get_assembly_url(id)
    label = os.path.basename(url)
    fna_link = f'{url}/{label}_genomic.fna.gz'
    ftp_download(fna_link, f'{output_dir}/{gcf}.fna.gz')
    faa_link = f'{url}/{label}_protein.faa.gz'
    ftp_download(faa_link, f'{output_dir}/{gcf}.faa.gz')
    gff_link = f'{url}/{label}_genomic.gff.gz'
    ftp_download(gff_link, f'{output_dir}/{gcf}.gff.gz')


def ftp_download(link, output):
    if os.path.exists(output):
        return
    urllib.request.urlretrieve(link, output)






if __name__ == "__main__":
    main()
    # download_gff("KP791807")
    # download_gcf('GCF_900637085.1', 'GCF_900637085.1')
