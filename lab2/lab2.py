# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:46:15 2023

@author: Isak
"""
data_path = "./data/"





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
            
def make_rooted():
    def rec_make_rooted(v, parent):
        t[v].remove(parent)
        for child in t[v]:
            rec_make_rooted(child, v)

    root = list(t.keys())[0] # practically random, but deterministic

    for child in t[root]:
        rec_make_rooted(child, root)
    print(f"root: {root} \nrootchildren: {t[root]}")
    return root



def make_nice():
    pass

global empty

def independent_set():
    #make starting set S
    S = binary_encoding()
    global empty
    empty = set_difference(S,S)
    pass

#t is tree of nodes, bags is node contents, node is current node in tree
def rec_calc_c(t, S, bags, node):
    children = t[node] #list of children
    
    empty = 0  #should be right
    
    if not children:  #leaf node -> base case
        c = 0
        return [c] #probably a dictionary later, with S as key? maybe value can be set + c?
    else: #split in 3 cases?
        node_t = get_node_t(children, bags) #node type
        
        if node_t == "join":
            c1 = rec_calc_c(t, S, bags, children[0])
            c2 = rec_calc_c(t, S, bags, children[1])
            c_table = c1 + c2 - sum(S) #sum(S) is meant to be nbr of 1s in 1hot S
            
        #by changing last argument to children[0] in recursive calls below we switch to t' from t (node)
        elif node_t == "forget":
            w = set_difference(bags[children[0]], bags[node])
            c_table = max(rec_calc_c(t, S, bags, children[0]), rec_calc_c(t, set_union(S, w), bags, children[0]))
        
        elif node_t == "introduce":
            v = set_difference(bags[node], bags[children[0]]) #The node that is introduced
            if set_intersection(bags[node], v) == empty: 
                c_table = rec_calc_c(t, S, bags, children[0])
            else: 
                c_table = rec_calc_c(t, set_difference(S, v), bags, children[0])

# given a list represetnation of the set, encode it into a binary representation
def binary_encoding(list_set):
    return sum ([1<<i for i in list_set])

# given a binary representation of a set, decode it into a list representation
def binary_decoding(int_set):
    list = []
    while int_set > 0:
        highest_bit = int_set.bit_length() - 1
        list.append(highest_bit) 
        int_set ^=  (1 << highest_bit) # flip highest bit to 0
        print(f" into {int_set:b}")
    return list

def set_union(a, b):
    return a | b

def set_difference(a, b): # given binary representations of 2 sets, find their difference
    return a & ~ b

def set_intersection(a, b): # given binary representations of 2 sets, find their interseciton
    return a & b

def get_node_t(node, children, bags):
    if len(children) > 1:
        return "join"
    elif len(bags[children[0]]) > len(bags[node]): #if child bag is bigger, this is forget
        return "forget"
    else:
        return "introduce" #only option left
            
if __name__ == "__main__":
    g_string = data_path + "BalancedTree_3_5.gr"
    t_string = data_path + "BalancedTree_3_5.td"
    parse_graph(g_string)
    parse_tree(t_string)

    root = make_rooted()
    make_nice()
    n = independent_set()
    print(n) 

    