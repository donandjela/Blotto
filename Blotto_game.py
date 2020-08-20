#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 23:34:35 2018

@author: Andjela Donevic
"""

import numpy as np
import timeit


def RandoStrat(init, n):
    res = init
    strat = []
    
    for i in range(n-1):
        rand = np.random.randint(0,res)
        strat.append(rand)
        res -= rand
    strat.append(res)
    np.random.shuffle(strat)
    return strat


# simulation of the game similar to function rezultat
def play_game(lista1, lista2):
    prvi = []
    poeni = range(10)
    
    for i,j in zip(lista1, lista2):
        if i-j>0:
            prvi.append(1)
        else:
            prvi.append(0)
            
    rez = np.dot(poeni,prvi)
            
    return (prvi, rez)    


#returns list of best strategies
"""
If the opponent wins we take his strategy
If we win threshold or more consecutive times we consider 
that strategy good and we add it ti the list of best strategies

"""
def find_best_strategies():
    ind = 0
    threshold = 300

    base_strategy = RandoStrat(100, 10)
    best = []
    i = 0
    while i<10: # i< number of strategies wanted 
        player_2_strategy = RandoStrat(100, 10)
    
        (first, res1) = play_game(base_strategy, player_2_strategy)
        (second, res2) = play_game(player_2_strategy,base_strategy)
    
        if res2 > res1:
            base_strategy = player_2_strategy
            ind=0
        ind+=1
        #print(ind)
        if ind>=threshold:
            
            if base_strategy not in best:
                best.append(base_strategy)
                i+=1
                print(i)
        
    return best

'''modified version where player one has init number of soldiers
   divided to 10 castles
   
   with init < 100 we are less likely to win so we set threshold = 150
   with init > 100 we are more likely to win so we set threshold = 310 
'''
    
def find_best_strategies_mod(init,threshold):
    ind = 0
    #threshold = 300

    base_strategy = RandoStrat(init, 10)
    best = []
    i = 0
    while i<10: # i< number of strategies wanted
        player_2_strategy = RandoStrat(100, 10)
    
        (first, res1) = play_game(base_strategy, player_2_strategy)
        (second, res2) = play_game(player_2_strategy,base_strategy)
    
        if res2 > res1:
            base_strategy = RandoStrat(init, 10)
            ind=0
        ind+=1
        #print(ind)
        if ind>=threshold:
            
            if base_strategy not in best:
                best.append(base_strategy)
                i+=1
                print(i)
        
    return best

start = timeit.timeit()


#best = find_best_strategies()
#best = find_best_strategies_mod(110,310)

best = find_best_strategies_mod(90,150)
print(best,'\n')
end = timeit.timeit()
print('Time:', end - start)

    

with open("best_strategies_00.txt","w") as f:
    for line in best:
        for ch in line:
            f.write(str(ch)+' ')
        f.write('\n')
    
    
    


# In[ ]:


import numpy as np
import pandas as pd

#generates list of strategies for players
def RandoStrat(init, n):
    res = init
    strat = []
    
    for i in range(n-1):
        rand = np.random.randint(0,res)
        strat.append(rand)
        res -= rand
    strat.append(res)
    np.random.shuffle(strat)
    return strat

'''calculates the result of game for first player with strategy lisit1
prvi: list "1" on  i-th place inidates that player won i-th casle
rez: points won in a game versus player with strategy given as list2
'''

def rezultat(lista1, lista2):
    prvi = []
    poeni = range(10)
    
    for i,j in zip(lista1, lista2):
        if i-j>0:
            prvi.append(1)
        else:
            prvi.append(0)
            
    rez = np.dot(poeni,prvi)
            
    return (prvi, rez)
            
'''
player one enters tournament with strategy given as lista1 and plays versus #dim opponents
function returns:
pobede : number of victories in this tournament
avg_rez : average points won in tournament
'''
        
def test(lista1, dim = 10000):
    pobede = []
    poeni = 0
    for i in range(dim):
        lista2  = RandoStrat(5,3)+ RandoStrat(40,4) + RandoStrat(55,3)
        l1,rez1 = rezultat(lista1,lista2)
        l2,rez2 = rezultat(lista2, lista1)
       
        if rez1>rez2:
            pobede.append(1)
            poeni += rez1
        else:
            pobede.append(0)
           
    avg_rez = poeni/dim
    return (pobede, avg_rez)


"""
player enters #dim tournaments with strategy given as lista1
function returns list ans with elements:

min(avg): Minimum number of vicories in #dim tournaments
max(avg): Maximum number of victories in #dim tournaments
sum(avg)/dim: Average number of victories in #dim tournaments
max(avg) - min(avg): Gap between minimum and maximum value, low gap is preferred
rez1 : average points won

"""

def avg_test(lista1,dim = 10):
    
    avg = []
    
    for i in range(dim):
        
        pobede, rez1 = test(lista1)
        pobeda = sum(pobede)
        avg.append(pobeda)
        
        
        
    '''ans = {"MIN": min(avg), 'MAX': max(avg),'AVG_WIN': sum(avg)/dim,
           'GAP': max(avg) - min(avg), 'AVG_POINTS' : rez1
           }
    '''
    
    ans = [min(avg), max(avg), sum(avg)/dim, max(avg) - min(avg), rez1 ]
        
        
        
    print(avg)
    print('MIN',min(avg))
    print('MAX',max(avg))
    print('AVG',sum(avg)/dim )
    print('GAP', max(avg) - min(avg))
    
    
    return ans

# checks list entry: correct numbers of troups -> sum, number of castles -> duzina
# if bad entry returns False, if good returns True
def proveri_unos(lista, suma = 100, duzina=10):
    
    if sum(lista) != suma:
        print('LOSA LISTA')
        return False
        
    if len(lista) != duzina:
        print('LOSA DUZINA')
        return False   
    return True
        
with open('best_strategies_00.txt','r') as f:
    lines = [[int(x) for x in line.split()]for line in f]
    print(lines)


data = pd.DataFrame(columns = ['MIN', 'MAX', 'AVG_WIN','GAP','AVG_POINTS'],
                    index = range(len(lines))
                   )

lines = pd.Series(lines)
print(lines)

i = 0
for line in lines:
    
    rez = avg_test(line)
    
    print(rez)
    
    data.iloc[i] = rez
    i +=1
    
print(data)

data['Lists'] = lines

data.to_excel('data_00_blotto.xls') 


# In[ ]:




