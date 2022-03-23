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
    # download_gcf('GCF_900637085.1', 'GCF_900637085.1')
