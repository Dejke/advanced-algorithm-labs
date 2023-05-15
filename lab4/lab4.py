import random
from random import randint
import os
from os import listdir
from os.path import isfile, join
import numpy as np


datapath = os.path.dirname(__file__) + "/data/"
def read_file(path):
    with open(path, "r") as file: 
        lines = file.readlines()
        G = {}
        line = lines[0]
        print (line)
        [N, M, H, F, P] = [int(x) for x in line.split()]
        print(N)
        A = np.zeros(shape=(N,N))
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

def markov(A, b, N):
    return np.linalg.solve(A-np.identity(N), -b)

def main():
    A, b, N, M, H, F, P = read_file("./data/toy.in")
    print(A)
    print(b)
    print(markov(A,b,N))

if __name__:
    main()
