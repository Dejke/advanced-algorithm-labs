import os 
import random
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
    A = [] # Let all vertices be outside of A to begin with

    for v in range(1,n+1):
        pass


def RS(E, n, m):
    pass

def main():
    E, n, m = read_file(DATAFOLDER + "/matching_1000.txt")
    E, n, m = read_file(DATAFOLDER + "/pw09_100.9.txt")
    print(E)
    print(n)
    print(m) 

    print(R(E,n,m))

if __name__ == "__main__":
    main()