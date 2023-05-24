#https://www.overleaf.com/project/6464b9e359b4ce0ab0a419e6

import random
from random import randint
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import glob
import sys
import time

sys.setrecursionlimit(3000)

datapath = os.path.dirname(__file__) + "/data/"
def read_file(path):
    with open(path, "r") as file: 
        lines = file.readlines()
        G = {}
        line = lines[0]
        #print (line)
        [N, M, H, F, P] = [int(x) for x in line.split()]
        #print(N)
        A = np.zeros(shape=(N,N))
        time_matrix = np.zeros(shape=(N,N))
        b = np.zeros(N)
    
        for i in range(1,len(lines)):
            line=lines[i]
            numbers = line.split()
            n1=int(numbers[0])
            n2=int(numbers[1])
            t = float(numbers[2])
            p1 = float(numbers[3])
            p2 = float(numbers[4])
            A[n1,n2] = p1
            A[n2,n1] = p2
            b[n1] = b[n1] + t*p1
            b[n2] = b[n2] + t*p2
            time_matrix[n1,n2] = t
            time_matrix[n2,n1] = t
            
            if n1 not in G :
                G[n1] =[(n2,p1,t)] #node we go to, with what prob, and time needed
            else :
                G[n1].append((n2,p1,t))
            if n2 not in G :
                G[n2] =[(n1,p2,t)]
            else :
                G[n2].append((n1,p2,t))

        return A, b, N, M, H, F, P, time_matrix

def markov_experiments(infiles):
    results = []
    for file in infiles:
        thisfile = os.path.basename(file)
        A, b, N, M, H, F, P, time_matrix = read_file(file)
        
        subgraph =  get_subgraph(A,H) 

        for i in set(range(N)) - subgraph:
            A[i,:] = np.zeros(N)
            #A[:,i] = np.zeros(N)

        marko = markov(A,b,N)
        row = [thisfile]

        if not F in subgraph:
            row.append("unreachable")
        else:   
            row.append(marko[F])
        if not P in subgraph:
            row.append("unreachable")
        else:   
            row.append(marko[P])
        results.append(row)
    return results
def get_subgraph(A, v):
    """Get the set of vertices that are connected to v in the transition matrix A"""
    AI = A + np.identity(len(A))
    subgraph = {v}
    last = set()
    while subgraph != last:
        last = subgraph
        probs = AI[:, list(subgraph)]
        subgraph = set(np.nonzero(probs.sum(axis = 1).T)[0].flatten())

    return subgraph

def montecarlo_experiments(infiles):
    for file in infiles:
        print()
        A, b, N, M, H, F, P, time_matrix = read_file(file)
        subgraph = get_subgraph(A,H)
        if not {F, P}.issubset(subgraph): # If both are not in grpah
            print(f"F or P can't reach H in graph {os.path.basename(file)}!")
            print()
            continue

        print(f"{os.path.basename(file)} (100 runs avg):")
        results_f = []
        results_p = []
        for i in range (100):
            #ry:
            result_f, result_p = montecarlo(N, H, F, P, A, time_matrix)
            #except: 
            #    print("monte carlo reached recursion depth :(")
            #    continue
            results_f.append(result_f)
            results_p.append(result_p)
        print("F: ", np.average(result_f))
        print("P: ", np.average(result_p))
    
