# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:46:15 2023

@author: Isak
"""
#from pathlib import Path
import os
data_path = "./data/"

def parse_graph(g_string):
    with open(g_string) as g_file:
        while True:
            l = g_file.readline()
            print("reading start: ", l)
            syms = l.split()
            if syms[0] == 'p':
                n_v = int(syms[2])
                n_e = int(syms[3])
                break
        for l in g_file:
            vertices = l.split()
            print(vertices)
            if len(vertices) == 0 or vertices[0] == 'c': # if comment - skip
                continue
            v1 = int(vertices[0])
            #if v1 == 1:
            #   print(g[v1])
            v2 = int(vertices[1])
            
            if g.get(v1): #if already in dict
                g[v1].append(v2)
            else:
                g[v1] = [v2]
            if g.get(v2): #if already in dict
                g[v2].append(v1)
            else:
                g[v2] = [v1]


def parse_tree(t_string):
    with open(t_string) as t_file:
        while True:
            l = t_file.readline()
            print("reading start: ", l)
            syms = l.split()
            if syms[0] == 's':
                num_bags = int(syms[2])
                tree_w = int(syms[3])-1
                num_v = int(syms[4])
                break     
        for l in t_file:
            vertices = l.split()
            print(vertices)
            if len(vertices) == 0 or vertices[0] == 'c': # if comment - skip
                continue
            elif vertices[0] == 'b':     
                bag_n = int(vertices[1])
                vertices = vertices[2:len(vertices)] #remove first 2 (symbol + bag nbr), rest should be nodes
                vertices = [int(v) for v in vertices]
                bags[bag_n] = vertices
            else: #in this case we have rows describing edges, so 2 values
                #do edge stuff
                v1 = int(vertices[0])
                #if v1 == 1:
                #   print(g[v1])
                v2 = int(vertices[1])
                
                if t.get(v1): #if already in dict
                    t[v1].append(v2)
                else:
                    t[v1] = [v2]
                if t.get(v2): #if already in dict
                    t[v2].append(v1)
                else:
                    t[v2] = [v1]
            
def make_rooted(t):
    def rec_make_rooted(v, parent):
        t[v].remove(parent)
        for child in t[v]:
            rec_make_rooted(child, v)

    root = list(t.keys())[0] # practically random, but deterministic

    for child in t[root]:
        rec_make_rooted(child, root)
    return root, t

global empty
global c_table

def independent_set(t, bags, root):
    global empty
    global c_table
    c_table = {} #table of tables (first key (which bag/table (t in pdf))) bag_nbr : value table(dict) of c_values with key subset (S in pdf, binary enc) : value c_value))
    rec_calc_c(t, bags, root) #start from root, root looks at children values etc recursively
    

#want c values for each subset- for each node -> dictionary of dictionaries, with outer key
#being node and inner being subset -> binary encoding i guess
#t is tree of nodes, bags is node contents, node is current node in tree
# assuming bags contains key bag_nbr : val binary_enc_of_bagset
# and t contains key bag_nbr : val list of children's bag nbrs


def rec_calc_c(t, bags, node):
    children = t[node] #list of children
    global c_table
    empty = 0  #should be right
    
    if not children:  #leaf node -> base case
        c_table[node] = {node:0}
        return {node:0} #probably a dictionary later, with S as key? maybe value can be set + c?
    
    else: #split in 3 cases?
        node_t = get_node_t(node, children, bags) #node type
        #do these for each subset S
        if node_t == "join":
            atemp = bags[node]
            btemp = binary_encoding(atemp)
            S_set = powerset(btemp)
            S_set = powerset(binary_encoding(bags[node]))
            c1 = rec_calc_c(t, bags, children[0]) 
            #c_table[children[0]] = ... ^
            c2 = rec_calc_c(t, bags, children[1])
            #dont need to redo this, one call to rec_calc should calculate for all subsets 
            for S in S_set: #for each subset              
                #join node -> same subsets in children as parent
                c_table[node][S] = c1[S] + c2[S] - sum([1 if i != 0 else 0 for i in binary_decoding(S)]) #sum(S) is meant to be nbr of 1s in 1hot S
                #is sum over list inefficient?
            return c_table[node]
            #more efficient way?
            
            # something like | (think above is good)
            #                v
            #c_table[node] = {subset_binaryenc : val for subset_binaryenc in subset}
            #where c_table is big table, c_table[node] are subtables
        #by changing last argument to children[0] in recursive calls below we switch to t' from t (node)
        elif node_t == "forget":
            atemp = bags[node]
            btemp = binary_encoding(atemp)
            S_set = powerset(btemp)
            #S_set = powerset(binary_encoding(bags[node]))
            S_set = binary_decoding(powerset(binary_encoding(bags[node])))
            c1 = rec_calc_c(t, bags, children[0])
            #c2 = rec_calc_c(t, set_union(S, w), bags, children[0])
            for S in S_set:
                c_table[node][S] = max(c1[S], c1[set_union(S, w)])
            return c_table[node]
        
        elif node_t == "introduce":
            v = set_difference(bags[node], bags[children[0]]) #The node that is introduced
            atemp = bags[node]
            btemp = binary_encoding(atemp)
            S_set = powerset(btemp)
            #S_set = powerset(binary_encoding(bags[node]))
            c1 = rec_calc_c(t, bags, children[0])
            for S in S_set:
                if set_intersection(bags[node], v) == empty: 
                    c_table[node][S] = c1[S]
                    #rec_calc_c(t, bags, children[0])
                else: 
                    c_table[node][S] = c1[set_difference(S, v)]+1 #the 1 for having 1 more node after introduce
                    #rec_calc_c(t, set_difference(S, v), bags, children[0])
            return c_table[node]



# given a list represetnation of the set, encode it into a binary representation
def binary_encoding(list_set):
    assert(isinstance(list_set, list))
    return sum ([1<<i for i in list_set])

# given a binary representation of a set, decode it into a list representation
def binary_decoding(int_set):
    assert(isinstance(int_set, int))
    list = []
    while int_set > 0:
        highest_bit = int_set.bit_length() - 1
        list.append(highest_bit) 
        int_set ^=  (1 << highest_bit) # flip highest bit to 0
    return list

def set_union(a, b):
    assert(isinstance(a, int))
    assert(isinstance(b, int))
    return a | b

def set_difference(a, b): # given binary representations of 2 sets, find their difference
    assert(isinstance(a, int))
    assert(isinstance(b, int))
    return a & ~ b

def set_intersection(a, b): # given binary representations of 2 sets, find their interseciton
    assert(isinstance(a, int))
    assert(isinstance(b, int))
    return a & b

#finds subsets
def powerset(int_set): 
    assert(isinstance(int_set, int))
    masks = [1 << mask for mask in range(int_set.bit_length())  if int_set & (1 << mask)] # eg int_set 0011 gives [0001, 0010]
    
    ls = {int_set}
    for mask in masks: #2^n subsets
        ls.update(powerset(int_set^mask)) # turn off the masked bit with xor 
    return ls

def get_node_t(node, children, bags):
    if len(children) > 1:
        return "join"
    elif len(bags[children[0]]) > len(bags[node]): #if child bag is bigger, this is forget
        return "forget"
    else:
        return "introduce" #only option left

def root_fine(t, bags, root):
    new_root = root
    #index = len(bags)
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
    return (t,bags,new_root)

def leaf_fine(t, bags):
    index = len(bags) + 1
    for bag in range(1,index) :
             
        if not t[bag]: #if bag is a leaf
            if bags[bag]:#if bag is not empty
                node = bags[bag]
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
    index = len(bags) + 1          
    if bags[leaf]:#if bag is not empty
        node = bags[leaf]
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
    index = len(bags) + 1
    for parent in dicti:
        enfants = t[parent]
        for i in range(len(enfants)):
            child = enfants[i]

            parentbag = set(bags[parent])
            childbag  = set(bags[child])
            to_introduce = parentbag - (parentbag & childbag)
            to_forget = childbag - (parentbag & childbag)

             
            if to_forget: # non-empty
                to_forget.pop()
            elif to_introduce: 
                to_introduce.pop()
            else:
                continue

            del(t[parent][i])
            new_node = parent 

            for node in to_introduce:
                new_node = index
                t[parent][i] = new_node
                parentbag.remove(node)
                bags[new_node] = list(parentbag)
                parent = new_node
                index += 1

            for node in to_forget:
                new_node = index
                t[parent][i] = new_node
                parentbag.add(node)
                bags[new_node] = list(parentbag)
                parent = new_node
                index += 1
            
            if new_node==parent:
                t[new_node][i] = child
            else:
                t[new_node] = [child]

            

            


    #         firstchild = t[v][0]
    #         del(t[v][0])
    #         t,bags,highest = root_fine(t,bags,x)
    #         t, bags,new_leaf = one_leaf(t, bags, v)
    #         t[new_leaf].append(highest)
    # return t, bags


def make_nice(t,bags,root):
    t,bags,root = root_fine(t, bags,root)
    t, bags = leaf_fine(t, bags)
    t, bags = between_nodes(t, bags)
    return t, bags, root



if __name__ == "__main__":
        #to rep graph... all edges in a list? 
    #a dict with vertices as keys and lists of edges(pairs of vertex-nums) as values?
    # Internet - key vertex, value list of neighbours
    g = {}
    n_e = 0 #number of edges in input
    n_v = 0 #number of vertices in input
    t = {} #dict for edges in tree - Ill use one dict for bags and one for bag-edges (both with bag nbr as key) - could make joint data class
    bags = {} #dict for bags
    num_bags = 0
    tree_w = 0
    num_v = 0 #number of vertices in the original graph (should match n_v)
    #g_string = data_path + "BalancedTree_3_5.gr"
    #t_string = data_path + "BalancedTree_3_5.td"
    #g_string = Path("BalancedTree_3_5.gr")
    #t_string = Path("BalancedTree_3_5.td")
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    g_rel_path = "data/web1.gr"
    t_rel_path = "data/web1.td"
    g_string = os.path.join(script_dir, g_rel_path)
    t_string = os.path.join(script_dir, t_rel_path)
    #g_string = Path(__file__).with_name('BalancedTree_3_5.gr')
    #t_string = Path(__file__).with_name('BalancedTree_3_5.td')
    #print(g_string)
    parse_graph(g_string)
    parse_tree(t_string)

    print(len(t))
    root, t = make_rooted(t)
    print(len(t))
    #t, bags, root = make_nice(t,bags, root)
    result = independent_set(t, bags, root)
    print(result) 

    