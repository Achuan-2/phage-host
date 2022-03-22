# 下载phage
PHAGE_DB=$PWD/db/phage
SCRIPTS=$PWD/scripts
ID_TXT="$PWD/VHDB_phage_download_error.txt"
SUCCESS_TXT=$PWD/VHDB_phage_downloaded.txt
ERROR_TXT=$PWD/VHDB_phage_download_error.txt
LOG=$PWD/VHDB_phage_download.log
ALL_NUM=$(cut -f 1 ${ID_TXT}|uniq|wc -l)
COUNT=0
for PHAGE_ID in $(cut -f 1  ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    if [ $(grep ${PHAGE_ID} VHDB_host_downloaded.txt) ];then
        continue
    else
        echo ${PHAGE_ID} >> ${LOG}
        python ${SCRIPTS}/ncbi_phage_download.py  ${PHAGE_ID}  ${PHAGE_DB}/${PHAGE_ID}
        
        if [ $? -ne 0 ];then
            #如果下载成功放入SUCCESS_TXT，如果下载不成功放入ERROR_TXT
            echo ${PHAGE_ID} >> ${ERROR_TXT}
        else
            echo ${PHAGE_ID} >> ${SUCCESS_TXT}
        fi
    fi
done
echo "end"



# PHAGE_DB=$PWD/db/phage
# SCRIPTS=$PWD/scripts
# ID_TXT=$PWD/data/VHDB_phage_id.txt
# ALL_NUM=$(cut -f 1  ${ID_TXT}|uniq|wc -l)
# COUNT=0
# for PHAGE_ID in $(cut -f 1  ${ID_TXT}|uniq);do
#     let COUNT++
#     printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
#     # rm -rf ${PHAGE_DB}/${PHAGE_ID}
#     python ${SCRIPTS}/ncbi_download.py faa ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
#     python ${SCRIPTS}/ncbi_download.py fna ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
#     python ${SCRIPTS}/ncbi_download.py gff3 ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
#     # echo ${PHAGE_ID} >> VHDB_phage_downloaded.txt
#     if [ $? -ne 0 ];then
#         #如果下载成功放入SUCCESS_TXT，如果下载不成功放入ERROR_TXT
#         echo ${GCF} >> ${ERROR_TXT}
#     fi
# done
# echo "end"