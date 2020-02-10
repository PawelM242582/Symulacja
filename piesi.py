from numpy import *
from random import *
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
lambd=16*60 #parametr lambda rozkładu wykładniczego gdzie 1/lambda to wartość oczekiwana
nn_max=100 # ilosć powtórzeń symulacji
clock_start=5*60 # godzina rozpoczęcia działania sygnalizacji świetlnej w systemie 10
clock_stop=22*60 #godzina zakończenia działania sygnalizacji świetlnej w systemie 10
cykl=[1,4]      #cykl trwania światła zielonego i czerwonego
piesi_max=1000 # ilość pieszych 

srednia_sredniej=[]
nn=0

#bezwzględny algorytm upływu czasu
def czas():
    global clock,zdarzenia_czasowe
    clock=min(zdarzenia_czasowe)
    del zdarzenia_czasowe[zdarzenia_czasowe.index(clock)]

#funkcja licząca średnia
def cal_average(num):

    sum_num = 0
    for t in num:
        sum_num = sum_num + t           
    avg = sum_num / len(num)
    return avg

while nn<nn_max:
    #warunki początkowe 
    clock=clock_start
    piesi=[]    
    czerwone=[clock_start] 
    zielone=[clock_start+cykl[1]]
    swiatlo="czerwone"
    #losowanie godzin przyjsć pieszych
    while len(piesi)<piesi_max:
        x=expovariate(1/lambd)
        if x>=clock_start and x<=clock_stop: piesi.append(x)  
    piesi.sort()

    #ustalenie czasów zmiany sygnalizacji świetlnej
    j=1
    while max(czerwone) <= 22*60 or max(zielone)<= 22*60:
        czerwone.append(czerwone[j-1]+cykl[1]+cykl[0])
        zielone.append(zielone[j-1]+cykl[1]+cykl[0])
        j+=1
    czerwone.sort()
    zielone.sort()

    #utworzenie zdarzeń czasowych 
    zdarzenia_czasowe=[]
    for i in range(len(piesi)):
        zdarzenia_czasowe.append(piesi[i])
    for i in range (len(czerwone)):
        zdarzenia_czasowe.append(czerwone[i])
        zdarzenia_czasowe.append(zielone[i])
    zdarzenia_czasowe.sort()  

    oczekiwanie=[]

    #właściwa pętla pojedyńczej symulacji
    while len(zdarzenia_czasowe)>0:

        
        #print(clock/60)
        #print(swiatlo)
        if clock in czerwone: 
            swiatlo="czerwone" 
            del czerwone[czerwone.index(clock)]
        elif clock in zielone:
            swiatlo="zielone"
            del zielone[zielone.index(clock)]
        if clock in piesi and swiatlo=="zielone":
            oczekiwanie.append(0)
            #print("pieszy przechodzi")
        if  clock in piesi and swiatlo=="czerwone":
            oczekiwanie.append(min(zielone)-clock)
            #print("pieszy czeka")
        
        czas()
    #print("średnie oczekiwanie ",cal_average(oczekiwanie))
    #print(oczekiwanie)
    nn+=1
    srednia_sredniej.append(cal_average(oczekiwanie))

#print("średnie ", srednia_sredniej )
tresc=srednia_sredniej
print("średnia średniej  oczekiwania  w minutach",cal_average(tresc))
"""
plik = open('‪plik1.txt','w')
plik.write(str(tresc))
plik.close()"""
for j in range(2):
    try :
        xl_file = r"raport.xls"
        rb = open_workbook(xl_file)
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        sheet.write(0, 0,"bez przycisku")
        for i in range (len(tresc)):
            sheet.write(i+1, 0, tresc[i]*60)
        wb.save(xl_file)
    except FileNotFoundError:
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("sheet1")
        book.save("raport.xls")