import random
from random import randint
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

datapath = os.path.dirname(__file__) + "/data/"
#file = open("c:/docs/cs/2Asuede/advanced algorithm/pw09_100.9.txt", "r")
def read_file(path):
    file = open(path, "r")
    lines = file.readlines()
    G = {}

    for i in range(1,len(lines)):
        line=lines[i]
        numbers = line.split()
        n1=int(numbers[0])
        n2=int(numbers[1])
        w=int(numbers[2])
        if n1 not in G :
            G[n1] =[(n2,w)]
        else :
            G[n1].append((n2,w))
        if n2 not in G :
            G[n2] =[(n1,w)]
        else :
            G[n2].append((n1,w))
    return G

def R(G):
    A=[]
    for v in G:
        if randint(0,1)==1:
            A.append(v)
    max_cut_value = sum([G[node][neigh][1] for node in A for neigh in range(len(G[node])) if not neigh in A]) 
    print(max_cut_value)
    return A, max_cut_value


#print (R(G))


def S(G, A = set(), B = set()):
    
    #A = set()
    #B = set()
    # Initialize all vertices as outside of set A
    if(len(B) == 0):
        for node in G:
            B.add(node)
    max_gain = 0
    while True:
        # Find the first vertex that increases the cut if swapped
        swap_node = None
        Bcopy = set(B)
        for node in Bcopy:
            gain = max_gain +sum([G[node][neigh][1] for neigh in range(len(G[node])) if G[node][neigh][0] in B]) -sum([G[node][neigh][1] for neigh in range(len(G[node])) if G[node][neigh][0] in A])
            if gain > max_gain:
                max_gain = gain
                swap_node = node
                B.remove(swap_node)
                A.add(swap_node)
        Acopy = set(A)
        for node in Acopy:
            gain = max_gain +sum([G[node][neigh][1] for neigh in range(len(G[node])) if G[node][neigh][0] in A]) -sum([G[node][neigh][1] for neigh in range(len(G[node])) if G[node][neigh][0] in B])
            if gain > max_gain:
                max_gain = gain
                swap_node = node
                A.remove(swap_node)
                B.add(swap_node)        # Swap the selected vertex
        # If no vertex increases the cut, terminate the algorithm
        if swap_node is None:
            break
    # Calculate and return the maximum cut value
    max_cut_value = sum([G[node][neigh][1] for node in A for neigh in range(len(G[node])) if G[node][neigh][0] in B]) 
    return max_cut_value



def RS(G):
    A, _ = R(G)
    A = set(A)
    B = set(G.keys()) - A
    #print(A,B)
    max_cut = S(G, A, B)
    return max_cut

def R_wrapper(G): # 
    _, maxcut =  R(G)
    return maxcut

def plot_algo(G, algo):
    data = [algo(G) for i in range(100)]

    print(data)
    counts, bins = np.histogram(np.array(data))
    print(counts, bins)
    plt.stairs(counts, bins)
    plt.show()

def main():
    print("R: ")
    R(G)
    print ("S: ", S(G))
    print("RS: ", RS(G))

if __name__ == "__main__":
    G = read_file(datapath + "pw09_100.9.txt")
    plot_algo(G, R_wrapper)
    plot_algo(G, S)
    plot_algo(G, RS)

#    G = read_file(datapath + "pw09_100.9.txt")



