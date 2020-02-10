import numpy as np
from matplotlib.pyplot import *
from random import *
N=500
ml,cl,kl,wl=[],[],[],[]
def srednia(x):
    return sum(x)/len(x)
for i in range (N):
    m=np.random.uniform(1000,2000)
    ml.append(m)
    c=np.random.uniform(450,550)
    cl.append(c)
    k=np.random.uniform(300,400)
    kl.append(k)
    w=np.random.uniform(100000,200000)
    wl.append(w)
z=srednia(ml)*(srednia(cl)-srednia(kl))-srednia(wl)

print("przewidywany zysk", z)
