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

"""


from fileinput import filename
from Bio import Entrez
import sys
import os




Entrez.email = "achuan-2@outlook.com"
def main():

    mode = sys.argv[1]
    i = sys.argv[2].strip()
    output = sys.argv[3].strip()
    mkdir(output)
    if mode == 'faa':
        filename = output+'/'+i + '.faa'
        if os.path.exists(filename):
            return
        text=download_faa(i)
        writefile(filename, text)
    elif mode == 'fna':
        filename = output+'/'+i + '.fna'
        if os.path.exists(filename):
            return
        text=download_fna(i)
        writefile(filename, text)
    else:
        pass


def download_fna(i):
    try:
        handle = Entrez.efetch(db="nuccore", id=i, rettype="fasta")
        text = handle.read()
    except:
        print("Error:", i)
    return text


def download_faa(i):
    try:
        handle = Entrez.efetch(db="nuccore", id=i, rettype="fasta_cds_aa")
        text = handle.read()
    except:
        print("Error:", i)
    return text

def download_gb(i):
    handle = Entrez.efetch(db="nuccore", id=i, rettype="gb")
    text = handle.read()
    return text


def writefile(filename, text):
    file = open(filename, mode='w', encoding='utf-8')
    file.write(text)
    file.close()


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    main()
