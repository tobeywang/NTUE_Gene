# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 11:15:43 2018
ACO 螞蟻演算法
@author: 21068X010 王靖瑤
參考來源：https://blog.csdn.net/golden1314521/article/details/45059719

"""
import numpy as np
import matplotlib.pyplot as plt
#城市距離表
distmat = [[0,91.8,105.2,89.9,189.9,76.2,278.3,54.4],
           [91.8,0,187.2,38.9,271.3,162.9,363.3,88.4],
           [105.2,187.2,0,194.1,182.3,31.4,176.1,153.8],
           [89.9,38.9,194.1,0,249.4,166.1,368.3,63.6],
           [189.9,271.3,182.3,249.4,0,168.0,243.0,185.9],
           [76.2,162.9,31.4,166.1,168.0,0,202.2,122.8],
           [278.3,363.3,176.1,368.3,243.0,202.2,0,320.0],
           [54.4,88.4,153.8,63.6,185.9,122.8,320.0,0]]

numant = 40 #螞蟻數量
numcity = 8 #城市個數
alpha = 1   #信息素重要程度因子
beta = 5    #未使用
rho = 0.1   #信息素的蒸發係數
Q = 1 #增加强度系數
#迭代次數
iter = 0
itermax = 250

etatable = 1.0/(distmat+np.diag([1e10]*numcity)) #表示螞蟻从城市i到j的期望程度
pheromonetable  = np.ones((numcity,numcity)) # 信息素矩阵
pathtable = np.zeros((numant,numcity)).astype(int) #路径記錄表


lengthaver = np.zeros(itermax) #各代路徑的平均長度
lengthbest = np.zeros(itermax) #各代及其之前遇到的最佳路徑長度
pathbest = np.zeros((itermax,numcity)) # 各代及其之前遇到的最佳路徑長度


while iter < itermax:


    if numant <= numcity:#城市比螞蟻多
        pathtable[:,0] = np.random.permutation(range(0,1))[:numant]
#        pathtable[:,0] = np.random.permutation(range(0,numcity))[:numant]
    else: #螞蟻比城市多
        pathtable[:numcity,0] = np.random.permutation(range(0,1))[:]
        #皆從第一個城市開始
        pathtable[numcity:,0] = np.random.randint(0,1,size=(1,numant-numcity))
        #np.random.permutation(range(0,numcity))[:numant-numcity]
        
    length = np.zeros(numant) #计算各个蚂螞蟻路徑距離

    for i in range(numant):

        visiting = pathtable[i,0] # 目前所在城市

        visited = set() #已訪問過的城市，不可重覆
        visited.add(visiting) #增加元素
        unvisited = set(range(numcity))#未訪問的城市
        unvisited.remove(visiting) #删除已訪問過(即當前的城市)
        print('未訪問城市:',unvisited)

        for j in range(1,numcity):
            listunvisited = list(unvisited)
            probtrans = np.zeros(len(listunvisited))
            #計算到其他剩下的城市費洛蒙期望程度
            for k in range(len(listunvisited)):
                probtrans[k] = np.power(pheromonetable[visiting][listunvisited[k]],alpha)\
                        *np.power(etatable[visiting][listunvisited[k]],alpha)
            #每一個下個城市費洛蒙/總費洛蒙
            cumsumprobtrans = (probtrans/sum(probtrans)).cumsum()
            cumsumprobtrans -= np.random.rand()
            tempcus=0.0
            print(cumsumprobtrans)
            for ii in range(len(cumsumprobtrans)):
                if(cumsumprobtrans[ii]>0.0 ):
                    k = listunvisited[ii]#下一个要訪問的城市
                    break
            print('下一個要訪問的城市:',k+1)
            pathtable[i,j] = k

            unvisited.remove(k)
            #visited.add(k)

            length[i] += distmat[visiting][k]

            visiting = k

        length[i] += distmat[visiting][pathtable[i,0]] #螞蟻的路徑距離包括最後一個城市和第一個城市的距離

    #每一次迭代後要做的統計
    lengthaver[iter] = length.mean()

    if iter == 0:
        lengthbest[iter] = length.min()
        pathbest[iter] = pathtable[length.argmin()].copy()      
    else:
        if length.min() > lengthbest[iter-1]:
            lengthbest[iter] = lengthbest[iter-1]
            pathbest[iter] = pathbest[iter-1].copy()

        else:
            lengthbest[iter] = length.min()
            pathbest[iter] = pathtable[length.argmin()].copy()    

    # 濃度更新信息素
    changepheromonetable = np.zeros((numcity,numcity))
    for i in range(numant):
        for j in range(numcity-1):
            if(pathtable[i,j]==pathtable[i,j+1]):
                changepheromonetable[pathtable[i,j]][pathtable[i,j+1]] +=0
            else:
                changepheromonetable[pathtable[i,j]][pathtable[i,j+1]] += Q/distmat[pathtable[i,j]][pathtable[i,j+1]]
        if(pathtable[i,j+1]==pathtable[i,0]):
            changepheromonetable[pathtable[i,j+1]][pathtable[i,0]] +=0
        else:
            changepheromonetable[pathtable[i,j+1]][pathtable[i,0]] += Q/distmat[pathtable[i,j+1]][pathtable[i,0]]

    pheromonetable = (1-rho)*pheromonetable + changepheromonetable


    iter += 1 


# 做出平均路徑長度和最優路徑長度        
fig,axes = plt.subplots(nrows=2,ncols=1,figsize=(12,10))
axes[0].plot(lengthaver,'k',marker = u'')
axes[0].set_title('Average Length')
axes[0].set_xlabel(u'iteration')

axes[1].plot(lengthbest,'k',marker = u'')
axes[1].set_title('Best Length')
axes[1].set_xlabel(u'iteration')
fig.savefig('Average_Best.png',dpi=500,bbox_inches='tight')
plt.close()
