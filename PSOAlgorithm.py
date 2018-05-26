# -*- coding: utf-8 -*-
"""
Created on Sat May 26 13:09:05 2018

@author: 20168x010
"""

import numpy as np    
import random     
import matplotlib.pyplot as plt    
import math
  
#----------------------PSO參數---------------------------------    
class PSO():    
    def __init__(self,pN,dim,max_iter):    
        self.w = 0.8    #速度權重  
        self.c1 = 2     #單組粒子最佳解速度權重  
        self.c2 = 2     #全的最佳解速度權重  
        self.r1= 0.6    #單組粒子亂數
        self.r2=0.3     #全體粒子亂數
        self.pN = pN                #粒子組總数量    
        self.dim = dim              #幾個變數    
        self.max_iter = max_iter    #迭代次数    
        self.X = np.zeros((self.pN,self.dim))       #所有粒子的位置    
        self.V = np.zeros((self.pN,self.dim))       #所有粒子的速度
        self.pbest = np.zeros((self.pN,self.dim))   #最佳位置    
        self.gbest = np.zeros((1,self.dim))         #最好的粒子組
        self.p_fit = np.zeros(self.pN)              #每組粒子歷史算出最佳值    
        self.fit = 1e10             #粒子群最佳值    
            
#---------------------目標函數-----------------------------    
    def function(self,x):    
        sum = 0    
        sum=x[0]**2+2*(x[1]**2)-0.3*math.cos(3*math.pi*x[0])-0.4*math.cos(4*math.pi*x[1])+0.7
        return sum  
#---------------------初始化----------------------------------    
    def init_Population(self):    
        for i in range(self.pN):    
            for j in range(self.dim):    
                self.X[i][j] = random.uniform(-100,100)    
                self.V[i][j] = random.uniform(-100,100)    
            self.pbest[i] = self.X[i]    
            tmp = self.function(self.X[i])    
            self.p_fit[i] = tmp    
            #排序粒子組
            if(tmp < self.fit):    
                self.fit = tmp    
                self.gbest = self.X[i]    
        
#----------------------更新粒子位置----------------------------------    
    def iterator(self):    
        fitness = []    
        for t in range(self.max_iter):    
            for i in range(self.pN):         #更新gbest\pbest    
               temp = self.function(self.X[i])    
               if(temp<self.p_fit[i]):      #更新粒子組最佳解    
                   self.p_fit[i] = temp    
                   self.pbest[i] = self.X[i]    
                   if(self.p_fit[i] < self.fit):  #更新全體最佳解    
                       self.gbest = self.X[i]    
                       self.fit = self.p_fit[i]    
            for i in range(self.pN):    
                #速度權重x粒子速度+最佳解速度權重*亂數*本身最佳解-粒子位置+全體最佳解速度權重*亂數*全體最佳解位置-粒子位置
                self.V[i] = self.w*self.V[i] + self.c1*self.r1*(self.pbest[i] - self.X[i]) + self.c2*self.r2*(self.gbest - self.X[i])    
                #粒子最新位置=上一個粒子位置+速度
                self.X[i] = self.X[i] + self.V[i]    
            fitness.append(self.fit)    
#            print(self.fit)                   #輸出最佳解    
        return fitness    
   
#----------------------Run-----------------------    
my_pso = PSO(pN=30,dim=2,max_iter=100)    
my_pso.init_Population()    
fitness= my_pso.iterator()  
print("最佳解Z:",my_pso.fit)
print("X1,X2:",my_pso.gbest)
#-------------------收斂圖--------------------    
plt.figure(1)    
plt.title("Figure1")    
plt.xlabel("iterators", size=14)    
plt.ylabel("fitness", size=14)    
t = np.array([t for t in range(0,100)])    
fitness = np.array(fitness)    
plt.plot(t,fitness, color='b',linewidth=3)    
plt.show()   