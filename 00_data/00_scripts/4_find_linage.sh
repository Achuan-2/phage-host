
# 获取find name的taxonomy信息
## 1 提取find name，然后根据name获得taxid和taxid rank
cd ..
cut -f 10  virushostdb_output.tsv > temp/find_name.tsv
sed -i '1d' temp/find_name.tsv

cat temp/find_name.tsv | taxonkit name2taxid -r | tee temp/find_rank.tsv


## 生成后需要先过滤info中重复的行，比如
#Bacillus\t55087、Gordonia\t7925、Morganella\t90690、Morganella\t108061,Paracoccus\t249411
# 还有Mycoplasma arthritidis无法直接获得taxid，需要手动加上Mycoplasma arthritidis 2111	species
## 3.3 根据taxid得到tax lineage
cut -f 2 temp/find_rank.tsv > temp/find_taxid.txt

cat temp/find_taxid.txt | taxonkit lineage | taxonkit reformat -f "{k}\t{p}\t{c}\t{o}\t{f}\t{g}\t{s}\t{t}" -P | cut -f 3- |  tr '\t' ';' | tee temp/find_lineage.tsv


paste temp/find_rank.tsv temp/find_lineage.tsv > lineage/find_info.tsv
# 验证：比较有无错误，使用vscode的文件比较功能
cut -f 1 lineage/find_info.tsv > temp/find_name2.tsv