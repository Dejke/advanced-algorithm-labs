import random
import copy
import numpy as np

def mark_node(node, idx):
    if not node["marked"]:
        node["marked"] = True
        return (idx+1)
    else: 
        return idx

def is_leaf(node):
    return node["left_child"] is None and node["right_child"] is None

def is_nonroot(node):
    return node["parent"] is not None

def is_nonleaf(node):
    return node["left_child"] is not None and node["right_child"] is not None


def neighbors(node):
    """Returns the index (0-indexed) of every node that may be affected by an update to this node"""
    n = [] 
    if is_nonleaf(node):
        n.append(node["left_child"]-1)
        n.append(node["right_child"]-1)
    if is_nonroot(node):
        n.append(node["parent"]-1)
        n.append(node["sibling"]-1)
    return n
                        

def rec_rules(tree, index, is_initial_call = False):
    node = tree[index]
    
    if node["marked"]:
        return 0
    
    should_mark = is_initial_call
    
    if is_nonleaf(node): # First rule can't apply to leaf nodes
        left_child = tree[node["left_child"]-1]
        right_child = tree[node["right_child"]-1]
        #print("checking rule")
        if left_child["marked"] and right_child["marked"]: #First rule
         #   print("applying rule 1")
            should_mark = True
    if is_nonroot(node): # Second rule can't apply to root node
        parent = tree[node["parent"]-1]
        sibling = tree[node["sibling"]-1]
        #print("checking rule")
        if parent["marked"] and sibling["marked"]:  #Second rule
         #   print("applying rule 2")
            should_mark = True
    
    if should_mark: 
        marked = 1 
        node["marked"] = True
        for index in neighbors(node):
            marked += rec_rules(tree, index)
        return marked
    else: 
        return 0   
        
def R1(N):
    return random.randint(0, N-1)

def R2(N):
    l = [i for i in range(0,N-1)]
    random.shuffle(l)
    return l

def R3(N, tree):
    temp = []
    for node in tree:
        if not node["marked"]:
            temp.append(node["index"]-1) #adds tree index of the node
    choice = np.random.choice(temp)
    #print(choice)
    return(choice)

def build_tree(N):
    tree = [{"index": i, "marked": False, "left_child": None, "right_child": None, "parent": None, "sibling": None} for i in range(1,N+1)]
    for j in range(0,N):
        i = j+1
        left_child_index = 2*i 
        right_child_index = 2*i + 1
        parent_index = (i) // 2
        sibling_index = (i+1) if i % 2 == 0 else (i-1)
        if left_child_index <= N:
            tree[j]["left_child"] = left_child_index
        if right_child_index <= N:
            tree[j]["right_child"] = right_child_index
        if parent_index >= 1:
            tree[j]["parent"] = parent_index
        if sibling_index >= 1 and sibling_index <= N:
            tree[j]["sibling"] = sibling_index
    return tree

def marking1(tree):
    N=len(tree)
    counter = 0
    marked = 0
    while marked<N:
        index = R1(N)
        counter += 1
        marked += rec_rules(tree, index, is_initial_call = True)

    return(counter)


def marking2(tree):
    N=len(tree)
    counter = 0
    marked=0
    r2_l = R2(N)
    #print(r2_l)
    while marked<N:
        index = r2_l[counter]
        counter += 1
        marked += rec_rules(tree, index, is_initial_call = True)

    return(counter)

def marking3(tree):
    N=len(tree)
    counter = 0
    marked = 0
    while marked<N:
        index = R3(N, tree)
        counter += 1
        marked += rec_rules(tree, index, is_initial_call = True)

    return(counter)

def calculate(N, iterations, markingfunction): 
    """ Run the algorithm (iterations) times, and calculate mean & standard deviation of results
        N is size of tree
        R is sampling function
    """

    tree = build_tree(N)
    lst=[]
    for i in range (iterations):
        tree_copy = copy.deepcopy(tree)
        lst.append(markingfunction(tree_copy))
    mean = sum(lst) / len(lst)
    print("The mean is :", mean)
    std = (sum([(x - mean) ** 2 for x in lst]) / len(lst)) ** 0.5
    
    return mean, std

def generate_table(samples = 1, max_power = 20):
    """Run all the experiments, and generate a latex table"""
    def emptystring(*args):
        return ""
    

    try: 
        import pandas as pd 
        N = [2**power-1 for power in range(2,max_power)]
        funcs = [R1,R2,R3]

        results = pd.DataFrame()
        for n in N:
            row  = []
            for func in funcs:
                print(f'N{n}')
                row.append(calculate(n, samples, func))
            results.append(row)
            print(row)
        print(results)
    except ModuleNotFoundError: 
        print("error: can't generate table without pandas package (pip install pandas)")

if __name__ == "__main__":
#    generate_table(max_power=4)
    
    mean, std = calculate(1023, 10, marking1)   
    print("The mean is :", mean)
    print("The standard deviation is:", std)
    



