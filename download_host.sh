#下载bacteria,
## 使用biopython Entrez接口
HOST_DB=$PWD/db/host
SCRIPTS=$PWD/scripts
# ID_TXT="$PWD/data/VHDB_host_gcf.txt"
SUCCESS_TXT=$PWD/VHDB_host_downloaded.txt
ERROR_TXT=$PWD/VHDB_host_download_error.txt
LOG=$PWD/VHDB_host_download.log
ALL_NUM=$(cut -f 1 ${ID_TXT}|uniq|wc -l)
COUNT=0
for GCF in $(cut -f 1 ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    if [ $(grep ${GCF} VHDB_host_downloaded.txt) ];then
        continue
    else
        echo ${GCF} >> ${LOG}
        python ${SCRIPTS}/ncbi_host_download.py  ${GCF}  ${HOST_DB}/${GCF}
        
        if [ $? -ne 0 ];then
            #如果下载成功放入SUCCESS_TXT，如果下载不成功放入ERROR_TXT
            echo ${GCF} >> ${ERROR_TXT}
        else
            echo ${GCF} >> ${SUCCESS_TXT}
        fi
    fi
done
echo "end"



## 使用ncbi-genome-download
# HOST_DB=$PWD/db/host
# ID_TXT="$PWD/data/virushostdb(non_scaffold)_id_host.txt"
# SUCCESS_TXT=$PWD/VHDB_host_downloaded.txt
# ERROR_TXT=$PWD/VHDB_host_download_error.txt
# LOG=$PWD/download_gcf.log
# ALL_NUM=$(cut -f 1 ${ID_TXT}|uniq|wc -l)
# COUNT=0

# for GCF in $(cut -f 1 ${ID_TXT}|uniq);do
#     let COUNT++
#     printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
#     if [ $(grep ${GCF} VHDB_host_downloaded.txt) ];then
#         continue
#     else
#         # rm -rf ${PHAGE_DB}/${PHAGE_ID}
#         echo ${GCF} >> ${LOG}
#         ncbi-genome-download --assembly-accessions ${GCF}  all --flat-output --formats protein-fasta --output-folder ${HOST_DB}
#         ncbi-genome-download --assembly-accessions ${GCF}  all --flat-output --formats fasta --output-folder ${HOST_DB}
#         ncbi-genome-download --assembly-accessions ${GCF}  all --flat-output --formats gff --output-folder ${HOST_DB}
        
#         if [ $? -ne 0 ];then
#             #如果下载成功放入SUCCESS_TXT，如果下载不成功放入ERROR_TXT
#             echo ${GCF} >> ${ERROR_TXT}
#         else
#             echo ${GCF} >> ${SUCCESS_TXT}
#         fi
#     fi
# done
# echo "end"


HOST_DB=$PWD/db/gcf
SCRIPTS=$PWD/scripts
ID_TXT="$PWD/phage_gcf.txt"
SUCCESS_TXT=$PWD/VHDB_host_downloaded.txt
ERROR_TXT=$PWD/VHDB_host_download_error.txt
LOG=$PWD/VHDB_host_download.log
ALL_NUM=$(cut -f 1 ${ID_TXT}|uniq|wc -l)
COUNT=0
for GCF in $(cut -f 1 ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    if [ $(grep ${GCF} VHDB_host_downloaded.txt) ];then
        continue
    else
        echo ${GCF} >> ${LOG}
        python ${SCRIPTS}/ncbi_host_download.py  ${GCF}  ${HOST_DB}/${GCF}
        
        if [ $? -ne 0 ];then
            #如果下载成功放入SUCCESS_TXT，如果下载不成功放入ERROR_TXT
            echo ${GCF} >> ${ERROR_TXT}
        else
            echo ${GCF} >> ${SUCCESS_TXT}
        fi
    fi
done
echo "end"
