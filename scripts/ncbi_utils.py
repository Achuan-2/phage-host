def simplify_name(name):
    index = name.rfind(' ')
    if index==-1:
        return name
    name2=name[0:index]
    return name2
