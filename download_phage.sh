# 下载phage
PHAGE_DB=$PWD/db/phage
SCRIPTS=$PWD/scripts
ID_TXT=$PWD/data/VHDB_phage_id.txt
ALL_NUM=$(cut -f 1  ${ID_TXT}|uniq|wc -l)
COUNT=0
for PHAGE_ID in $(cut -f 1  ${ID_TXT}|uniq);do
    let COUNT++
    printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    # rm -rf ${PHAGE_DB}/${PHAGE_ID}
    python ${SCRIPTS}/ncbi_download.py faa ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
    python ${SCRIPTS}/ncbi_download.py fna ${PHAGE_ID} ${PHAGE_DB}/${PHAGE_ID}
    echo ${PHAGE_ID} >> VHDB_phage_downloaded.txt
done
echo "end"
