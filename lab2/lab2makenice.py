def root_fine(t, bags,root):
    new_root = root
    if not bags[root]==[]:
        n=len(t[root])
        index = len(bags)
        node = t[root]
        node_child = root
        for i in range(n):
            del(node[0])
            bags[index]=node
            t[index] =[node_child]
            node_child = index
            index +=1
    new_root = index-1
    return(t,bags,new_root)

def leaf_fine(t, bags):
    index = len(bags)
    for bag in t :
        #print(t)
        if t[bag]==[]: #if bag is a leaf
            if not bags[bag]==[]:#if bag is not empty
                node = t[bag]
                n = len(node)
                del(node[0])
                bags[index]=node
                t[index] =[bag]
                index +=1
                for i in range(1,n):
                    del(node[0])
                    bags[index]=node
                    if i!=n-1: #if it is not the final leaf
                        t[index] = [index+1]
                        index +=1
                    else : 
                        t[index]=[]
    return t, bags
    
def one_leaf(t, bags,leaf):
    new_leaf = leaf
    index = len(bags)           
    if not bags[leaf]==[]:#if bag is not empty
        node = t[leaf]
        n = len(node)
        del(node[0])
        bags[index]=node
        t[index] =[leaf]
        index +=1
        for i in range(1,n):
            del(node[0])
            bags[index]=node
            if i!=n-1: #if it is not the final leaf
                t[index] = [index+1]
                index +=1
            else : 
                t[index]=[]
        new_leaf = index
    return t, bags,new_leaf


def between_nodes(t, bags):
    dicti=bags
    for v in dicti:
        enfants = t[v]
        for i in range(len(enfants)) : 
            del(t[v][i])
            t,bags,highest = root_fine(t,bags,t[v][i])
            t, bags,new_leaf = one_leaf(t, bags,)
            t[new_leaf].append(highest)
    return t, bags

def fine_dec(t,bags,root):
    t,bags,root = root_fine(t, bags,root)
    t, bags = leaf_fine(t, bags)
    t, bags = between_nodes(t, bags)
    return t, bags, root



