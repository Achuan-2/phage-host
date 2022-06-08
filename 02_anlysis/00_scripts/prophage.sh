#!/bin/bash
#SBATCH --cpus-per-task=10
#SBATCH -o slurm.%N.%j.out        # STDOUT
#SBATCH -e slurm.%N.%j.err        # STDERR
BACTERIA_ID=$1
path=/mnt/raid7/Dachuang/Achuan/03_phage_host
VIRUS_INDEX=/mnt/raid7/Dachuang/Achuan/03_phage_host/db/Virus_index
BACTERIA_FA=$2
# 导入perl lib环境变量
export PERL5LIB=/mnt/raid7/Dachuang/Biosoft/miniconda3/envs/achuan/lib/perl5/site_perl/5.22.0/

cd /mnt/raid7/Dachuang/Achuan/03_phage_host
mkdir -p 02_Prophage
cd 02_Prophage
mkdir -p 01_phagefinder
mkdir -p 02_prophage
# mkdir -p 03_cut
# mkdir -p 04_megablast_virus
# mkdir -p 05_megablast_virus_noevalue

echo "step 1.1 contig file exists and create directory"
cd 01_phagefinder
mkdir -p ${BACTERIA_ID}
echo "step 2.1 uncompress contig file ..."
cat   $BACTERIA_FA |awk '/^>/&&NR>1{print "";}{ printf "%s",/^>/ ? $0" ":$0 }' |\
    awk '{print $1"\n"$NF}' >${BACTERIA_ID}/${BACTERIA_ID}.con

echo "step 2.2 run tRNA predictions ... "
#### tRNAscan-SE -Q -B -o ${BACTERIA_ID}/tRNAscan.out ${BACTERIA_ID}/${BACTERIA_ID}.con > /dev/null
/mnt/raid5/sunchuqing/Softwares/aragorn -m -o ${BACTERIA_ID}/tmRNA_aragorn.out ${BACTERIA_ID}/${BACTERIA_ID}.con

echo "step 2.3 get pep and gff file ..."
/mnt/raid5/sunchuqing/Softwares/gmhmmp -m /mnt/raid8/sunchuqing/Softwares/MetaGeneMark_v1.mod -f 3 -o ${BACTERIA_ID}/${BACTERIA_ID}.gff -A ${BACTERIA_ID}/${BACTERIA_ID}.pep.tmp ${BACTERIA_ID}/${BACTERIA_ID}.con

echo "step 2.4 change seq names and run blastall --"
perl /mnt/raid1/data/wchen_data/reformat_seq_name.pl -i ${BACTERIA_ID}/${BACTERIA_ID}.pep.tmp -o ${BACTERIA_ID}/${BACTERIA_ID}.pep
/mnt/raid7/sunchuqing/Softwares/bin/blastall -p blastp -m 8 -e 0.001 -o ${BACTERIA_ID}/ncbi.out -v 4 -b 4 -a 4 -F F -i ${BACTERIA_ID}/${BACTERIA_ID}.pep -d /mnt/raid1/data/wchen_data/phage_finder_v2.1/DB/phage_10_02_07_release.db

echo "step 2.5 get information file -- "
perl /mnt/raid1/data/wchen_data/gff2Phage_Finder_infor_file.pl \
        -s ${BACTERIA_ID}/${BACTERIA_ID}.con \
        -i ${BACTERIA_ID}/${BACTERIA_ID}.gff \
        -o ${BACTERIA_ID}/phage_finder_info.txt  > /dev/null
echo "step 2.6 enter the dir and run hmmsearch ... "
cd ${BACTERIA_ID}
bash /mnt/raid1/data/wchen_data/phage_finder_v2.1/bin/HMM3_searches.sh $path/02_Prophage/01_phagefinder/${BACTERIA_ID}/${BACTERIA_ID}.pep

echo "step 2.7 enter the dir and run script ... " 
/mnt/raid1/data/wchen_data/phage_finder_v2.1/bin/Phage_Finder_v2.1.pl -t ncbi.out -i phage_finder_info.txt -n tmRNA_aragorn.out -A ${BACTERIA_ID}.con -S
cd ../..
echo "step 3. get prophage seq"
rm -rf 02_prophage/${BACTERIA_ID}
while read -r line
do
    genomename=`echo $line| tr -s ' ' | awk 'BEGIN {FS=" "} {print $1}'`
    if [ "$genomename" == "#asmbl_id" ];then
        continue
    fi
    seq=`grep -w -A 1 ">$genomename" 01_phagefinder/${BACTERIA_ID}/${BACTERIA_ID}.con|tail -n 1`
    start=`echo $line| tr -s ' ' | awk 'BEGIN {FS=" "} {print $4}'`
    len=`echo $line| tr -s ' ' | awk 'BEGIN {FS=" "} {print $6}'`
    echo ">${genomename}::${start}_${len}" >> 02_prophage/${BACTERIA_ID}
    echo ${seq: $start: $len} >> 02_prophage/${BACTERIA_ID}
