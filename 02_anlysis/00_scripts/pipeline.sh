# 0.合并virus fna,构建噬菌体序列比对数据库
PROJECT=/mnt/raid7/Dachuang/Achuan/03_phage_host/
mkdir -p $PROJECT/01_db/Virus_index
cat $PROJECT/01_db/phage/*/*.fna > $PROJECT/01_db/Virus_index/Virus.fna
/mnt/raid6/sunchuqing/Softwares/miniconda/bin/blastall -p makeblastdb

## 0.1.构建bowtie2索引
cd $PROJECT/01_db/Virus_index/
bowtie2-build -f Virus.fna Virus

## 0.2.构建blastn索引
/usr/bin/makeblastdb -in $PROJECT/01_db/Virus_index/Virus.fna -dbtype nucl -out $PROJECT/01_db/Virus_index/Virus_blast


# 1. 跑crispr 代码
HOST_DB=$PROJECT/01_db/host
SCRIPTS=$PROJECT/00_scripts
COUNT=0
COMMAND='ls ${HOST_DB}'
ALL_NUM=$(eval $COMMAND |wc -l)
eval $COMMAND | while read BACTERIA_ID;do
    bash ${SCRIPTS}/crispr_crisprcasfinder.sh ${BACTERIA_ID} ${HOST_DB}/${BACTERIA_ID}/${BACTERIA_ID}.fna
    let COUNT++
    echo "progress:" ${COUNT} ${ALL_NUM} > crispr.log

done
run
# 2.跑prophage鉴定
HOST_DB=$PROJECT/01_db/host
SCRIPTS=$PROJECT/00_scripts
COUNT=0
COMMAND='ls ${HOST_DB}'
ALL_NUM=$(eval $COMMAND |wc -l)
eval $COMMAND | while read BACTERIA_ID;do
    bash ${SCRIPTS}/prophage.sh ${BACTERIA_ID} ${HOST_DB}/${BACTERIA_ID}/${BACTERIA_ID}.fna

    let COUNT++
    if [[ COUNT -lt ALL_NUM ]];then
        printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    else
        printf "progress:%d/%d\n" "${COUNT}" "${ALL_NUM}"
    fi
done
# 3.跑blastn鉴定
HOST_DB=$PROJECT/01_db/host
SCRIPTS=$PROJECT/00_scripts                       
COUNT=0
COMMAND='ls ${HOST_DB}'
ALL_NUM=$(eval $COMMAND |wc -l)
eval $COMMAND | while read BACTERIA_ID;do
    bash ${SCRIPTS}/blastn.sh ${BACTERIA_ID} ${HOST_DB}/${BACTERIA_ID}/${BACTERIA_ID}.fna
    let COUNT++
    if [[ COUNT -lt ALL_NUM ]];then
        printf "progress:%d/%d\r" "${COUNT}" "${ALL_NUM}"
    else
        printf "progress:%d/%d\n" "${COUNT}" "${ALL_NUM}"
    fi

done
echo "blastn $BACTERIA_ID to Virus DB"

