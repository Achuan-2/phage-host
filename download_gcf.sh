# 下载bacteria
HOST_DB=$PWD/db/host
ID_TXT="$PWD/data/virushostdb(non_scaffold)_id_host.txt"
SUCESS_TXT=$PWD/VHDB_host_downloaded.txt
ERROR_TXT=$PWD/VHDB_host_download_error.txt
LOG=$PWD/download_gcf.log
ALL_NUM=$(cut -f 1 ${ID_TXT}|uniq|wc -l)
COUNT=0

for GCF in $(cut -f 1 ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    if [ $(grep ${GCF} VHDB_host_downloaded.txt) ];then
        continue
    else
        # rm -rf ${PHAGE_DB}/${PHAGE_ID}
        echo ${GCF} >> ${LOG}
        ncbi-genome-download --assembly-accessions ${GCF}  all --flat-output --formats protein-fasta --output-folder ${HOST_DB}
        ncbi-genome-download --assembly-accessions ${GCF}  all --flat-output --formats fasta --output-folder ${HOST_DB}
        ncbi-genome-download --assembly-accessions ${GCF}  all --flat-output --formats gff --output-folder ${HOST_DB}
        
        if [ $? -ne 0 ];then
            #如果下载成功，如果下载不成功
            echo ${GCF} >> ${ERROR_TXT}
        else
            echo ${GCF} >> ${SUCESS_TXT}
        fi
    fi
done
echo "end"

