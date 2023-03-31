import random
import numpy as np

treevec = []
N = 0

def is_leaf(index):
    return index > N/2

def is_root(index):
    return index == 1

def sibling (index):
    if index % 2 == 0: # we are left child
        return index + 1
    else:              # we are right child
        return index - 1

def parent (index):
    return index // 2

def left_child (index):
    return 2 * index

def right_child (index):
    return 2 * index + 1

 
def rec_mark_node(index):
    """Mark the node. If a rule applies to any neighbor, update them too"""
    
    if treevec[index]:
        return 0
    treevec[index] = True
    counter = 1

    if not is_leaf(index):
        left = left_child(index)
        right = right_child(index)
        if treevec[left] != treevec[right]: 
            if treevec[left]:
                counter += rec_mark_node(right)
            else:
                counter += rec_mark_node(left)

    if not is_root(index):
        parent_index = parent(index)
        sibling_index = sibling(index)
        if treevec[parent_index] != treevec[sibling_index]:
            if treevec[parent_index]:
                counter += rec_mark_node(sibling_index)
            else:
                counter += rec_mark_node(parent_index)
    return counter   
        
def R1():
    return random.randint(1, N)

def R2():
    l = [i for i in range(1,N)]
    random.shuffle(l)
    return l

def R3():
    l = [i for i in range(1,N)]
    random.shuffle(l)
    return l
#    return np.random.choice(np.where(treevec == False)[0])


def marking1():
    counter = 0
    marked = 0

    index = 0
    while marked<N:
        index = R1()
        counter += 1
        marked += rec_mark_node(index)
    #print(f'LAST MARKED NODE {is_leaf(index)}')
    return(counter)


def marking2():
    counter = 0
    marked=0
    r2_l = R2()
    #print(r2_l)
    while marked<N:
        index = r2_l[counter]
        counter += 1
        marked += rec_mark_node(index)

    return(counter)

def marking3():
    counter = 0
    marked = 0
    r3_l = R3()
    l_index = 0
    while marked<N:
        while treevec[r3_l[l_index]]:
            l_index += 1
        index = r3_l[l_index]
        counter += 1
        l_index += 1
        marked += rec_mark_node(index)

    return(counter)

def calculate(treesize, iterations, markingfunction): 
    """ Run the algorithm (iterations) times, and calculate mean & standard deviation of results
        N is size of tree
        R is sampling function
    """

    # Assign globals 
    global N, treevec
    N = treesize

    lst=[]
    for i in range (iterations):
        
        treevec = np.array([False for _ in range(N+1)], dtype=bool)
        treevec[0] = True # Just so R3 doesn't select the dummy value at the start of treevec
        lst.append(markingfunction())
    mean = sum(lst) / len(lst)
    #print("The mean is :", mean)
    std = (sum([(x - mean) ** 2 for x in lst]) / len(lst)) ** 0.5
    
    return mean, std



def scientific_notation(mean, stdev):
    
    stdexp = np.Infinity
    if stdev != 0:
        # Round both to same sigfig
        stdexp = int(np.log10(stdev))
        mean = np.round(mean / 10**stdexp) * 10**stdexp
        stdev = np.round(stdev / 10**stdexp) * 10**stdexp

    #scientific notation
    meanexp = int(np.log10(mean))
    mean /= 10**meanexp
    stdev /= 10**meanexp

    stdev = f'{stdev:.1g}'

    precision = 2 if stdev == 0 else len(stdev.split('.')[0])
    
    mean = f'{mean:.{precision}f}'   
        
#    return f'{mean} plusminus {stdev} * 10^{meanexp}'
    if meanexp == 0:
        return f'${mean} \\pm {stdev}$'
    else:
        return f'${mean} \\pm {stdev} \\times 10^{meanexp}$'
    
def generate_table(samples = 1, max_power = 20, latex = True):
    """Run all the experiments, and generate a latex table"""
    try: 
        import pandas as pd 
        import tqdm as tqdm
        N = [2**power-1 for power in range(2,max_power+1)]
        funcs = [marking1,marking2,marking3]

        results = []
        for n in tqdm.tqdm(N):
            row  = [str(n)]
            for markingfunction in funcs:
                mean,std = calculate(n, samples, markingfunction)
                row.append(scientific_notation(mean,std))

            ER1 = (n+1)/2 * np.log((n+1) / 4) + np.euler_gamma * (n+1) / 2
            exponent = int(np.log10(ER1))
            ER1 /= 10**exponent
            row.append(f'${ER1:.1f} \\times 10^{exponent}$')
            results.append(row)
        
        df = pd.DataFrame(results)

        df = df.set_axis(["$N$", "$R_1$","$R_2$","$R_3$", "$E[R_1]$"], axis=1)#.join(pd.DataFrame({'E[R1]',["" for _ in N]}))

        if latex:
            print(df.to_latex(escape = False, index = False))
        else:
            print(df)
    except ModuleNotFoundError: 
        print("error: can't generate table without pandas & tqdm packages")

if __name__ == "__main__":
    generate_table(samples=10, max_power=20, latex = True)

    #print(calculate(1023, 1000, marking1))
    #mean, std = calculate(1023, 10, marking1)   
    #print(mean,std)
    #print(scientific_notation(mean,std))



