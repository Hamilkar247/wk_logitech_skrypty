#!/usr/bin/env python3
# - *- coding: utf- 8 - *-

from inspect import trace
import os
import configparser
import logging
import sys
import traceback
from datetime import datetime
import shutil

def wyswietl_czas():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

def przerwij_i_wyswietl_czas():
    wyswietl_czas()
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

def nazwa_programu():
    return "przekroczenie.py"

def data_i_godzina():
    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    return current_time

def drukuj(obiekt_do_wydruku):
    try:
        print(data_i_godzina()+" "+nazwa_programu()+" "+str(obiekt_do_wydruku))
    except Exception as e:
        print(e)
        print(traceback.print_exc())

class Krotka_Danych(object):
    def __init__(self):
        drukuj("krotka_danych")
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

class Przekroczenia(object):

    def __init__(self):
        drukuj("przekroczenia - init")
        #ścieszki przejścia etc.
        self.path_to_przekroczenia_raport_csv='/var/www/html/weewx/lightlog_sensors/media/csv/przekroczenia.csv' #/var/www/html/weewx/our_site/przekroczenia'
        self.path_to_generated_weewx_file='/var/www/html/weewx/lightlog_sensors/media/csv'
        self.path_to_media_frontend='/var/www/html/weewx/lightlog_sensors/media'
        self.path_to_csv_with_last_record=self.path_to_generated_weewx_file+"/NOAA/"+"NOAA-last-hour.csv"

        self.config=configparser.ConfigParser()
        #konfiguracja_globalna
        self.path_to_configuration_ini=self.path_to_media_frontend+"/"+"config/configuration.ini"
        self.zmienne_konfiguracyjne_parsowanie()

        #konfiguracja czujników
        self.path_to_sensors_ini=self.path_to_media_frontend+"/"+'config/sensors.ini'
        self.config.read(self.path_to_sensors_ini)
        sekcje=self.config.sections()
        drukuj(sekcje)
        self.wczytanie_ostatniego_rekordu()
        self.czas_poprz_przekroczenia=''
        self.wczytaj_czas_ostatniego_przekroczenia()
        #przerwij_i_wyswietl_czas()
        drukuj(self.czas_poprz_przekroczenia)
        if self.czas_poprz_przekroczenia != self.krotka_danych.data:  
            for sekcja in sekcje:
                if sekcja != 'configuration': #sprawdzam czy to nie sekcja nie zwiazana z czujnikami
                    drukuj(sekcja)
                    self.parsowanie_zmiennych_sensorowych(sekcja)
                    #wczytanie csv-ki z ostatnim rekordem

                    self.badamy_przekroczenia()
                    self.sprawdz_baterie()

                    self.wyslij_mejla()
                    self.wyslij_smsa()
                    self.wyczyszczenie_zmiennych_konfiguracyjnych_czujnika()
            self.nadpisz_czas_ostatniego_zbadanego_przekroczenia() #ODKOMENTOWANIE PRZY TESTACH - ZAKOMENTOWANIE PRZY PRODUKCJI
        else:
            drukuj("nie ma nowego rekordu do sprawdzenia")
        
    def wczytaj_czas_ostatniego_przekroczenia(self):
        drukuj("wczytaj_czas_ostatniego_przekroczenia")
        path_czas_ostatnie_przekroczenie=self.path_to_generated_weewx_file+"/"+"czas_ostatniego_przekroczenia.txt"
        if os.path.exists(path_czas_ostatnie_przekroczenie):
            with open(path_czas_ostatnie_przekroczenie, "r", encoding="utf-8") as plik_z_czas_zbad_rekordu:
                self.czas_poprz_przekroczenia=plik_z_czas_zbad_rekordu.read()
        else:
            with open(path_czas_ostatnie_przekroczenie, 'w') as fp:
                pass
                self.czas_poprz_przekroczenia=''

    def nadpisz_czas_ostatniego_zbadanego_przekroczenia(self):
        drukuj("nadpisz_czas_ostatniego_zbadanego_przekroczenia")
        path_czas_ostatnie_przekroczenie=self.path_to_generated_weewx_file+"/"+"czas_ostatniego_przekroczenia.txt"
        if os.path.exists(path_czas_ostatnie_przekroczenie):
            with open(path_czas_ostatnie_przekroczenie, "w", encoding="utf-8") as plik_z_czas_zbad_rekordu:
                self.czas_poprz_przekroczenia=plik_z_czas_zbad_rekordu.write(self.krotka_danych.data)

    def zmienne_konfiguracyjne_parsowanie(self):
        drukuj("parsowanie_zmiennych_konfiguracyjnych configuration.ini")
        try:
            self.config.read(self.path_to_configuration_ini)
            configuration='configuration'
            self.telefon_number = self.config.get(configuration, 'telefon_number')
            self.telefon_frequency_hour = self.config.get(configuration, 'telefon_frequency_hour')
            self.email_address = self.config.get(configuration, 'email_address')
            self.email_frequency_hour = self.config.get(configuration, 'email_frequency_hour')
            self.inform_range_disconnected=self.config.getboolean(configuration, 'inform_range_disconnected')
            self.inform_range_disconnected_frequency_hour=self.config.get(configuration, 'inform_range_disconnected_frequency_hour')
            self.time_period_to_inform_after_range_disconnected_hour=self.config.get(configuration, 'time_period_to_inform_after_range_disconnected_hour')
        except AttributeError as e:
            drukuj("AttributeError - błąd")
            print(e)
            print(traceback.print_exc())
        except Exception as e:
            drukuj("wystapil blad przy parsowaniu zmiennych z configuration.ini")
            print(e)
            print(traceback.print_exc())

    def parsowanie_zmiennych_sensorowych(self, sekcja):
        drukuj("parsowanie_zmiennych_sensorowych sensors.ini")
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
            drukuj("wystapił błąd przy parsowaniu zmiennych")
            print(e)
            print(traceback.print_exc())
        drukuj(self.nazwa_czujnika)

    def wyczyszczenie_zmiennych_konfiguracyjnych_czujnika(self):
        drukuj("wyczyszczenie_zmiennych_konfiguracyjnych_czujnika")
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
            drukuj("wystapil blad przy parsowaniu zmiennych czujnika w sensors.ini")
            print(traceback.print_exc())
        drukuj(self.nazwa_czujnika)

    def transformacja(self, value_str):
        value_str=value_str.split(" " , 1)[0].replace(",",".")
        if isfloat(value_str):
            return float(value_str)
        else:
            return value_str
    

    def wczytanie_ostatniego_rekordu(self):
        drukuj("wczytanie_ostatniego_rekordu")
        with open(self.path_to_csv_with_last_record, "r", encoding="utf-8") as csv_file_last_record:
            linia = csv_file_last_record.read()
        csv_file_last_record.close()
        krotka = linia.split(';')
        #Data;Zasieg[%];Temp0[°C];Temp1[°C];Temp2[°C];Temp3[°C];Temp4[°C];Temp5[°C];Temp6[°C];Temp7[°C];Temp8[°C];Wilgotnosc0[%];Wilgotnosc1[%];Wilgotnosc2[%];Wilgotnosc3[%];Wilgotnosc4[%];Wilgotnosc5[%];Wilgotnosc6[%];Wilgotnosc7[%];Wilgotnosc8[%];Bateria0[%];Bateria1[%];Bateria2[%];Bateria3[%];Bateria4[%];Bateria5[%];Bateria6[%];Bateria7[%];Bateria8[%];
        drukuj("krotka: "+linia)
        self.krotka_danych=Krotka_Danych()
        self.krotka_danych.data=krotka[0]
        drukuj(str(self.krotka_danych.data) +" data pomiaru")
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
        
        drukuj("temp0 "+str(self.krotka_danych.temp[0]))       
        drukuj("wilg0 "+str(self.krotka_danych.wilg[0]))       

    def badamy_przekroczenia(self):
        drukuj("badamy_przekroczenia")
        self.czy_przekroczylo_temperature()
        self.czy_przekroczylo_wilgotnosc()

    def uaktualnij_plik_roboczy_csv_przekroczen(self):
        drukuj("uaktualnij_plik_roboczy_csv_przekroczen")
        if (os.path.isfile(self.path_to_przekroczenia_raport_csv)):
            shutil.copy2(self.path_to_przekroczenia_raport_csv, self.path_to_przekroczenia_raport_csv+".work")
        else:
            drukuj("nie znaleziono pod ścieszką "+ self.path_to_przekroczenia_raport_csv)
     
    def uaktualnij_plik_csv_przekroczen(self):
        drukuj("uaktualnij_plik_csv_przekroczen")
        if (os.path.isfile(self.path_to_przekroczenia_raport_csv+".work")):
            shutil.copy2(self.path_to_przekroczenia_raport_csv+".work", self.path_to_przekroczenia_raport_csv)
        else:
            drukuj("nie znaleziono pod ścieszką "+ self.path_to_przekroczenia_raport_csv+".work")
     
    def wpis_do_przekroczen(self, wpis, typ): #, typ, wartosc_z_jednostka):
        drukuj("wpis_do_przekroczen")
        #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda zapis
        drukuj(wpis)
        self.uaktualnij_plik_roboczy_csv_przekroczen()
        with open(self.path_to_przekroczenia_raport_csv+".work", "a", encoding="utf-8") as plik_do_przekroczen:
            plik_do_przekroczen.write(wpis+"\n")
        plik_do_przekroczen.close()
        self.uaktualnij_plik_csv_przekroczen()
        drukuj("Dodano przekroczenie typu "+typ)

    def sprawdz_baterie(self):
        drukuj("sprawdz_baterie")
        wartosc_baterii=self.krotka_danych.bat[int(self.sensor_id)]
        drukuj(wartosc_baterii)
        if isdigit(wartosc_baterii):
            if int(wartosc_baterii) == 1:
                #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda zapis
                typ="Bateria"
                wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+"-"+";"+"-"+";"+str(wartosc_baterii)+";"
                self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                drukuj("brak sygnału o niskim poziomie baterii")
        else:
            drukuj("N\A " + wartosc_baterii)
            drukuj("nie ma alarmu o słabej baterii "+wartosc_baterii)


    def czy_przekroczylo_temperature(self):
        drukuj("czy_przekroczylo_temperature")
        wartosc_temperatury=self.krotka_danych.temp[int(self.sensor_id)]
        typ="Temperatura"
        if isfloat(wartosc_temperatury):
            wartosc_z_jednostka=str(wartosc_temperatury)+" °C"
            if isfloat(self.temp_min_stopnie_celsjusza):
                if float(wartosc_temperatury) < float(self.temp_min_stopnie_celsjusza):
                    drukuj("przekroczenie - za niska temperatura")
                    #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda krotka
                    wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+str(self.temp_min_stopnie_celsjusza)+";"+str(self.temp_max_stopnie_celsjusza)+";"+wartosc_z_jednostka+";"
                    self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                drukuj("brak ogranicznika temperatury minimalnej")
            if isfloat(self.temp_max_stopnie_celsjusza):
                if float(wartosc_temperatury) > float(self.temp_max_stopnie_celsjusza):
                    drukuj("przekroczenie - za wysoka temperatura")
                    wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+str(self.temp_min_stopnie_celsjusza)+";"+str(self.temp_max_stopnie_celsjusza)+";"+wartosc_z_jednostka+";"
                    self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                drukuj("brak ogranicznika temperatury maksymalnej")
        else:
            drukuj("brak danych na temat zmierzonej temperatury")
            drukuj(self.krotka_danych.temp[int(self.sensor_id)])

    def czy_przekroczylo_wilgotnosc(self):
        drukuj("czy_przekroczylo_wilgotnosc"),
        wartosc_wilgotnosc=self.krotka_danych.wilg[int(self.sensor_id)]
        typ="Wilgotność"
        if isfloat(wartosc_wilgotnosc):
            wartosc_z_jednostka=str(wartosc_wilgotnosc)+" %"
            if isfloat(self.wilgotnosc_min_procent):
                if float(wartosc_wilgotnosc) < float(self.wilgotnosc_min_procent):
                    drukuj("przekroczenie - za niska wilgotnosc") 
                    #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda krotka
                    wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+str(self.wilgotnosc_min_procent)+";"+str(self.wilgotnosc_max_procent)+";"+wartosc_z_jednostka+";"
                    self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                drukuj("brak ogranicznika wilgotnosci minimalnej")
            if isfloat(self.wilgotnosc_max_procent):
                if float(wartosc_wilgotnosc) > float(self.wilgotnosc_max_procent):
                    drukuj("przekroczenie - za wysoka wilgotność")
                    #Id;Nazwa;Data;Typ;Min;Max;Wartość; - jak wygląda krotka
                    wpis=str(self.sensor_id)+";"+str(self.sensor_name)+";"+str(self.krotka_danych.data)+";"+str(typ)+";"+str(self.wilgotnosc_min_procent)+";"+str(self.wilgotnosc_max_procent)+";"+wartosc_z_jednostka+";"
                    self.wpis_do_przekroczen(wpis=wpis, typ=typ)
            else:
                drukuj("brak ogranicznika wilgotnosci maksymalnej") 
        else:
            drukuj("brak danych na temat zmierzonej wilgotności")
            drukuj(self.krotka_danych.wilg[int(self.sensor_id)])

    def wyslij_mejla(self):
        drukuj("wyślij_mejla")
        pass
   
    def wyslij_smsa(self):
        drukuj("wyślij_smsa")
        pass
    

if __name__ == "__main__":
    drukuj("------PRZEKROCZENIE--------")
    #inicjalizacja
    przekroczenia=Przekroczenia()

