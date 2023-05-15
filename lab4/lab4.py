import numpy as np
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
        numbers = line.split()
        N, M, H, F, P = numbers
        A = np.array(np.zeros(N,N))
        b = np.array(np.zeros(N))
    
        for i in range(1,len(lines)):
            line=lines[i]
            numbers = line.split()
            n1=int(numbers[0])
            n2=int(numbers[1])
            t=int(numbers[2])
            p1 = int(numbers(3))
            p2 = int(numbers(4))
            A[n1,n2] = p1
            A[n2,n1] = p2
            b[n1] = b[n1] + t*p1
            b[n2] = b[n2] + t*p2
            
            if n1 not in G :
                G[n1] =[(n2,p1,t)] #node we go to, with what prob, and time needed
            else :
                G[n1].append((n2,p1,t))
            if n2 not in G :
                G[n2] =[(n1,p2,t)]
            else :
                G[n2].append((n1,p2,t))
        return A, b, N, M, H, F, P


#def markov(G, )