done < "01_phagefinder/${BACTERIA_ID}/PFPR_tab.txt"

mkdir -p 03_blastn_virus/${BACTERIA_ID}
#mkdir -p 03_bowtie_virus/${BACTERIA_ID}
# bowtie2 -x $path/02_Enrichment/db/${BACTERIA_ID} \
#     -f 02_prophage/${BACTERIA_ID}\
#     -S 03_bowtie_virus/${BACTERIA_ID}/${BACTERIA_ID}.sam\
#     -p 16 --end-to-end
#awk 'BEGIN {FS="\t"} $3!="*" {print $1 "," $3}' 03_bowtie_virus/${BACTERIA_ID}/${BACTERIA_ID}.sam|grep -v "^@" > 03_bowtie_virus/${BACTERIA_ID}/${BACTERIA_ID}.b2v

/mnt/raid6/sunchuqing/Softwares/miniconda/bin/blastall -p blastn \
    -i 02_prophage/${BACTERIA_ID}  \
    -d ${VIRUS_INDEX}/Virus_blast \
    -o 03_blastn_virus/${BACTERIA_ID}/${BACTERIA_ID}.tab \
    -m 8 -e 1e-5 -a 16

# /mnt/raid7/Dachuang/Biosoft/miniconda3/envs/achuan/bin/blastn -query 02_prophage/${BACTERIA_ID} \
#     -out 03_blastn_virus/${BACTERIA_ID}/${BACTERIA_ID}.tab \
#     -db ${VIRUS_INDEX}/Virus_blast \
#     -outfmt 6 -evalue 1e-5 \
#     -num_threads 16 
# mkdir -p 02_Prophage_assign/${BACTERIA_ID}
# cd 02_Prophage_assign
mkdir -p 04_Assign
cat 03_blastn_virus/${BACTERIA_ID}/${BACTERIA_ID}.tab | \
    awk 'BEGIN {FS="\t"} $3>90 && $4>500 {print "'${BACTERIA_ID}'" "," $2}'> 04_Assign/${BACTERIA_ID}.b2v
# awk 'BEGIN {FS="[, ]"}  ($3>0.7 && $4>0.9) || ($3>0.9 && $4>0.7) {print $1 "," "'${BACTERIA_ID}'" "_" $2}' > ${BACTERIA_ID}/${BACTERIA_ID}.b2v

cd $path
# echo "step 4. megablast for prophage vs virus"
# blastall -n T -p blastn -m 8 -d /mnt/raid1/data/blastdb/virus/20181226/virus -e 1e-10 -i 02_prophage/${BACTERIA_ID} -a 4 -o 04_megablast_virus/${BACTERIA_ID}
# blastall -n T -p blastn -m 8 -d /mnt/raid1/data/blastdb/virus/20181226/virus -i 02_prophage/${BACTERIA_ID} -a 4 -o 05_megablast_virus_noevalue/${BACTERIA_ID}


<<run
# 1. 构建blast数据库
makeblastdb -in Virus_index/Virus.fna -dbtype nucl -out Virus_index/Virus_blast

# 2、跑流程
# 运行单个
HOST_DB=/mnt/raid7/Dachuang/Achuan/03_phage_host/db/host
SCRIPTS=/mnt/raid7/Dachuang/Achuan/03_phage_host/00_scripts
BACTERIA_ID="GCF_000005845.2" 
BACTERIA_FA="${HOST_DB}/${BACTERIA_ID}/${BACTERIA_ID}.fna"

bash ${SCRIPTS}/prophage.sh ${BACTERIA_ID} ${BACTERIA_FA}

# 运行全部样本
HOST_DB=/mnt/raid7/Dachuang/Achuan/03_phage_host/db/host
SCRIPTS=/mnt/raid7/Dachuang/Achuan/03_phage_host/00_scripts
ls ${HOST_DB} | while read BACTERIA_ID;do  sbatch ${SCRIPTS}/prophage.sh ${BACTERIA_ID} ${HOST_DB}/${BACTERIA_ID}/${BACTERIA_ID}.fna;done
run