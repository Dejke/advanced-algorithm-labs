# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:46:15 2023

@author: Isak
"""
#from pathlib import Path
import os
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
        node_t = get_node_t(children, bags) #node type
        #do these for each subset S
        if node_t == "join":
            S_set = powerset(bags[node])
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
            w = set_difference(bags[children[0]], bags[node])
            S_set = powerset(bags[node])
            c1 = rec_calc_c(t, bags, children[0])
            #c2 = rec_calc_c(t, set_union(S, w), bags, children[0])
            for S in S_set:
                c_table[node][S] = max(c1[S], c1[set_union(S, w)])
            return c_table[node]
        
        elif node_t == "introduce":
            v = set_difference(bags[node], bags[children[0]]) #The node that is introduced
            S_set = powerset(bags[node])
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
    return sum ([1<<i for i in list_set])

# given a binary representation of a set, decode it into a list representation
def binary_decoding(int_set):
    list = []
    while int_set > 0:
        highest_bit = int_set.bit_length() - 1
        list.append(highest_bit) 
        int_set ^=  (1 << highest_bit) # flip highest bit to 0
    return list

def set_union(a, b):
    return a | b

def set_difference(a, b): # given binary representations of 2 sets, find their difference
    return a & ~ b

def set_intersection(a, b): # given binary representations of 2 sets, find their interseciton
    return a & b

#finds subsets
def powerset(int_set): 
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
            
if __name__ == "__main__":
    #g_string = data_path + "BalancedTree_3_5.gr"
    #t_string = data_path + "BalancedTree_3_5.td"
    #g_string = Path("BalancedTree_3_5.gr")
    #t_string = Path("BalancedTree_3_5.td")
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    g_rel_path = "data/BalancedTree_3_5.gr"
    t_rel_path = "data/BalancedTree_3_5.td"
    g_string = os.path.join(script_dir, g_rel_path)
    t_string = os.path.join(script_dir, t_rel_path)
    #g_string = Path(__file__).with_name('BalancedTree_3_5.gr')
    #t_string = Path(__file__).with_name('BalancedTree_3_5.td')
    #print(g_string)
    parse_graph(g_string)
    parse_tree(t_string)

    root = make_rooted()
    make_nice()
    n = independent_set()
    print(n) 

    