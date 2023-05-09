import os 
import random
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
    loop = True
    while(loop):
        cut_before = cut(A,E)
        for v in range(1,n+1): 
            swapped_A = swapped(A,v)
            cut_after = cut(swapped_A,E)
            loop = False
            if cut_after > cut_before:
                A = swapped_A
                cut_before = cut_after
                loop = True
    return A

def RS(E, n):
    return S(E, n, A=R(E,n))

def cut(A, E): # determine the size of the cut A over E
    A = set(A) # faster lookups
    return sum([w for (u,v,w) in E if (u in A) != (v in A)])

def printdata(E, n, algo):
    data = [cut(algo(E,n), E) for _ in range(100)]
    print()
    print(algo)
    print("Avg: ", np.average(data))
    print("Max: ", np.max(data))
    for d in data:
        print(d)

def main():
    E, n, m = read_file(DATAFOLDER + "/pw09_100.9.txt")
    printdata(E, n, R)
    printdata(E, n, S)
    printdata(E, n, RS)
    E, n, m = read_file(DATAFOLDER + "/matching_1000.txt")
    printdata(E, n, R)
    printdata(E, n, S)
    printdata(E, n, RS)

if __name__ == "__main__":
    main()