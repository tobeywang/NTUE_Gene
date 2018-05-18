# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 15:44:13 2018

@author: Python35
"""

# genetic algorithm
from numpy import random
import matplotlib.pyplot as plt
import math

# environment
err = 0.5  # error tolerance 交配率
ns = 5  # number of survivor 每代留下幾個最好的基因
nc = 20  # number of child 一個基因生下幾個孩子
gens = 100  # generation 
mu=0.05

#交配
def get_childs(parents):
    value=[round(parent + random.randn()*err,6)
            for _ in range(nc)
            for parent in parents]
#    print("選擇前:",value)
    return value
#複製
def get_survivors(offsprings, f):
    #留下值最大的前五個(ns)
    return sorted(offsprings, key=f, reverse=True)[:ns]

#突變
def get_mutation(offsprings):
    value=[(offspring+random.randn()*mu)
            for _ in range(1) #只突變一次
            for offspring in offsprings]
    return value                    
def ga(f, guess, lb=0,le=0):
    parents = [guess]
    history = []
    for _ in range(gens):
        offsprings = [child for child in get_childs(parents)
                      if child >= lb and child<=le]
#        print("選擇後:",offsprings)            
        survivors = get_survivors(offsprings, f)
        #突變
        mutations=[child for child in get_mutation(survivors)
                    if child>lb and child <le]
        parents = mutations
        history.append(max(mutations))
#        print("MAX:",max(survivors))
    return history,max(mutations)


if __name__ == '__main__':
    # problem
    f=lambda x1:x1*math.sin(4*math.pi*x1)
    f2=lambda x2:x2*math.sin(4*math.pi*x2)
#   f = lambda x1,x2:21.5+x1*math.sin(4*math.pi*x1)+x2*math.sin(4*math.pi*x2)
    history,sur = ga(f, guess=1.,lb=-3.0,le=12.0)
    #X1基因長度24 000000000000000000000000=-3.0
    history2,sur2 = ga(f2, guess=4.1,lb=4.1,le=5.8)
    #X2基因長度21 00000000000000000000=4.0
    print('X1 :',sur)
    print('X2 :',sur2)
    print("MAX f(x1,x2):",21.5+sur+sur2)

    maxhistory=[]    
    if len(history)== len(history2):
        for i in range(len(history)):
            maxhistory.append(21.5+history[i]+history2[i])
    plt.figure()
    ax =plt.subplot(2,2,1)
    ax.set_title('X1')
    plt.plot(history)
    ax =plt.subplot(2,2,2)
    ax.set_title('X2')    
    plt.plot(history2)  
    plt.show()
    plt.figure()
    plt.plot(maxhistory)
    plt.show()