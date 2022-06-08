#下载bacteria,
## 使用biopython Entrez接口

HOST_DB=../../01_db/host
SCRIPTS=./
DOWNLOAD=../download/
ID_TXT="$DOWNLOAD/host_id.txt"
SUCCESS_TXT=$DOWNLOAD/VHDB_host_downloaded.txt
touch $SUCCESS_TXT
ERROR_TXT=$DOWNLOAD/VHDB_host_download_error.txt
LOG=$DOWNLOAD/VHDB_host_download.log
ALL_NUM=$(cut -f 1 ${ID_TXT}|uniq|wc -l)
COUNT=0
for GCF in $(cut -f 1 ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    if [ $(grep ${GCF} $SUCCESS_TXT) ];then
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



