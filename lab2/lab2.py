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
root = -1 #index of root node, assigned later
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
    pass

def make_nice():
    pass

def independent_set():
    pass
            
if __name__ == "__main__":
    

    g_string = data_path + "BalancedTree_3_5.gr"
    t_string = data_path + "BalancedTree_3_5.td"
    parse_graph(g_string)
    parse_tree(t_string)
    make_rooted()
    make_nice()
    n = independent_set()
    print(n) 

    