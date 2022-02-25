#!/usr/bin/env python3
# - *- coding: utf- 8 - *-

from inspect import trace
import os
import configparser
import logging
import sys
import traceback
from datetime import datetime

def przerwij_i_wyswietl_czas():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    sys.exit()

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def isdigit(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

class Krotka_Danych(object):
    def __init__(self):
        print("krotka_danych")
        self.data=None
        self.zasieg=None
        self.temp=[
            None,            
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None            
        ]
        #self.temp[0]=None
        #self.temp[1]=None
        #self.temp[2]=None
        #self.temp[3]=None
        #self.temp[4]=None
        #self.temp[5]=None
        #self.temp[6]=None
        #self.temp[7]=None
        #self.temp[8]=None
        self.wilg=[
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,           
            None            
        ]
        #self.wilg[0]=None
        #self.wilg[1]=None
        #self.wilg[2]=None
        #self.wilg[3]=None
        #self.wilg[4]=None
        #self.wilg[5]=None
        #self.wilg[6]=None
        #self.wilg[7]=None
        #self.wilg[8]=None
        self.bat=[
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None
        ]
        #self.bat[0]=None      
        #self.bat[1]=None
        #self.bat[2]=None
        #self.bat[3]=None
        #self.bat[4]=None
        #self.bat[5]=None
        #self.bat[6]=None
        #self.bat[7]=None
        #self.bat[8]=None   

class Przekroczenia(object):

    def __init__(self):
        print("przekroczenia")
        #ścieszki przejścia etc.
        self.path_to_przekroczenia_raport_csv='/var/www/html/weewx/lightlog_sensors/media/csv/przekroczenia.csv' #/var/www/html/weewx/our_site/przekroczenia'
        self.path_to_generated_weewx_file='/var/www/html/weewx/lightlog_sensors/media/csv'
        self.path_to_media_frontend='/var/www/html/weewx/lightlog_sensors/media'
        self.path_to_csv_with_last_record=self.path_to_generated_weewx_file+"/NOAA/"+"NOAA-last-hour copy.csv"

        self.config= configparser.ConfigParser()
        #konfiguracja_globalna
        self.path_to_configuration_ini=self.path_to_media_frontend+"/"+"config/configuration.ini"
        self.zmienne_konfiguracyjne_parsowanie()

        #konfiguracja czujników
        self.path_to_sensors_ini=self.path_to_media_frontend+"/"+'config/sensors.ini'
        self.config.read(self.path_to_sensors_ini)
        sekcje=self.config.sections()
        print(sekcje)
        #przerwij_i_wyswietl_czas()
        for sekcja in sekcje:
            if sekcja != 'configuration':
                print(sekcja)
                self.parsowanie_zmiennych(sekcja)
                #wczytanie csv-ki z ostatnim rekordem
                self.wczytanie_ostatniego_rekordu()
                self.badamy_przekroczenia()
                self.sprawdz_baterie()

                self.wyslij_mejla()
                self.wyslij_smsa()
                self.wyczyszczenie_zmiennych_konfiguracyjnych_czujnika()

    def zmienne_konfiguracyjne_parsowanie(self):
        print("Зродились ми з великої години")
        print("parsowanie_zmienny configuration.ini")
        try:
            self.config.read(self.path_to_configuration_ini)
            configuration='configuration'
            self.telefon_number = self.config.get(configuration, 'telefon_number')
            self.telefon_frequency = self.config.get(configuration, 'telefon_frequency')
            self.email_address=self.config.get(configuration, 'email_address')
            self.email_frequency=self.config.get(configuration, 'email_frequency')
            self.inform_range_disconnected=self.config.getboolean(configuration, 'inform_range_disconnected')
            self.inform_range_disconnected_frequency=self.config.get(configuration, 'inform_range_disconnected_frequency')
            self.time_period_to_inform_after_range_disconnected=self.config.get(configuration, 'time_period_to_inform_after_range_disconnected')
        except AttributeError as e:
            print(e)
            print(traceback.print_exc())
        except Exception as e:
            print("wystapil blad przy parsowaniu zmiennych z configuration.ini")
            print(e)
            print(traceback.print_exc())

    def parsowanie_zmiennych(self, sekcja):
        print("Aeterna Victrix!")
        try:
            #parsowanie zmiennych istniejącego pliku
            self.nazwa_czujnika=sekcja
            self.sensor_id = self.config.get(self.nazwa_czujnika, 'sensor_id')
            self.sensor_name = self.config.get(self.nazwa_czujnika, 'sensor_name')
            self.sensor_number = self.config.get(self.nazwa_czujnika, 'serial_number')
            self.lokalizacja = self.config.get(self.nazwa_czujnika, 'lokalizacja')
            self.data_kalibracji = self.config.get(self.nazwa_czujnika, 'data_kalibracji')
            self.data_nastepnej_kalibracji = self.config.get(self.nazwa_czujnika, 'data_nastepnej_kalibracji')
            self.powiadomienie_o_kalibracji = self.config.get(self.nazwa_czujnika, 'powiadomienie_o_kalibracji')
            self.powiadomienie_o_przekroczeniu_temperatury = self.config.getboolean(self.nazwa_czujnika, 'powiadomienie_o_przekroczeniu_temperatury')
            self.temp_min_stopnie_celsjusza = self.config.get(self.nazwa_czujnika, 'temp_min_stopnie_celsjusza')
            self.temp_max_stopnie_celsjusza = self.config.get(self.nazwa_czujnika, 'temp_max_stopnie_celsjusza')
            self.powiadomienie_o_przekroczeniu_wilgotnosci = self.config.getboolean(self.nazwa_czujnika, 'powiadomienie_o_przekroczeniu_wilgotnosci')
            self.wilgotnosc_min_procent = self.config.get(self.nazwa_czujnika, 'wilgotnosc_min_procent')
            self.wilgotnosc_max_procent = self.config.get(self.nazwa_czujnika, 'wilgotnosc_max_procent')
            self.powiadomienie_bateria = self.config.getboolean(self.nazwa_czujnika, 'powiadomienie_bateria')
            self.powiadomienie_sms = self.config.getboolean(self.nazwa_czujnika, 'powiadomienie_sms')
            self.powiadomienie_email = self.config.getboolean(self.nazwa_czujnika, 'powiadomienie_email')
        except Exception as e:
            print("wystapil błądd przy parsowaniu zmiennych")
            print(traceback.print_exc())
        print(self.nazwa_czujnika)

    def wyczyszczenie_zmiennych_konfiguracyjnych_czujnika(self):
        print("Aeterna Victrix!")
        config = configparser.ConfigParser()
        try:
            #parsowanie zmiennych istniejącego pliku
            config.read(self.path_to_sensors_ini)
            self.nazwa_czujnika=None
            self.sensor_id = None
            self.sensor_name = None 
            self.sensor_number = None
            self.lokalizacja = None 
            self.data_kalibracji = None
            self.data_nastepnej_kalibracji = None
            self.powiadomienie_o_kalibracji = None
            self.powiadomienie_o_przekroczeniu_temperatury = None
            self.temp_min_stopnie_celsjusza = None
            self.temp_max_stopnie_celsjusza = None
            self.powiadomienie_o_przekroczeniu_wilgotnosci = None
            self.wilgotnosc_min_procent = None
            self.wilgotnosc_max_procent = None
            self.powiadomienie_bateria = None
            self.powiadomienie_sms = None
            self.powiadomienie_email = None
        except Exception as e:
            print("wystapil blad przy parsowaniu zmiennych czujnika w sensors.ini")
            print(traceback.print_exc())
        print(self.nazwa_czujnika)

    def transformacja(self, value_str):
        value_str=value_str.split(" " , 1)[0].replace(",",".")
        if isfloat(value_str):
            return float(value_str)
        else:
            return value_str
    

    def wczytanie_ostatniego_rekordu(self):
        with open(self.path_to_csv_with_last_record, "r", encoding="utf-8") as csv_file_last_record:
            krotka = csv_file_last_record.read().split(';')
        #Data;Zasieg[%];Temp0[°C];Temp1[°C];Temp2[°C];Temp3[°C];Temp4[°C];Temp5[°C];Temp6[°C];Temp7[°C];Temp8[°C];Wilgotnosc0[%];Wilgotnosc1[%];Wilgotnosc2[%];Wilgotnosc3[%];Wilgotnosc4[%];Wilgotnosc5[%];Wilgotnosc6[%];Wilgotnosc7[%];Wilgotnosc8[%];Bateria0[%];Bateria1[%];Bateria2[%];Bateria3[%];Bateria4[%];Bateria5[%];Bateria6[%];Bateria7[%];Bateria8[%];
        self.krotka_danych=Krotka_Danych()
        self.krotka_danych.data=krotka[0]
        print(str(self.krotka_danych.data) +" слава")
        self.krotka_danych.zasieg=self.transformacja(krotka[1])
        #self.krotka_danych.temp=[]
        self.krotka_danych.temp[0]=self.transformacja(krotka[2])
        self.krotka_danych.temp[1]=self.transformacja(krotka[3])
        self.krotka_danych.temp[2]=self.transformacja(krotka[4])
        self.krotka_danych.temp[3]=self.transformacja(krotka[5])
        self.krotka_danych.temp[4]=self.transformacja(krotka[6])
        self.krotka_danych.temp[5]=self.transformacja(krotka[7])
        self.krotka_danych.temp[6]=self.transformacja(krotka[8])
        self.krotka_danych.temp[7]=self.transformacja(krotka[9])
        self.krotka_danych.temp[8]=self.transformacja(krotka[10])
        #self.krotka_danych.wilg=[]
        self.krotka_danych.wilg[0]=self.transformacja(krotka[11])
        self.krotka_danych.wilg[1]=self.transformacja(krotka[12])
        self.krotka_danych.wilg[2]=self.transformacja(krotka[13])
        self.krotka_danych.wilg[3]=self.transformacja(krotka[14])
        self.krotka_danych.wilg[4]=self.transformacja(krotka[15])
        self.krotka_danych.wilg[5]=self.transformacja(krotka[16])
        self.krotka_danych.wilg[6]=self.transformacja(krotka[17])
        self.krotka_danych.wilg[7]=self.transformacja(krotka[18])
        self.krotka_danych.wilg[8]=self.transformacja(krotka[19])
        #self.krotka_danych.bat=[]
        self.krotka_danych.bat[0]=self.transformacja(krotka[20])      
        self.krotka_danych.bat[1]=self.transformacja(krotka[21])
        self.krotka_danych.bat[2]=self.transformacja(krotka[22])
        self.krotka_danych.bat[3]=self.transformacja(krotka[23])
        self.krotka_danych.bat[4]=self.transformacja(krotka[24])
        self.krotka_danych.bat[5]=self.transformacja(krotka[25])
        self.krotka_danych.bat[6]=self.transformacja(krotka[26])
        self.krotka_danych.bat[7]=self.transformacja(krotka[27])
        self.krotka_danych.bat[8]=self.transformacja(krotka[28])        

    def badamy_przekroczenia(self):
        self.czy_przekroczylo_temperature()
        self.czy_przekroczylo_wilgotnosc()

    def wpis_do_przekroczen(self, wpis, typ): #, typ, wartosc_z_jednostka):
        #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda zapis
        print(wpis)
        with open(self.path_to_przekroczenia_raport_csv, "a", encoding="utf-8") as plik_do_przekroczen:
            plik_do_przekroczen.write(wpis+"\n")
        plik_do_przekroczen.close()
        print("Dodano przekroczenie typu "+typ)

    def sprawdz_baterie(self):
        print("kyiv not kiev - padająca bateria")
        wartosc_baterii=self.krotka_danych.bat[int(self.sensor_id)]
        print(wartosc_baterii)
        if isdigit(wartosc_baterii):
            if int(wartosc_baterii) == 1:
                #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda zapis
                typ="Bateria"
                wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+"-"+";"+"-"+";"+str(wartosc_baterii)+";"
                self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                print("brak sygnału o niskim poziomie baterii")
        else:
            print("N\A " + wartosc_baterii)
            print("nie ma alarmu o słabej baterii "+wartosc_baterii)


    def czy_przekroczylo_temperature(self):
        print("plurimos annos - temperatura")
        wartosc_temperatury=self.krotka_danych.temp[int(self.sensor_id)]
        typ="Temperatura"
        if isfloat(wartosc_temperatury):
            wartosc_z_jednostka=str(wartosc_temperatury)+" °C"
            if isfloat(self.temp_min_stopnie_celsjusza):
                if float(wartosc_temperatury) < float(self.temp_min_stopnie_celsjusza):
                    print("przekroczenie - za niska temperatura")
                    #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda krotka
                    wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+str(self.temp_min_stopnie_celsjusza)+";"+str(self.temp_max_stopnie_celsjusza)+";"+wartosc_z_jednostka+";"
                    self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                print("brak ogranicznika temperatury minimalnej")
            if isfloat(self.temp_max_stopnie_celsjusza):
                if float(wartosc_temperatury) > float(self.temp_max_stopnie_celsjusza):
                    print("przekroczenie - za wysoka temperatura")
                    wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+str(self.temp_min_stopnie_celsjusza)+";"+str(self.temp_max_stopnie_celsjusza)+";"+wartosc_z_jednostka+";"
                    self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                print("brak ogranicznika temperatury maksymalnej")
        else:
            print("brak danych na temat zmierzonej temperatury")
            print(self.temp0)

    def czy_przekroczylo_wilgotnosc(self):
        print("plurimos annos - wilgotnosc"),
        wartosc_wilgotnosc=self.krotka_danych.wilg[int(self.sensor_id)]
        typ="Wilgotność"
        if isfloat(wartosc_wilgotnosc):
            wartosc_z_jednostka=str(wartosc_wilgotnosc)+" %"
            if isfloat(self.wilgotnosc_min_procent):
                if float(wartosc_wilgotnosc) < float(self.wilgotnosc_min_procent):
                    print("przekroczenie - za niska wilgotnosc") 
                    #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda krotka
                    wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+str(self.wilgotnosc_min_procent)+";"+str(self.wilgotnosc_max_procent)+";"+wartosc_z_jednostka+";"
                    self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                print("brak ogranicznika wilgotnosci minimalnej")
            if isfloat(self.wilgotnosc_max_procent):
                if float(wartosc_wilgotnosc) > float(self.wilgotnosc_max_procent):
                    print("przekroczenie - za wysoka wilgotność")
                    #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda krotka
                    wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+str(self.wilgotnosc_min_procent)+";"+str(self.wilgotnosc_max_procent)+";"+wartosc_z_jednostka+";"
                    self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                print("brak ogranicznika wilgotnosci maksymalnej") 
        else:
            print("brak danych na temat zmierzonej wilgotności")

    def wyslij_mejla(self):
        pass
   
    def wyslij_smsa(self):
        pass
    

if __name__ == "__main__":

    #inicjalizacja
    przekroczenia=Przekroczenia()

