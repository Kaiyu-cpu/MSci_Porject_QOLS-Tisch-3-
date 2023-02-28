#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 21:25:41 2023

@author: hukaiyu
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

def fitness(V):
    return V-np.log10(1-V)

def fitness_wrong(V):
    return V-np.log(1-V)

#%% BO
df1 = pd.DataFrame()
df1 = pd.read_csv("0223_BO_records/Bayesian_0223.csv")


df2 = pd.DataFrame()
df2 = pd.read_csv("Bayesian_0224.csv")
df = pd.concat([df1,df2])

#%% BO

for i in range (17):
    plt.title("{}".format(i))
    plt.plot(df.iloc[i][1:])
    plt.show()

#%% GA

df = pd.DataFrame()
df = pd.read_csv("Pygad_record.csv")

Big_list=[]
for i in range(8):
    x = df.iloc[i][1:]
    iter_list = []
    for j in range(0,len(x),8):
        sub_section = x[j:j+8]
        iter_list.append(max(sub_section))
            
    #plt.plot(iter_list)
    plt.show()
    Big_list.append(iter_list)
  
ensemble = pd.DataFrame(Big_list)

temp=np.linspace(0,1,1000)
y=[]
for i in temp:
    y.append(fitness_wrong(i))
V_ensemble=[]
for i in range (8):
    V_ensemble.append (np.interp(ensemble.iloc[i], y, temp))


#%% BO
good =[0,2,4,5,9,10,11,12]
ensemble=[]
for i in good:
    ensemble.append(df.iloc[i][1:])

temp=np.linspace(0,99,1000)
y=[]
for i in temp:
    y.append(fitness(i))
V_ensemble=[]
for i in range (len(good)):
    V_ensemble.append (np.interp(ensemble[i], y, temp))


#%% Both (BO99, GA100)
V_ensemble = pd.DataFrame(V_ensemble)

mean=V_ensemble.mean(axis=0)

std=V_ensemble.std(axis=0)

x=np.linspace(0,100,101)

fig, ax1 = plt.subplots(figsize=(9, 6))

plt.grid()
ax2 = ax1.twinx()

ax1.plot(x,mean,color='blue')
xtick=np.linspace(0,100,11)
ax1.set_xticks(xtick)
#ax1.set_yticks([0.5,0.7,0.9,1.1,1.3,1.5])

ax1.fill_between(x, mean-std/2, mean+std/2, alpha=0.3,color='g',edgecolor='white')
ax1.set_ylabel("Visibility",fontsize=15)
ax1.set_xlabel("Generation",fontsize=15)

ax1.tick_params(labelsize=15)
ax2.tick_params(labelsize=15)


ax2.set_ylabel("Fitness function",fontsize=15)
#ax2.plot(x,V,color='red')
#ax2.set_yticks([])

formatter = mticker.FuncFormatter(lambda x, pos:'{:.1f}'.format(x-np.log10(1-x)))
ax2.yaxis.set_major_formatter(formatter)
ax1.set_ylim(0.65,1)
ax2.set_ylim(ax1.get_ylim())
plt.show()




