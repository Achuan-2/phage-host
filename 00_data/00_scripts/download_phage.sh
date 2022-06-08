# 下载phage
HOST_DB=../../01_db/phage
SCRIPTS=./
DOWNLOAD=../download/
ID_TXT="$DOWNLOAD/phage_id.txt"
SUCCESS_TXT=$DOWNLOAD/VHDB_phage_downloaded.txt
touch $SUCCESS_TXT
ERROR_TXT=$DOWNLOAD/VHDB_phage_download_error.txt
LOG=$DOWNLOAD/VHDB_phage_download.log
ALL_NUM=$(cut -f 1 ${ID_TXT}|uniq|wc -l)
COUNT=0
for PHAGE_ID in $(cut -f 1  ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    if [ $(grep ${PHAGE_ID} $SUCCESS_TXT) ];then
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
