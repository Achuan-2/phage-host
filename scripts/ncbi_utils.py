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

if __name__=="__main__":
    last_lineage('Bacteria; Terrabacteria group; Tenericutes; Mollicutes; Acholeplasmatales; Acholeplasmataceae; Acholeplasma')
    
