import random
from random import randint
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

datapath = os.path.dirname(__file__) + "/data/"
def read_file(path):
    with open(path, "r") as file: 
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
    return A, max_cut_value

def S(G, A = set(), B = set()):
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
                B.add(swap_node) # Swap the selected vertex
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

def R_wrapper(G): 
    _, maxcut =  R(G)
    return maxcut

def print_data(G, algo, filename):
    with open(filename, "w") as file:
        data = [algo(G) for _ in range(100)]
        print ("\nfilename: "+filename)
        print ("average: ", np.average(data))
        print ("max: ", np.max(data))
        data = [str(d) for d in data]
        file.write('\n'.join(data))

# def plot_algo(G, algo, optimal):
#     data = [algo(G) for _ in range(100)]
#     fig, ax = plt.subplots()
#     n, bins, patches = ax.hist(x=data, range=(0,optimal), bins=100) 

#     print(algo)

#     # X ticks/labels trickery
#     ax.set_xbound(lower=0, upper=optimal)
#     ticks = ax.get_xticks()
#     ticks[-1] = optimal
#     ax.set_xticks(ticks)
#     labels = [label.get_text() for label in ax.get_xticklabels()]
#     labels[-1] = "OPT"
#     ax.set_xticklabels(labels)
#     plt.show()

#     print ("average:", np.average(data))
#     print ("max: ", np.max(data))

def main():
    if not os.path.exists("./out"):
        os.mkdir("./out")
    G = read_file(datapath + "pw09_100.9.txt")
    print_data(G, RS, "./out/pw09_RS.txt")
    print_data(G, S, "./out/pw09_S.txt")
    print_data(G, R_wrapper, "./out/pw09_R.txt")
    
    G = read_file(datapath + "matching_1000.txt")
    print_data(G, S, "./out/matching_S.txt")
    print_data(G, RS, "./out/matching_RS.txt")
    print_data(G, R_wrapper, "./out/matching_R.txt")
    # plot_algo(G, R_wrapper, 13658)
    # plot_algo(G, S, 13658)
    # plot_algo(G, RS, 13658)
    
    # plot_algo(G, R_wrapper, 500)
    # plot_algo(G, S, 500)
    # plot_algo(G, RS, 500)
    # #fig.tight_layout() 
    
    # ax[0][0].set_title("pw09_100.9")
    # ax[0][1].set_title("matching_1000")

    # ax[0][0].set_ylabel("R")
    # ax[1][0].set_ylabel("S")
    # ax[2][0].set_ylabel("RS")
    
    plt.show()


if __name__ == "__main__": 
    #G = read_file(datapath + "matching_1000.txt")
    #print(S(G))
    main()



