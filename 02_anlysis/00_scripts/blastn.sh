#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH -o slurm.%N.%j.out        # STDOUT
#SBATCH -e slurm.%N.%j.err        # STDERR


BACTERIA_ID=$1
BACTERIA_FA=$2
path=/mnt/raid7/Dachuang/Achuan/03_phage_host/

VIRUS_INDEX=/mnt/raid7/Dachuang/Achuan/03_phage_host/db/Virus_index

mkdir -p $path/03_blastn
cd $path/03_blastn

# echo "blastn $BACTERIA_ID to Virus DB"
mkdir -p 01_blastn_virus/$BACTERIA_ID
/mnt/raid6/sunchuqing/Softwares/miniconda/bin/blastall -p blastn \
    -i $BACTERIA_FA \
    -d ${VIRUS_INDEX}/Virus_blast \
    -o 01_blastn_virus/${BACTERIA_ID}/${BACTERIA_ID}.tab \
    -m 8 -e 1e-5 -a 16


mkdir -p 02_Assign
echo "Bac,Virus,identity,hit length">02_Assign/${BACTERIA_ID}.b2v
cat 01_blastn_virus/${BACTERIA_ID}/${BACTERIA_ID}.tab | \
    awk 'BEGIN {FS="\t"} $3>90 && $4>500 {print "'${BACTERIA_ID}'" "," $2 "," $3 "," $4}'>> 02_Assign/${BACTERIA_ID}.b2v
cd $path

<<run
# 1. 构建blast数据库
makeblastdb -in Virus_index/Virus.fna -dbtype nucl -out Virus_index/Virus_blast

# 2、跑流程
# 运行单个
HOST_DB=/mnt/raid7/Dachuang/Achuan/03_phage_host/db/host
SCRIPTS=/mnt/raid7/Dachuang/Achuan/03_phage_host/00_scripts
BACTERIA_ID="GCF_000005845.2" 
BACTERIA_FA="${HOST_DB}/${BACTERIA_ID}/${BACTERIA_ID}.fna"

bash ${SCRIPTS}/blastn.sh ${BACTERIA_ID} ${BACTERIA_FA}

# 运行全部样本
HOST_DB=/mnt/raid7/Dachuang/Achuan/03_phage_host/db/host
SCRIPTS=/mnt/raid7/Dachuang/Achuan/03_phage_host/00_scripts
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
run