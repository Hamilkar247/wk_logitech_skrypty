# - *- coding: utf- 8 - *-

import csv
import json
import os
import pprint


######## UWAGA TA WERSJA NADPISUJE caly plik zamiast dodawać na koniec

csv_plik_path = "NOAA-last-day.csv"
json_plik_path = "NOAA-last-day.json"


flag_not_exist_file=False
if os.path.exists(json_plik_path):
    flag_not_exist_file=False
else:
    flag_not_exist_file=True 
    open(json_plik_path, 'a').close()

with open ("NOAA-last-day.json") as json_plik:
    dane_dotychczasowe_tego_pliku = json.load(json_plik)


#przykladowy output 
####print(list_json) 
####print("----------")
####print(list_json['dane'][0])
####print("------------")
####print(list_json['dane'][0][0])
# wyniki
#{'data': [['Data', 'Zasieg[%]', 'Temp0[°C]' ...]]}
#----------
#['Data', 'Zasieg[%]', 'Temp0[°C]', 'Temp1[°C]' .... ]]}
#------------
#Data
#

list_json_data=[]
with open(csv_plik_path) as csv_plik: 
    i=0
    for rows in csv_plik:
        if i==0:
            i=i+1
            continue
        print("------")
        #print(rows.split(";"))
        krotka_danych = rows.split(";")
        print(krotka_danych)
        list_of_value=[]
        for wartosc_str in krotka_danych:
            print("----------")
            #print(wartosc_str.lstrip())
            #print(wartosc_str.lstrip().replace("\n",""))
            element=wartosc_str.lstrip().replace("/n","")
            if element != "":
                list_of_value.append(element)
        list_json_data.append(list_of_value)

#print(list_json_data)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(list_json_data)




print("-------------")
#pprint(print(json_plik))
print("-------------")

ahoj="["
#'",'.join(list_json_data[0]+'"')
#a=0
# for element in list_json_data[0]:
#     if a==0:
#         a=a+1
#     ahoj.add('"'+element+'"')

for i in range(0, len(list_json_data[0]), 1):
    print(ahoj)
    ahoj=ahoj+'"'+list_json_data[0][i].strip()+'"' 
    if i != len(list_json_data[0])-1:
        ahoj=ahoj+","
print(ahoj)
ahoj=ahoj+"]"
print(ahoj)
ahoj=ahoj.replace("/n","")
print(ahoj)
with open("NOAA-last-day.json", "ab+") as json_plik_do_dodania:
    json_plik_do_dodania.seek(-2, os.SEEK_END)
    json_plik_do_dodania.truncate()         # usuwa z pliku trzy ostatnie znaki
    json_plik_do_dodania.write(b",")
    json_plik_do_dodania.write(bytes(ahoj,'utf-8'))
    json_plik_do_dodania.write(b"]}")
    json_plik_do_dodania.close()


