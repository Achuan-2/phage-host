def simplify_name(name):
    index = name.rfind(' ')
    if index==-1:
        return name
    name2=name[0:index]
    return name2
def last_lineage(lineage):
    return lineage.split('; ')[-1]

if __name__=="__main__":
    x='Bacteria; Terrabacteria group; Tenericutes; Mollicutes; Acholeplasmatales; Acholeplasmataceae; Acholeplasma'
    list1=x.split('; ')
    while list1:
        x = list1.pop(-1)
        print(x)
    
