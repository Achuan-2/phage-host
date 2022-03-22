import sys
import os
from ncbi_utils import writefile,mkdir
from ncbi_download import download_faa,download_fna,download_gff


def main():

    id = sys.argv[1].strip()
    output = sys.argv[2].strip()
    mkdir(output)
    mode_dict = {'faa': download_faa, 'fna': download_fna,
                'gff3': download_gff}
    for mode in mode_dict:
        func = mode_dict.get(mode)
        filename = f'{output}/{id}.{mode}'
        if os.path.exists(filename):
            continue
        content = func(id)
        while not content:
            content = func(id)
        writefile(filename, content)


if __name__ == "__main__":
    main()

