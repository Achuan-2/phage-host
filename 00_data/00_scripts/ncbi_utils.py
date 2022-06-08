import os
def simplify_name(name):
    index = name.rfind(' ')
    if index==-1:
        return name
    name2=name[0:index]
    return name2
def last_lineage(lineage):
    list1=lineage.split('; ')
    while list1:
        x = list1.pop(-1)
        print(x)
def writefile(filename, content):
    file = open(filename, mode='w', encoding='utf-8')
    file.write(content)
    file.close()


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
if __name__=="__main__":
    last_lineage('Bacteria; Terrabacteria group; Tenericutes; Mollicutes; Acholeplasmatales; Acholeplasmataceae; Acholeplasma')
    
