# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 15:55:03 2018

−3.0 ≤ x1 ≤ 12.1,  4.1 ≤ x2 ≤ 5.8 
@author: 21068X010
"""

# -*- coding: UTF-8 -*-
import math
import random
import matplotlib.pyplot as plt
history = []#物種適應差集合
adapthis=[]
# 函数
def Rosenbrock(x1,x2):
    sum=21.5+x1*math.sin(4*math.pi*x1)+x2*math.sin(4*math.pi*x2)
    return sum
def get_survivors(adapt,x):
    global show
    adapt,x=zip(*sorted(zip(adapt,x), reverse=True)[:5])
    return adapt,x
# 解碼
def decode(x):
    x1,x2=0,0
    x1=-3.0+(15.1)*(int(x[0:24],2)-0)/(16777215-0)#基因長度:24
    x2=4.1+(1.7)*(int(x[25:46],2)-0)/(2097151-0)#基因長度:21
    return round(x1, 6),round(x2, 6)
def decodeX1(x):
    x1,x2=0,0
    x1=-3.0+(15)*(int(x[0:24],2)-0)/(16777215-0)
    return x1,x2
def decodeX2(x):
    x1,x2=0,0
    x2=4.1+(1.7)*(int(x[25:46],2)-0)/(2097151-0)
    return x1,x2    
# 隨機
def randomX():
    x=''
    for i in range(24+21+1):
        x=x+str(random.randint(0,1))
    return x

def main():
    x=[]
    number=1000
    nc = 20 
    # 1. 族群大小
    for i in range(number):
        x.append(randomX())

    last_total_adapt=0
    this_total_adapt=100000.
    adapt = []
    # 終止條件=走幾代
    while(abs(last_total_adapt-this_total_adapt)>0.1):
        history.append(abs(last_total_adapt-this_total_adapt))
        # 重置
        last_total_adapt = this_total_adapt
        this_total_adapt = 0
#        adapt =[]
        # 2. 計算適應度
        for i in range(len(x)):
            x1, x2 = decode(x[i])
            adapt.append(Rosenbrock(x1, x2))
#        adapt,x=get_survivors(adapt,x)
#        adapt=list(adapt)
#        x=list(x)
        
        # 3. 複製
        minAdapt,minX=adapt[0],0
        maxAdapt,maxX=adapt[0],0
        for i in range(len(x)):
            if(adapt[i]<minAdapt):
                minAdapt, minX = adapt[i], i
            if (adapt[i] > maxAdapt):
                maxAdapt, maxX =  adapt[i], i
        #  適應度最小的讓最大的取代，使得最大的可以有更高機會被選到
        x[minX],adapt[minX]=x[maxX],adapt[maxX]

        # 4. 交配
        for i in range(nc):
            # 每位有千分之5的機率被選出做交配
            ran=random.randint(0,1000)
            if ran>995:
                n1=random.randint(0,len(x)-1)
                n2 = random.randint(0, len(x)-1)
                xa=x[n1]
                xb =x[n2]
                cut_point=random.randint(0,24+21+1)
                xa1 = xa[:cut_point] + xb[cut_point:]
                xb1 = xb[:cut_point] + xa[cut_point:]
                x[n1]=xa1
                x[n2]=xb1
        # 5. 突變
        for i in range(len(x)):
            tempx=x[i]
            for j in range(len(tempx)):
                # 每位有十萬分之2的機率突變
                ran=random.randint(0,100000)
                if ran>99998:
                    if tempx[j] is '1':
                       tempx=tempx[:j]+'0'+tempx[j+1:]
                    else:
                        tempx = tempx[:j] + '1' + tempx[j + 1:]

        # 重算 totoal_adapt
        for i in range(len(x)):
            x1, x2 = decode(x[i])
            adapt.append(Rosenbrock(x1, x2))
            this_total_adapt=this_total_adapt+Rosenbrock(x1, x2)
        adapthis.append(adapt[0])
    print('encode x1:',x[0][0:24])    
    print('encode x2:',x[0][25:46])
    print('decode x1:',decodeX1(x[0]))    
    print('decode x2:',decodeX2(x[0]))
    print ('x1,x2:',decode(x[0]))
    print ('MAX f(x1,x2):',adapt[0])
main()
plt.figure()
plt.title('Convergence process')
plt.axis([0,1600,0,100])
plt.plot(history)
plt.show()

plt.figure()
plt.title('f(x1,x2)')    
plt.plot(adapthis)
plt.show()