import pandas as pd


df=pd.read_table('../virushostdb_output(filtered).tsv')
phage_list=[]
for line in set(df['viral_acc']):
    if ',' in line:
        accs=[acc.strip() for acc in line.split(',')]
        phage_list.extend(accs)
    else:
        phage_list.append(line.strip())
set1=set(phage_list)
f = open("../download/phage_id.txt", "w")
f.write('\n'.join(set1))
f.close()


host_list = []
for line in set(df['new_gcf']):
    host_list.append(line.strip())
f = open("../download/host_id.txt", "w")
f.write('\n'.join(host_list))
f.close()
