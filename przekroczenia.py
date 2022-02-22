#!/usr/bin/env python3
# - *- coding: utf- 8 - *-

import os
import configparser
import logging

class Przekroczenia(object):

    def __init__(self):
        print("przekroczenia")
        #ścieszki przejścia etc.
        self.path_to_przekroczenia_raport='/var/www/html/weewx/our_site/przekroczenia'
        self.path_to_generated_weewx_file='/var/www/html/weewx/our_site'
        self.path_to_csv_with_last_record=self.path_to_generated_weewx_file+"/NOAA/"+"NOAA-last-hour copy.csv"
        self.path_to_przekroczenia_csv=self.path_to_generated_weewx_file+"/przekroczenia/"+"przekroczenia.csv"

        #konfiguracja
        self.path_to_konfiguracja_file=self.path_to_generated_weewx_file+"/"+'konfiguracja/konfiguracja.ini'
        os.chdir(self.path_to_generated_weewx_file)
        self.parsowanie_zmiennych()

        #wczytanie csv-ki z ostatnim rekordem
        self.wczytanie_ostatniego_rekordu()
        self.czy_przekroczylo_temperature()

    
    def wczytanie_ostatniego_rekordu(self):
        with open(self.path_to_csv_with_last_record, "r", encoding="utf-8") as csv_file_last_record:
            line = csv_file_last_record.read().split(';')
        #Data;Zasieg[%];Temp0[°C];Temp1[°C];Temp2[°C];Temp3[°C];Temp4[°C];Temp5[°C];Temp6[°C];Temp7[°C];Temp8[°C];Wilgotnosc0[%];Wilgotnosc1[%];Wilgotnosc2[%];Wilgotnosc3[%];Wilgotnosc4[%];Wilgotnosc5[%];Wilgotnosc6[%];Wilgotnosc7[%];Wilgotnosc8[%];Bateria0[%];Bateria1[%];Bateria2[%];Bateria3[%];Bateria4[%];Bateria5[%];Bateria6[%];Bateria7[%];Bateria8[%];
        print(line)
        self.data=line[2]
        self.temp0=float(line[2].split(" ", 1)[0].replace(",","."))
        print(self.temp0)


    def parsowanie_zmiennych(self):
        print("Aeterna Victrix!")
        config = configparser.ConfigParser()
    
        #parsowanie zmiennych istniejącego pliku
        config.read(self.path_to_konfiguracja_file)
        self.nazwa_czujnika="czujnik0"
        self.sensor_id = config.getint(self.nazwa_czujnika, 'sensor_id')
        self.sensor_name = config.get(self.nazwa_czujnika, 'sensor_name')
        self.sensor_number = config.get(self.nazwa_czujnika, 'serial_number')
        self.lokalizacja = config.get(self.nazwa_czujnika, 'lokalizacja')
        self.data_kalibracji = config.get(self.nazwa_czujnika, 'data_kalibracji')
        self.data_nastepnej_kalibracji = config.get(self.nazwa_czujnika, 'data_nastepnej_kalibracji')
        self.powiadomienie_o_kalibracji = config.getboolean(self.nazwa_czujnika, 'powiadomienie_o_kalibracji')
        self.powiadomienie_o_przekroczeniu_temperatury = config.getboolean(self.nazwa_czujnika, 'powiadomienie_o_przekroczeniu_temperatury')
        self.temp_min_stopnie_celsjusza = config.getint(self.nazwa_czujnika, 'temp_min_stopnie_celsjusza')
        self.temp_max_stopnie_celsjusza = config.getint(self.nazwa_czujnika, 'temp_max_stopnie_celsjusza')
        self.powiadomienie_o_przekroczeniu_wilgotnosci = config.getboolean(self.nazwa_czujnika, 'powiadomienie_o_przekroczeniu_wilgotnosci')
        self.wilgotnosc_min_procent = config.getint(self.nazwa_czujnika, 'wilgotnosc_min_procent')
        self.wilgotnosc_max_procent = config.getint(self.nazwa_czujnika, 'wilgotnosc_max_procent')
        self.powiadomienie_bateria = config.getboolean(self.nazwa_czujnika, 'powiadomienie_bateria')
        self.powiadomienie_sms = config.getboolean(self.nazwa_czujnika, 'powiadomienie_sms')
        self.powiadomienie_email = config.getboolean(self.nazwa_czujnika, 'powiadomienie_email')
        print(self.nazwa_czujnika)


    def wpis_do_przekroczen(self, typ):
        #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda zapis
        wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.data)+";"+str(typ)+";"+str(self.temp_min_stopnie_celsjusza)+";"+str(self.temp_max_stopnie_celsjusza)+";"+str(self.temp0)+";"
        print(wpis)
        #
        
        #    line = plik_do_przekroczen.read().split(';')
        with open(self.path_to_przekroczenia_csv, "a", encoding="utf-8") as plik_do_przekroczen:
            plik_do_przekroczen.write(wpis+"\n")
        plik_do_przekroczen.close()
        print("Dodano przekroczenie typu "+typ)


    def czy_przekroczylo_temperature(self):
        print("plurimos annos")
        if self.temp0 < self.temp_min_stopnie_celsjusza:
            print("przekroczenie - za niska temperatura") 
            self.wpis_do_przekroczen(typ="Temperatura")
        elif self.temp0 > self.temp_max_stopnie_celsjusza:
            print("przekroczenie - za wysoka temperatura")
            self.wpis_do_przekroczen(typ="Temperatura")
        else:
            print("nie ma przekroczenia - dziękuje że leci pan w naszych liniach")
    

if __name__ == "__main__":

    #inicjalizacja
    przekroczenia=Przekroczenia()


    ##########config.set('section_a', 'string_val', 'world')
    ##########print('heri coit statim')
    ##########config.add_section('section_b')
    ##########config.set('section_b', 'meal_val', 'spam')
    ##########config.set('section_b', 'not_found_val', '404')
    ##########with open(path_to_konfiguracja_file, 'w', encoding="utf-8") as configfile:
    ##########    config.write(configfile)
###    with open('test
###    print(config["DEFAULT"]["path"])
###    print(config["DEFAULT"]["ahjo"])
###    config["DEFAULT"]["path"] = 'moj ci'
###    config["DEFAULT"]["default_message"] = "kurla"
###    print(config["DEFAULT"]["path"])
###    with open('konfiguracja.ini', 'w') as configfile:
###        config.write(configfile)
