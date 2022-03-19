# 下载phage
PHAGE_DB=$PWD/db/phage
SCRIPTS=$PWD/scripts
ID_TXT=data_pos.txt
ALL_NUM=$(cut -f 1 -d "," ${ID_TXT}|uniq|wc -l)
COUNT=0
for PHAGE_ID in $(cut -f 1 -d "," ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    # rm -rf ${PHAGE_DB}/${PHAGE_ID}
    python ${SCRIPTS}/ncbi_download.py faa ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
    python ${SCRIPTS}/ncbi_download.py fna ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
done
echo "end"

# 下载bacteria
PHAGE_DB=$PWD/db/bacteria
SCRIPTS=$PWD/scripts
ID_TXT=data_pos.txt
ALL_NUM=$(cut -f 2 -d "," ${ID_TXT}|uniq|wc -l)
COUNT=0
for PHAGE_ID in $(cut -f 2 -d "," ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    # rm -rf ${PHAGE_DB}/${PHAGE_ID}
    python ${SCRIPTS}/ncbi_download.py faa ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
    python ${SCRIPTS}/ncbi_download.py fna ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
done
echo "end"
