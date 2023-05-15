import random

def montecarlo_rec(N,H,position, proba_matrix, time_matrix, time=0):
    if position == H:
        return time
    else :
        chosen_option = random.choices([i for i in range(N) if proba_matrix[position][i]!=0], proba_matrix[position], k=1)
        time += time_matrix[position][chosen_option] 
        return montecarlo_rec(N, H,chosen_option, proba_matrix, time_matrix, time=0)
    
def montecarlo(N,H,F,P, proba_matrix, time_matrix):
    time_f = montecarlo_rec(N,H,F, proba_matrix, time_matrix)
    time_p = montecarlo_rec(N,H,P, proba_matrix, time_matrix)
    return time_f, time_p 

A, b, N, M, H, F, P = read_file(datapath)
montecarlo(N,H,F,P, A, time_matrix)

