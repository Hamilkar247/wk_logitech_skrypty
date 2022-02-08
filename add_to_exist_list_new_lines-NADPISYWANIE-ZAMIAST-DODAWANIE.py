import csv
import json
from os import lseek
import pprint


######## UWAGA TA WERSJA NADPISUJE caly plik zamiast dodawać na koniec

csv_plik_path = "NOAA-last-day.csv"
json_plik_path = "NOAA-last-day.json"



with open ("NOAA-wzor.json") as json_plik:
    list_json_data = json.load(json_plik)


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


data = {}
with open(csv_plik_path) as csv_plik: 
    for rows in csv_plik:
        print("------")
        #print(rows.split(";"))
        krotka_danych = rows.split(";")
        print(krotka_danych)
        list_of_value=[]
        for wartosc_str in krotka_danych:
            print("----------")
            print(wartosc_str.lstrip())
            print(wartosc_str.lstrip().replace("\n",""))
            list_of_value.append(wartosc_str.lstrip().replace("\n",""))
        list_json_data['dane'].append(list_of_value)

#print(list_json_data)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(list_json_data)

with open("NOAA-last-day.json", "w") as json_plik:
    json.dump(list_json_data, json_plik)

#with open(json_plik_path, "NOAA-last-day.json") as json_plik:
#    json_plik.write()
#    for rows in csvReader:
#        id = rows["id"]
#        data[id] = rows
#
#with open(json_plik_path,"w") as json_file:
#    jsonFile.write(json.dumps(data, indent=4))
