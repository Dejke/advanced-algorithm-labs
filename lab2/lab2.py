# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:46:15 2023

@author: Isak
"""
#from pathlib import Path
import os
from os import listdir
from os.path import isfile, join
import glob
import threading
import _thread
from threading import Thread
from threading import Event
from time import sleep
from multiprocessing import Process

data_path = "./data/"

from itertools import chain, combinations

def parse_graph(g_string):
    g = {}
    n_v = 0
    with open(g_string) as g_file:
        while True:
            l = g_file.readline()
            #print("reading start: ", l)
            syms = l.split()
            if syms[0] == 'p':
                n_v = int(syms[2])
                n_e = int(syms[3])
                break
        for l in g_file:
            vertices = l.split()
            #print(vertices)
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
    return g, n_v


def parse_tree(t_string):
    t = {}
    bags = {}
    tree_w = 0
    with open(t_string) as t_file:
        while True:
            l = t_file.readline()
            #print("reading start: ", l)
            syms = l.split()
            if syms[0] == 's':
                num_bags = int(syms[2])
                tree_w = int(syms[3])-1
                num_v = int(syms[4])
                break     
        for l in t_file:
            vertices = l.split()
            ##print(vertices)
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
                #   #print(g[v1])
                v2 = int(vertices[1])
                
                if t.get(v1): #if already in dict
                    t[v1].append(v2)
                else:
                    t[v1] = [v2]
                if t.get(v2): #if already in dict
                    t[v2].append(v1)
                else:
                    t[v2] = [v1]
    return t, bags, tree_w
            
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
global g

def independent_set(t, bags, root):
    global empty
    global c_table
    c_table = {} #table of tables (first key (which bag/table (t in pdf))) bag_nbr : value table(dict) of c_values with key subset (S in pdf, binary enc) : value c_value))
    return rec_calc_c(t, bags, root) #start from root, root looks at children values etc recursively

def independent_set_p(t, bags, root):
    global empty
    global c_table
    c_table = {} #table of tables (first key (which bag/table (t in pdf))) bag_nbr : value table(dict) of c_values with key subset (S in pdf, binary enc) : value c_value))
    return rec_calc_c_p(t, bags, root)    

#want c values for each subset- for each node -> dictionary of dictionaries, with outer key
#being node and inner being subset -> binary encoding i guess
#t is tree of nodes, bags is node contents, node is current node in tree
# assuming bags contains key bag_nbr : val binary_enc_of_bagset
# and t contains key bag_nbr : val list of children's bag nbrs


def get_node_t(node, children, bags):
    if len(children) > 1:
        return "join"
    #one vertex difference -> binary rep bigger if it has the extra element
    elif len(bags[children[0]]) > len(bags[node]): #if child bag is bigger, this is forget
        return "forget"
    else:
        return "introduce" #only option left

def rec_calc_c(t, bags, node):
    #print("reccalc for node", node)
    children = t[node] #list of children
    
    global c_table
    global g
    empty = frozenset({})  #should be right
    
    if not children:  #leaf node -> base case
        #print("node : ", node, " is a leaf, returning")
        c_table[node] = {empty:0} #only subset is empty set in leaf
        return {empty:0} #probably a dictionary later, with S as key? maybe value can be set + c?
    
    else: 
        node_t = get_node_t(node, children, bags) 
        if node_t == "join":
            c1 = rec_calc_c(t, bags, children[0])
            #print("new ctable entry: ", c_table[children[0]])
            #c_table[children[0]] = ... ^
            c2 = rec_calc_c(t, bags, children[1])
            c_table[node] = {} #need to create empty dict first
            #dont need to redo this, one call to rec_calc should calculate for all subsets 
            for S in spowerset(bags[node]): #for each subset           
                if is_independent_set(g, S):
                    c_table[node][S] = c1[S] + c2[S] - len(S) 
                else:
                    c_table[node][S] = -float('inf')
            del c_table[children[0]]
            del c_table[children[1]]
            return c_table[node]
        #by changing last argument to children[0] in recursive calls below we switch to t' from t (node)
        elif node_t == "forget":
            w = bags[children[0]] - bags[node] #the node that is forgotten
            c1 = rec_calc_c(t, bags, children[0])
            c_table[node] = {} #need to create empty dict first
            for S in spowerset(bags[node]): # for every subset
                if is_independent_set(g, S):
                    c_table[node][S] = max(c1[S], c1[S | w])
                else:
                    c_table[node][S] = -float('inf')
            del c_table[children[0]]
            return c_table[node]
        
        elif node_t == "introduce":
            #print("Introduce node")
            v = bags[node] - bags[children[0]] #The node that is introduced
            c1 = rec_calc_c(t, bags, children[0])
            c_table[node] = {} #need to create empty dict first'
            #print(node)
            #print(bags[node])
            for S in spowerset(bags[node]):
                if is_independent_set(g, S):
                    if S & v == empty: 
                        c_table[node][S] = c1[S]
                        #rec_calc_c(t, bags, children[0])
                    else: 
                        c_table[node][S] = c1[S - v]+1 #the 1 for having 1 more node after introduce
                        #rec_calc_c(t, set_difference(S, v), bags, children[0])
                else:
                    c_table[node][S] = -float('inf')
            del c_table[children[0]]
            return c_table[node]

global interrupted
def rec_calc_c_p(t, bags, node):
    #print("reccalc for node", node)
    global interrupted
    # if event.is_set() or interrupted:
    #     interrupted = True
        
    #     return "interrupted"
    children = t[node] #list of children
    
    global c_table
    global g
    
    empty = frozenset({})  #should be right
    
    if not children:  #leaf node -> base case
        #print("node : ", node, " is a leaf, returning")
        c_table[node] = {empty:0} #only subset is empty set in leaf
        return {empty:0} #probably a dictionary later, with S as key? maybe value can be set + c?
    
    else: 
        node_t = get_node_t(node, children, bags) 
        if node_t == "join":
            c1 = rec_calc_c(t, bags, children[0])
            if interrupted:
                return {empty:0}
            #print("new ctable entry: ", c_table[children[0]])
            #c_table[children[0]] = ... ^
            c2 = rec_calc_c(t, bags, children[1])
            if interrupted:
                return {empty:0}
            c_table[node] = {} #need to create empty dict first
            #dont need to redo this, one call to rec_calc should calculate for all subsets 
            for S in spowerset(bags[node]): #for each subset           
                if is_independent_set(g, S):
                    c_table[node][S] = c1[S] + c2[S] - len(S) 
                else:
                    c_table[node][S] = -float('inf')
            del c_table[children[0]]
            del c_table[children[1]]
            return c_table[node]
        #by changing last argument to children[0] in recursive calls below we switch to t' from t (node)
        elif node_t == "forget":
            w = bags[children[0]] - bags[node] #the node that is forgotten
            c1 = rec_calc_c(t, bags, children[0])
            if interrupted:
                return {empty:0}
            c_table[node] = {} #need to create empty dict first
            for S in spowerset(bags[node]): # for every subset
                if is_independent_set(g, S):
                    c_table[node][S] = max(c1[S], c1[S | w])
                else:
                    c_table[node][S] = -float('inf')
            del c_table[children[0]]
            return c_table[node]
        
        elif node_t == "introduce":
            #print("Introduce node")
            v = bags[node] - bags[children[0]] #The node that is introduced
            c1 = rec_calc_c(t, bags, children[0])
            if interrupted:
                return {empty:0}
            c_table[node] = {} #need to create empty dict first'
            #print(node)
            #print(bags[node])
            for S in spowerset(bags[node]):
                if is_independent_set(g, S):
                    if S & v == empty: 
                        c_table[node][S] = c1[S]
                        #rec_calc_c(t, bags, children[0])
                    else: 
                        c_table[node][S] = c1[S - v]+1 #the 1 for having 1 more node after introduce
                        #rec_calc_c(t, set_difference(S, v), bags, children[0])
                else:
                    c_table[node][S] = -float('inf')
            del c_table[children[0]]
            return c_table[node]

def spowerset(s):
    return [frozenset(tup) for tup in chain.from_iterable(combinations(s,r) for r in range(len(s)+1))]
    
def root_fine(t, bags, root):
    new_root = root
    #index = len(bags)
    if bags[root]: #if not empty list
        n=len(bags[root]) #changed so n is number of vertices in root bag
        index = len(bags)+1 #next index not used by tree yet
        node = bags[root] 
        node_child = root
        for i in range(n):
            node = node[1:len(node)]
            bags[index]=node
            t[index] =[node_child]
            node_child = index
            index +=1
        new_root = index-1
    return (t,bags,new_root)

def leaf_fine(t, bags):
    index = len(bags) + 1
    for bag in range(1, index) : #bag = bag_nbr/node_nbr
             
        if not t[bag]: #if bag is a leaf
            #print(bag, " is a leaf")
            if bags[bag]:#if bag is not empty
                node = bags[bag]
                n = len(node)
                #del(node[0])
                node = node[1:len(node)]
                bags[index]=node
                t[bag] = [index]
                t[index] = [index+1]
                index +=1
                for i in range(1,n):
                    #del(node[0])
                    node = node[1:len(node)]
                    bags[index]=node
                    if i!=n-1: #if it is not the final leaf
                        t[index] = [index+1]
                        index +=1
                    else : 
                        t[index]=[]
                        index += 1
    return t, bags

def one_leaf(t, bags,leaf):
    new_leaf = leaf
    index = len(bags) + 1          
    if bags[leaf]:#if bag is not empty
        node = bags[leaf]
        n = len(node)
        #del(node[0])
        node = node[1:len(node)]
        bags[index]=node
        t[index] =[leaf]
        index +=1
        for i in range(1,n):
            #del(node[0])
            node = node[1:len(node)]
            bags[index]=node
            if i!=n-1: #if it is not the final leaf
                t[index] = [index+1]
                index +=1
            else : 
                t[index]=[]
        new_leaf = index
    return t, bags,new_leaf

def join_split(t, bags):
    index = len(bags) + 1
    for node in range(1,index):
        node_index = node #initially we have this, then it switches to join-nodes
        if len(t[node]) > 1: #if its a split node #NOTE: maybe check so not join already
            parent_bag = t[node]
            while(len(parent_bag) > 1):
                t[index] = [parent_bag[0]]
                bags[index] = bags[node_index]
                
                t[index+1] = parent_bag[1:len(parent_bag)] #NOTE: maybe count children, make many joints without assigning all children - first
                bags[index+1] = bags[node_index]
                
                t[node_index] = [index, index+1] #old parent now only has 2 children with identical bags
                node_index = index+1 # new "parent node" that should be split with join
                
                 #create 2 identical children for join node, 1 gets one of original
                 #node's children as child, other gets the rest - repeat with new parent node
                
                index = index + 2
                parent_bag = t[node_index]
                
    return t, bags
                

def between_nodes(t, bags):
    index = len(bags) + 1
    for parent in range(1, len(t)+1):
        enfants = t[parent]
        for i in range(len(enfants)):
            # print("Enfants: ", enfants)
            child = enfants[i]

            parentbag = set(bags[parent])
            childbag  = set(bags[child])
            to_introduce = parentbag - (parentbag & childbag)
            to_forget = childbag - (parentbag & childbag)
            # print("to_introduce", to_introduce)
            # print("to_forget", to_forget)
             
            if to_forget:         
                to_forget.pop()
            elif to_introduce: # non-empty
                to_introduce.pop()
            else:
                continue

            #del(t[parent][i])
            new_node = parent 
            
            for node in to_introduce:
                # print("INtroducing", node)
                if new_node == parent:                
                    t[parent][i] = index
                else: 
                    t[new_node] = [index]

                new_node = index
                
                parentbag.remove(node)
                bags[new_node] = list(parentbag)
                index += 1

            for node in to_forget:
                # print("Forgetting", node)
                if new_node == parent:                
                    t[parent][i] = index
                else: 
                    t[new_node] = [index]

                new_node = index

                parentbag.add(node)
                bags[new_node] = list(parentbag)
                index += 1

            
            
            if new_node==parent:
                # print("newnode = ", new_node)
                t[new_node][i] = child
            else:
                t[new_node] = [child]
    return t, bags
            


    #         firstchild = t[v][0]
    #         del(t[v][0])
    #         t,bags,highest = root_fine(t,bags,x)
    #         t, bags,new_leaf = one_leaf(t, bags, v)
    #         t[new_leaf].append(highest)
    # return t, bags


def make_nice(t,bags,root):
    # print("Root:",root)
    t,bags,root = root_fine(t, bags,root)  
    #print("bags when root empty", bags)
    #print("tree with empty root:", t, "root:", root)
    t, bags = leaf_fine(t, bags)
    
    # print("bags when leaves/root empty", bags)
    # print("tree with empty leaves:", t, "root:", root)
    t, bags = between_nodes(t, bags)
    # print("bags when between is fixed", bags)
    # print("tree when between is fixed:", t, "root:", root)
    t, bags = join_split(t, bags)
    
    #make set rep in bags
    #print(bags)
    for i in bags.keys():
        bags[i] = set(bags[i])
#    bags = [set(bag) for bag in bags]
    return t, bags, root

def is_independent_set(G, vertices):
    for v in vertices:
        if v not in G:
            return False  # v is not a vertex in G
        for u in G[v]:
            if u in vertices:
                return False  # u is a neighbor of v in vertices
    return True

def is_independent_set_v2(G, vertices):
    for u in G: 
        for v  in G[u]:
            if u in vertices and v in vertices :
                return False 
    return True

def calc_indep_set(g_string, t_string, instance):
    global g
    t = {}
    bags = {}
    g,n_v = parse_graph(g_string)
    t, bags, tw = parse_tree(t_string)
    #print(t)
    root, t = make_rooted(t)
    t, bags, root = make_nice(t,bags, root)
    result = independent_set(t, bags, root) #_p for parallell
    with open("./output.tex", "a") as outfile:
        fixedname = instance.replace("_", "\\_")
        output = f"{fixedname} & $ {n_v} $ & $ {tw} $ & $ {result[frozenset()]} $ \\\\\n" 
        outfile.write(output)#c_table[root][0])
        print(output, end='')

if __name__ == "__main__":
        #to rep graph... all edges in a list? 
    #a dict with vertices as keys and lists of edges(pairs of vertex-nums) as values?
    # Internet - key vertex, value list of neighbours
    
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
    file_dir =  os.path.join(script_dir, "data")
    onlyfiles = sorted([f for f in listdir(file_dir) if isfile(join(file_dir, f))])
    grfiles = sorted(glob.glob(os.path.join(file_dir, "*.gr")))
    tdfiles = sorted(glob.glob(os.path.join(file_dir, "*.td")))
    g_rel_path = "data/AhrensSzekeresGeneralizedQuadrangleGraph_3.gr"
    t_rel_path = "data/AhrensSzekeresGeneralizedQuadrangleGraph_3.td"
    g_string = os.path.join(script_dir, g_rel_path)
    t_string = os.path.join(script_dir, t_rel_path)
    
    #g_string = Path(__file__).with_name('BalancedTree_3_5.gr')
    #t_string = Path(__file__).with_name('BalancedTree_3_5.td')
    #print(g_string)
    
    global g
    files = list(zip(grfiles, tdfiles))
    del files[0]
    file_n = 0
    global interrupted
    for g_string, t_string in files:
        interrupted = False
        #event = threading.Event()
        t = {} 
        bags = {}
        #note g should also reset but this is done in parse_graph
        #print(g_string, t_string)
        #g_string = files[1][0]
        #t_string = files[1][1]
        #print(onlyfiles[file_n], onlyfiles[file_n+1])
        
        thread = Process(target=calc_indep_set, args=(g_string, t_string, onlyfiles[file_n].split('.')[0]))
        file_n = file_n +2
        #thread.setDaemon(True)
        thread.start()
        thread.join(timeout=60)
        thread.terminate()
        #event.set()
        # g = parse_graph(g_string)
        # parse_tree(t_string)
    
        # root, t = make_rooted(t)
        # # print("bags:", bags)
        # # print("tree:", t)
        # t, bags, root = make_nice(t,bags, root)
        # # print("Finished tree decomp")
        # # #print("bags:", bags)
        # # #print("tree:",t)
        # result = independent_set(t, bags, root)
        # print(result)
        global c_table
        #print(c_table)
        # print(g_string, ":\t", result)#c_table[root][0])

    