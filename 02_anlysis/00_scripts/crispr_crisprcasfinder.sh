#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH -o slurm.%N.%j.out        # STDOUT
#SBATCH -e slurm.%N.%j.err        # STDERR

# 1、输入变量
# - BACTERIA_ID：基因组id
# - fa 基因组序列路径
BACTERIA_ID=$1
BACTERIA_FA=$2
VIRUS_INDEX=/mnt/raid7/Dachuang/Achuan/03_phage_host/db/Virus_index

mkdir -p 01_CRISPR
cd 01_CRISPR
mkdir -p 01_spacers_result
mkdir -p 02_spacers
mkdir -p 03_repeats

export PATH=$PATH:/mnt/raid6/sunchuqing/Softwares/miniconda3/bin/

# 2、CRISPRCasFinder 运行鉴定CRISPR SPACER，结果放入01_spacers_result
/usr/bin/perl /mnt/raid1/tools/CRISPR_tools/CRISPRCasFinder-release-4.2.20/CRISPRCasFinder.pl \
    -soFile /mnt/raid1/tools/CRISPR_tools/CRISPRCasFinder-release-4.2.20/sel392v2.so \
    -cf CasFinder-2.0.3 -def G -keep \
    -in ${BACTERIA_FA} \
    -out 01_spacers_result/${BACTERIA_ID}




# 3、解析结果文件夹的result.json文件，jq是命令行解析json文件
# 3.1.获取Sequences字段下的Crisprs内容，把Name和Re字段提取出来,经过处理后得到类似fasta的格式，>id Array_序号_起始_结束 第二行是cripsr序列
dir=`cat 01_spacers_result/${BACTERIA_ID}/result.json|jq '.Sequences[].Crisprs[] | {Name,Re: .Regions[]}' |grep -A 4 -B 2 "Spacer"`

# sed 's/"Name"/\n>/g' 把Name字段删除只保留id
# sed 's/\(.*\)_\(.*\)/\1\tArrary_\2/' 把id_序号改成“id Arrary_序号”
# sed 's/:\|"\| \|}\|--//g' 去除冒号、引号、空格、}和--，\|是或的意思
#  sed 's/,Re.*Start/_/g'| sed 's/,End/_/g'|sed 's/,Sequence/\n/g' 是为了得到>id Array_序号_起始_结束 第二行是cripsr序列
echo $dir | sed 's/"Name"/\n>/g' |sed 's/\(.*\)_\(.*\)/\1\tArrary_\2/'  | sed 's/:\|"\| \|}\|--//g' |  sed 's/,Re.*Start/_/g'| sed 's/,End/_/g'|sed 's/,Sequence/\n/g'|grep -v "^$" > 02_spacers/${BACTERIA_ID}.2

# 3.2. 获取DR_Consensus信息（应该就是CRISPR里的重复片段，放入repeats文件夹下
dir2=`cat 01_spacers_result/${BACTERIA_ID}/result.json|jq '.Sequences[].Crisprs[] | {Name,DR_Consensus}'`

echo $dir2 | sed 's/"Name"/\n>/g'|sed 's/, "DR_Consensus": /\n/g' |sed 's/\(.*\)_\(.*\)/\1\tArrary_\2/'  | sed 's/:\|"\| \|}\|--\|{//g' |grep -v "^$"> 03_repeats/${BACTERIA_ID}.2


# 3.3. 获取Evidence_Level，保存到01_spacers_result/${BACTERIA_ID}/${BACTERIA_ID}.confidance，在对之前提取的sripsr序列进行筛选，得到from.contig
dir3=`cat 01_spacers_result/${BACTERIA_ID}/result.json|jq '.Sequences[].Crisprs[] | {Name,Evidence_Level}'`

echo $dir3 | sed 's/"Name"/\n>/g'|sed 's/, "Evidence_Level": /,/g' |sed 's/\(.*\)_\(.*\)/\1\tArrary_\2/'  | sed 's/:\|"\| \|}\|--\|{//g' |grep -v "^$" |awk -F "," ' $NF==4 {print $1}' > 01_spacers_result/${BACTERIA_ID}/${BACTERIA_ID}.confidance

grep -A 1 -Ff 01_spacers_result/${BACTERIA_ID}/${BACTERIA_ID}.confidance 02_spacers/${BACTERIA_ID}.2 |grep -v "^-"> 02_spacers/${BACTERIA_ID}.from.contig
mkdir -p 04_bowtie_virus/${BACTERIA_ID}

# 4、把${BACTERIA_ID}.from.contig 与virus进行比对，即spacer到病毒序列的比对
bowtie2 -x ${VIRUS_INDEX}/Virus \
    -f 02_spacers/${BACTERIA_ID}.from.contig \
    -S 04_bowtie_virus/${BACTERIA_ID}/${BACTERIA_ID}.sam\
    -p 16 --end-to-end

# 提取宿主和细菌比对上的序号：不要@开头的注释，提取宿主序号和比对上，但有一个问题是有重复
grep -v "^@" 04_bowtie_virus/${BACTERIA_ID}/${BACTERIA_ID}.sam |awk 'BEGIN {FS="\t"} $3!="*" {print "'${BACTERIA_ID},'" $3}' |grep -v "@" > 04_bowtie_virus/${BACTERIA_ID}/${BACTERIA_ID}.b2v

<<run
# 1、先构建索引,建索引通常出现的条件是在测序产生的reads片段与参考基因组进行比对时，为了比对更加快速，需要建立索引（相对于目录性质），帮助比对软件更快速的找到目标区域
# 1.1合并所有phage文件
mkdir -p Virus_index
cat db/phage/*/*.fna > Virus_index/Virus.fna

# 1.2构建索引
cd Virus_index
bowtie2-build -f Virus.fna Virus


# 2、跑流程
# 运行单个
HOST_DB=/mnt/raid7/Dachuang/Achuan/03_phage_host/db/host
SCRIPTS=/mnt/raid7/Dachuang/Achuan/03_phage_host/00_scripts
BACTERIA_ID="GCF_000007805.1" 
BACTERIA_FA="$DB/${BACTERIA_ID}/${BACTERIA_ID}.fna"

bash ${SCRIPTS}/crispr_crisprcasfinder.sh ${BACTERIA_ID} ${BACTERIA_FA}

# 运行全部样本
# 注意：这个命令不能用sbatch批量运行，因为软件的问题，不同id会产生相同的临时文件，而一个运行完又会把临时文件删除，同时运行的另一个就会报错。
HOST_DB=/mnt/raid7/Dachuang/Achuan/03_phage_host/db/host
SCRIPTS=/mnt/raid7/Dachuang/Achuan/03_phage_host/00_scripts
ls ${HOST_DB} | while read BACTERIA_ID;do  bash ${SCRIPTS}/crispr_crisprcasfinder.sh ${BACTERIA_ID} ${HOST_DB}/${BACTERIA_ID}/${BACTERIA_ID}.fna;done
run