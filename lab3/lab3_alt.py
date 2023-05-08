import os 
import random
import matplotlib.pyplot as plt
import numpy as np
DATAFOLDER = dir_path = os.path.dirname(os.path.realpath(__file__)) + "/data"

def read_file(path):
    with open(path) as file:
        E = [] # list of tuples (u,v,w) - (v1, v2, weight)
        [n, m] = file.readline().split() # n = |V|, m = |E|
        while line:=file.readline():
            [u,v,w] = line.split()
            E.append((int(u),int(v),int(w)))
    return E,int(n),int(m)

def R(E, n):
    return [v for v in range(1,n+1) if random.randint(0,1) == 1]

def S(E, n, A = []):
    def swapped(A, v):
        if v in A:
            return [a for a in A if not a == v] # remove v
        else: 
            return A + [v] # append v
    def bestswap(A):
        cut_before = cut(A,E)
        candidates = list(range(1,n+1))
        for v in candidates: 
            swapped_A = swapped(A,v)
            cut_after = cut(swapped_A,E)
            if cut_after > cut_before:
                return swapped_A, True
        return A, False
    
    A = [] # Let all vertices be outside of A to begin with
    loop = True
    while(loop):
        A, loop = bestswap(A)
    return A

def RS(E, n):
    return S(E, n, A=R(E,n))

def cut (A, E):# determine the size of the cut A over E
    tally = 0
    print(A)
    for (u,v,w) in E:
        A_u = u in A
        A_v = v in A
        if A_u != A_v: # part of the cut
            tally += w
    return tally

def plot_algo(E, n, m, algo, optimum):
    data = [cut(algo(E,n,m), E) for i in range(100)]

    print(data)
    counts, bins = np.histogram(np.array(data))
    print(counts, bins)
    #bins = np.array([int(val) for val in bins])
    plt.stairs(counts, bins)
    plt.pyplot.xlim(left=0,right=optimum)
    plt.show()

def main():
    #E, n, m = read_file(DATAFOLDER + "/matching_1000.txt")
    E, n, m = read_file(DATAFOLDER + "/pw09_100.9.txt")
    plot_algo(E, n, m, R, optimum = 13658)
    #print(cut(R(E,n,m), E))
    print(cut(S(E,n,m), E))
if __name__ == "__main__":
    main()