def experiments():
    import pandas as pd 

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    file_dir =  os.path.join(script_dir, "data")
    #onlyfiles = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]
    infiles = glob.glob(os.path.join(file_dir, "*.in"))


    results = []
    for file in infiles:
        thisfile = os.path.basename(file)
        print("\t Monte Carlo - ", thisfile)
        
        A, b, N, M, H, F, P, time_matrix = read_file(file)
        nodes = set()
        print("A= ", A)
        print("H= ", H)
        #nodes_F = get_sub(F, A, nodes)
        #nodes_P = get_sub(P, A, nodes)
        nodes = {H}
        nodes = get_sub_e(H,A,nodes)
        #print("Subgraph from F: ", nodes_F)
        #print("Subgraph from P: ", nodes_P)
        #print("Subgraph to H ", nodes_H)
        if F not in nodes or P not in nodes:
            if F not in nodes:
                print("No delivery from F")
            if P not in nodes:
                print("no delivery from P")
            print("Alen", len(A))
            print("No delivery ajaj")
            continue
        try:
            if thisfile == "toy.in":
                monte_avg_f, monte_avg_p = 0,0
                toy_ans_F = 18.2727272727
                toy_ans_P = 25.5454545455
                start = time.time()
                                
                
                for i in range(10000):
                    monte_f, monte_p = montecarlo(N,H,F,P, A, time_matrix)
                    monte_avg_f += monte_f
                    monte_avg_p += monte_p
                monte_avg_f, monte_avg_p = monte_avg_f/10000, monte_avg_p/10000
                end = time.time()
                print("Elapsed time for 10 000 runs: ", end - start)
                
                acc_F = dig_of_acc(toy_ans_F, monte_avg_f)
                acc_P = dig_of_acc(toy_ans_P, monte_avg_p)
                print("acc_F ", acc_F)
                print("acc_P ", acc_P)
                print("Number of significant digits for 10 000 runs: ", min(acc_F,acc_P))
            print("monte_avg_f, monte_avg_p: ", monte_avg_f, monte_avg_p)
            print("File: ", thisfile)
            monte_f, monte_p = montecarlo(N,H,F,P, A, time_matrix)
            print("FedUps", monte_f)
            print("PostNHL", monte_p)
        except:
            pass
        
    #ansfiles = glob.glob(os.path.join(file_dir, "*.ans"))
    montecarlo_experiments(infiles)

    
    markovresults = markov_experiments(infiles)
    table = pd.DataFrame(markovresults)
    table = table.set_axis(["input graph", "$E[$FedUps$]$", "$E[$PostNHL$]$"], axis = 1)

    print(table.to_latex(escape = False, index = False))

def dig_of_acc(ans, est):        
     acc = abs((ans-est)/ans)
     lead = count_leading_zeroes(acc)
     return lead

    #up to 100 trailing
def count_leading_zeroes(d):
    return int(np.ceil(-np.log10(d)))

def get_sub_e(end, A, nodes):
    #print("getting subgraph starting in ", start)
    for i in range(len(A)):
        #print(A[start][i])
        if A[i][end] > 0 and i not in nodes:
            nodes.add(i)
            nodes = get_sub(i, A, nodes)
            #print(nodes)
    return nodes

def get_sub(start, A, nodes):
    #print("getting subgraph starting in ", start)
    for i in range(len(A)):
        #print(A[start][i])
        if A[start][i] > 0 and i not in nodes:
            nodes.add(i)
            nodes = get_sub(i, A, nodes)
            #print(nodes)
    return nodes
    

def markov(A, b, N):

    return np.linalg.solve(A-np.identity(N), -b)


def montecarlo_loop(N, H, from_node, proba_matrix, time_matrix):
    time = 0
    node = from_node

    while node != H:
        intersections = [i for i in range(N)]
        probabilities = proba_matrix[node]

        nextnode = random.choices(intersections, probabilities, k=1)[0]
        time += time_matrix[node, nextnode]
        node = nextnode
    return time


def montecarlo_rec(N,H,position, proba_matrix, time_matrix, time):
    if position == H:
        return time
    else:
        intersections = [i for i in range(N)]
        probabilities = proba_matrix[position]
        chosen_option = random.choices(intersections, probabilities, k=1)
        time += time_matrix[position, chosen_option][0] 
        return montecarlo_rec(N, H,chosen_option[0], proba_matrix, time_matrix, time)
    
def montecarlo(N, H, F, P, proba_matrix, time_matrix):
    stack = []
#    time_f = montecarlo_rec(N,H,F, proba_matrix, time_matrix,0)
#    time_p = montecarlo_rec(N,H,P, proba_matrix, time_matrix,0)
    time_f = montecarlo_loop(N, H, F, proba_matrix, time_matrix)
    time_p = montecarlo_loop(N, H, P, proba_matrix, time_matrix)
    return time_f, time_p 

def check_same_subset(G, list_neigh,waiting_list):
    h=waiting_list.pop()
    for neigh in G[h]:
        if neigh[0] not in list_neigh :
            waiting_list.add(neigh[0])
    if waiting_list == set():
        return list_neigh
    
def reachable(G, H,T):
    if T in check_same_subset(G,[H], set()):
        return True
    else :
        return False


if __name__ == "__main__":
    
    experiments()
    #sol_quality_small()




    