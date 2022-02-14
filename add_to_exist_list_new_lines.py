
# - *- coding: utf- 8 - *-

import csv
import json
import os
import pprint
import sys
import shutil
######## UWAGA TA WERSJA NADPISUJE caly plik zamiast dodawać na koniec

csv_plik_path = "NOAA-last-day.csv"
json_plik_path = "NOAA-last-day.json"
json_wzor= "NOAA-wzor.json"

if os.path.exists(json_plik_path) == True and os.stat(json_plik_path).st_size > 0:
    with open (json_plik_path) as json_plik:
        dane_dotychczasowe_tego_pliku = json.load(json_plik)
else: 
    with open(json_wzor) as json_plik:
        dane_dotychczasowe_tego_pliku = json.load(json_plik)
    shutil.copyfile(json_wzor, json_plik_path)
czas_dotychczasowych_pomiarow=[]
for data_czasowa in dane_dotychczasowe_tego_pliku["data"]:
    czas_dotychczasowych_pomiarow.append(data_czasowa[0])
print("czas_dotychczasowych_pomiarow")
print(czas_dotychczasowych_pomiarow)
print(dane_dotychczasowe_tego_pliku)

#sys.exit()
#przykladowy output 
####print(list_json) 
####print("----------")
####print(list_json['dane'][0])
####print("------------")
####print(list_json['dane'][0][0])
# wyniki
#{'dane': [['Data', 'Zasieg[%]', 'Temp0[°C]' ...]]}
#----------
#['Data', 'Zasieg[%]', 'Temp0[°C]', 'Temp1[°C]' .... ]]}
#------------
#Data
#
# sys.exit()
list_json_data=[]
with open(csv_plik_path) as csv_plik: 
    i=0
    for rows in csv_plik:
        if i==0:
            i=i+1
            continue
        #print("------")
        #print(rows.split(";"))
        krotka_danych = rows.split(";")
        #print(krotka_danych)
        list_of_value=[]
        for wartosc_str in krotka_danych:
            #print("----------")
            #print(wartosc_str.lstrip())
            #print(wartosc_str.lstrip().replace("\n",""))
            element=wartosc_str.lstrip().replace("/n","")
            if element != "":
                list_of_value.append(element)
        list_json_data.append(list_of_value)

###print(list_json_data)
###pp = pprint.PrettyPrinter(indent=4)
###pp.pprint(list_json_data)
#sys.exit()

##print("-------------")
#pprint(print(json_plik))
##print("-------------")

ahoj=""
#'",'.join(list_json_data[0]+'"')
#a=0
# for element in list_json_data[0]:
#     if a==0:
#         a=a+1
#     ahoj.add('"'+element+'"')
czy_dodano_jakis_rekord=False
for j in range(0, len(list_json_data), 1):
    #print("----krotki--------")
    #print(list_json_data[0][0].strip())
    #print(list_json_data[0][1].strip())
    #print(list_json_data[1][0].strip())
    #print(list_json_data[1][1].strip())
    #print(list_json_data[2][0].strip())
    #print(czas_dotychczasowych_pomiarow)
    #print("------------")
    ##sprawdzam czy ten pomiar już przypadkiem nie jest w jsonie
    #print(len(list_json_data))
    #print("j"+str(j))
    if list_json_data[j][0].strip() not in czas_dotychczasowych_pomiarow:
        #print("i"+str(i))
        czy_dodano_jakis_rekord=True
        ahoj=ahoj+"["
        for i in range(0, len(list_json_data[j]), 1):
            ahoj=ahoj+'"'+list_json_data[j][i].strip()+'"' 
            if i != len(list_json_data[j])-1:
                ahoj=ahoj+","
        ahoj=ahoj+"]"+","


#print(ahoj)
if czy_dodano_jakis_rekord:
    #usuwam psujący syntaks przecinek po ostatniej krotce danych
    ahoj = ahoj[:-1]
    #print(ahoj)
    ahoj=ahoj+"]"
    #print(ahoj)
    ahoj=ahoj.replace("/n","")
    #print(ahoj)
    
    with open(json_plik_path, "ab+") as json_plik_do_dodania:
        json_plik_do_dodania.seek(-2, os.SEEK_END)
        json_plik_do_dodania.truncate() # usuwa z pliku trzy ostatnie znaki
        json_plik_do_dodania.write(b",")
        json_plik_do_dodania.write(bytes(ahoj,'utf-8'))
        json_plik_do_dodania.write(b"}")
        json_plik_do_dodania.close()


