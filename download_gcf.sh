# 下载bacteria
HOST_DB=$PWD/db/host
ID_TXT=host_gcf.txt
cut -f 10 virushostdb_phage2.tsv |tail -n+2 | uniq > ${ID_TXT}
PROCESS_TXT=VHDB_host_downloaded.txt
ALL_NUM=$(cut -f 1 ${ID_TXT}|uniq|wc -l)
COUNT=0

for GCF in $(cut -f 1 ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    # rm -rf ${PHAGE_DB}/${PHAGE_ID}
    ncbi-genome-download --assembly-accessions ${GCF}  all --flat-output --formats protein-fasta --output-folder ${HOST_DB}
    ncbi-genome-download --assembly-accessions ${GCF}  all --flat-output --formats fasta --output-folder ${HOST_DB}
    echo ${GCF} >> ${PROCESS_TXT}
done
echo "end"
