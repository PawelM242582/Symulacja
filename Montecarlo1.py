import numpy as np
from matplotlib.pyplot import *
from random import *
from math import pi

listx=[]
listy=[]
def init():
    s=500
    xk=1.5
    xp=0
    wynik=mc(s,xk,xp)
    return wynik
def f(x):

    return (1/ np.sqrt(2*pi)) * np.exp(-(x**2/2))
def mc(s,xk,xp):
    global listx,listy
    score=0
    dx=np.abs(xk-xp)
    for i in range(s):
        x=xp+np.random.uniform(0,1)*(abs(xp-xk))
    
        score+=f(x)
        listx.append(x)
        listy.append(f(x))
    wynik=dx*score/s
    return wynik
w=init()
ww=0.433193
print("całka obliczona numerycznie",w)
print("wynik z kalkulatora ",ww)
print("różnica ", abs(ww-w))
print("błąd ",abs(ww-w)/ww)

