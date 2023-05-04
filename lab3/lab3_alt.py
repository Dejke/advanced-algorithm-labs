import os 
import random
import matplotlib.pyplot as plt
import numpy as np
#import pyplotlib
DATAFOLDER = dir_path = os.path.dirname(os.path.realpath(__file__)) + "/data"

def read_file(path):
    with open(path) as file:
        E = [] # list of tuples (u,v,w) - (v1, v2, weight)
        [n, m] = file.readline().split() # n = |V|, m = |E|
        while line:=file.readline():
            [u,v,w] = line.split()
            E.append((int(u),int(v),int(w)))
    return E,int(n),int(m)

def R(E, n, m):
    return [v for v in range(1,n+1) if random.randint(0,1) == 1]

def S(E, n, m):
    def swapped(A, v):
        swapped_A = A.copy()
        if v in A:
            swapped_A.remove(v)
        else: 
            swapped_A.append(v)
        return swapped_A
        
    A = [] # Let all vertices be outside of A to begin with

    while True:
        cut_before = cut(A,E)
        candidates = list(range(1,n+1))
        random.shuffle(candidates)
        for v in candidates: # Maybe this should sample randomly, in that case just shuffle 
            swapped_A = swapped(A,v)
            cut_after = cut(swapped_A,E)
            if cut_after > cut_before:
                A = swapped_A
                continue
        break
    return A

def RS(E, n, m):
    pass

def cut (A, E):# determine the size of the cut A over E
    tally = 0
    print(A)
    for (u,v,w) in E:
        A_u = u in A
        A_v = v in A
        if A_u != A_v: # part of the cut
            tally += w
    return tally

def plot_algo(E, n, m, algo):
    data = [cut(algo(E,n,m), E) for i in range(100)]

    print(data)
    counts, bins = np.histogram(np.array(data))
    print(counts, bins)
    plt.stairs(counts, bins)
    plt.show()

def main():
    #E, n, m = read_file(DATAFOLDER + "/matching_1000.txt")
    E, n, m = read_file(DATAFOLDER + "/pw09_100.9.txt")
    #plot_algo(E, n, m, R)
    #print(cut(R(E,n,m), E))
    print(cut(S(E,n,m), E))
if __name__ == "__main__":
    main()