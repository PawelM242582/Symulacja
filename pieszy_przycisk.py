from numpy import *
from random import *
from scipy.stats import *
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
p=input("podaj wartości parametru przycisk delay w sekundach oddzielone spacjami")
p=p.split()
for h in range(len(p)):
    lambd=16*60 #parametr lambda rozkładu wykładniczego gdzie 1/lambda to wartość oczekiwana
    nn_max=100 # ilosć powtórzeń symulacji
    clock_start=5*60 # godzina rozpoczęcia działania sygnalizacji świetlnej w systemie 10
    clock_stop=22*60 #godzina zakończenia działania sygnalizacji świetlnej w systemie 10
    duration=60/60   #czas trwania światła zielonego 
    przycisk_delay=int(p[h])/60 #czas po jakim zapala się zielone w minutach w systemie 10
    piesi_max=1000 # ilość pieszych 
    zielone=[]
    czerwone=[]
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

    def p_przycisk(time):
        global zielone, zdarzenia_czasowe
        zielone.append(time+przycisk_delay)
        zdarzenia_czasowe.append(time+przycisk_delay)
        czerwone.append(time+przycisk_delay+duration)
        zdarzenia_czasowe.append(time+przycisk_delay+duration)

    while nn<nn_max:

        clock=clock_start
        piesi=[]
        przycisk=0 # flaga 0 niewcisnięte, 1 wciśnięte
        #losowanie godzin przyjsć pieszych
        while len(piesi)<piesi_max:
            x=expovariate(1/lambd)
            if x>=clock_start and x<=clock_stop: piesi.append(x)  
        piesi.sort()

        swiatlo="czerwone"

        #utworzenie zdarzeń czasowych 
        zdarzenia_czasowe=[]
        for i in range(len(piesi)):
            zdarzenia_czasowe.append(piesi[i])
        for i in range (len(czerwone)):
            zdarzenia_czasowe.append(czerwone[i])
        zdarzenia_czasowe.sort() 

        oczekiwanie=[]
        while len(zdarzenia_czasowe)>0:
            #print(clock/60)
            #print(swiatlo)   

            if clock in czerwone: 
                swiatlo="czerwone" 
                del czerwone[czerwone.index(clock)]
            elif clock in zielone:
                swiatlo="zielone"
                przycisk=0
                del zielone[zielone.index(clock)]

            if clock in piesi:
                if swiatlo=="czerwone":
                    if przycisk==0:
                        przycisk=1
                        p_przycisk(clock)
                        oczekiwanie.append((przycisk_delay))
                        #print("pieszy wciska przycisk")
                    elif przycisk==1:
                        oczekiwanie.append((min(zielone)-clock))
                        #print("pieszy nie wciska")
                elif swiatlo=="zielone":
                    oczekiwanie.append(0)
                    #print("pieszy przechodzi ")
            

            czas()
        #print(oczekiwanie)
        #print("średnie oczekiwanie ",cal_average(oczekiwanie))
        srednia_sredniej.append(cal_average(oczekiwanie))

        nn+=1
    #miara oceny
    #print("średnie ", srednia_sredniej )
    tresc=srednia_sredniej
    print("średnia średniej  oczekiwania w minutach dla opóźnienia ", przycisk_delay*60 ," to ",cal_average(tresc))
    """
    plik = open('‪plik.txt','w')
    plik.write(str(tresc))
    plik.close()
    """

    for j in range(2):
        try :
            xl_file = r"raport.xls"
            rb = open_workbook(xl_file)
            wb = copy(rb)
            sheet = wb.get_sheet(0)
            sheet1 = wb.get_sheet(1)
            sheet.write(0,h+1,"z przyciskiem "+str(przycisk_delay*60))
            sheet1.write(0,h+1,"z przyciskiem srednia "+str(przycisk_delay*60))
            for i in range (len(tresc)):
                sheet.write(i+1, h+1, tresc[i]*60)
            for i in range (len(tresc)):
                sheet1.write(1, h+1, cal_average(tresc))
            wb.save(xl_file)
        except FileNotFoundError:
            book = xlwt.Workbook(encoding="utf-8")
            sheet1 = book.add_sheet("sheet1")
            sheet2 = book.add_sheet("sheet2")
            book.save("raport.xls")