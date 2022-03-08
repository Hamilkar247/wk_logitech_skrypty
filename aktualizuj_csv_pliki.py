#!/usr/bin/python3
# - *- coding: utf- 8 - *-
import os
import shutil
import hashlib
from datetime import datetime, timedelta
import sys
import logging
import traceback

def nazwa_programu():
    return "aktualizuj_csv_pliki.py"

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

def przerwij_i_wyswietl_czas():
    czas_teraz = datetime.now()
    current_time = czas_teraz.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    sys.exit()

class AktualizujCsvPliki(object):

    def __init__(self):
        drukuj("Aktualizuj_CSV_Pliki")
        drukuj("Per aspera ad astra")    
        self.path_to_generated_weewx_file='/var/www/html/weewx/lightlog_sensors/media/csv/NOAA'
        self.path_to_media='/var/www/html/weewx/lightlog_sensors/media/csv/NOAA'
        #fragment os.chdir i powrotem jest by zaspokoić marudnego cron-a
        if os.path.isdir(self.path_to_generated_weewx_file):
            drukuj("znaleziono folder")
            os.chdir(self.path_to_generated_weewx_file)
        else:
            drukuj("nie ma jak znalezc tego folderu")
        self.path_to_generated_weewx_file='/var/www/html/weewx/lightlog_sensors/media/csv/NOAA'
        #name_dest_of_file="NOAA-16__02__2022.csv"
        self.list_name_dest_file=["NOAA_this_day.csv", "NOAA_this_week.csv", "NOAA_this_month.csv", "NOAA_this_year.csv"]

        self.name_source_of_file="NOAA-last-hour.csv"
        self.name_wzor_file="NOAA_wzor.csv" #w miejscu generowania weewx-a programu jest wzor z chmod 777
    
        self.path_source=self.path_to_generated_weewx_file+"/"+self.name_source_of_file
        self.path_wzor_csv_file=self.path_to_generated_weewx_file+"/"+self.name_wzor_file
        self.wskazywacz=self.czy_md5_wskazuje_nowe_dane_oto_jest_pytanie(self.path_to_generated_weewx_file)
        if self.wskazywacz:
            for name_dest_of_file in self.list_name_dest_file:
                self.path_destination=self.path_to_generated_weewx_file+"/"+name_dest_of_file
                self.wskazywacz=self.czy_md5_wskazuje_nowe_dane_oto_jest_pytanie(self.path_to_generated_weewx_file)
                if self.wskazywacz:
                    if os.path.exists(self.path_source):
                        if os.path.exists(self.path_destination) == False:
                            shutil.copy2(self.path_wzor_csv_file, self.path_destination)
                        with open(self.path_source) as csv_file: #odczytujemy rekordy z pliku 'NOAA-last-hour.csv'
                            lines = csv_file.readlines()
                        if name_dest_of_file == "NOAA_this_day.csv":
                            self.sprawdzanie_czy_dzien_sie_skonczyl(lines[0], self.path_to_generated_weewx_file)
                        elif name_dest_of_file == "NOAA_this_week.csv":
                            self.sprawdzanie_czy_tydzien_sie_skonczyl(lines[0], self.path_to_generated_weewx_file)
                        if name_dest_of_file == "NOAA_this_month.csv":
                            self.sprawdzanie_czy_miesiac_sie_skonczyl(lines[0], self.path_to_generated_weewx_file)
                        if name_dest_of_file == "NOAA_this_year.csv":
                            self.sprawdzanie_czy_rok_sie_skonczyl(lines[0], self.path_to_generated_weewx_file)

                        self.uaktualnij_plik_roboczy_csv(self.path_to_generated_weewx_file+"/"+name_dest_of_file)
                        f_dest=open(self.path_to_generated_weewx_file+"/"+name_dest_of_file,"a") 
                        for line in lines:
                            f_dest.write("\n")
                            f_dest.write(line)
                        f_dest.close()
                        drukuj("zakonczono dodawanie tekstu do pliku")
                    else: 
                        drukuj("nie ma pliku źródłowego - to po co mnie budzisz koleś?")
                else:
                    drukuj("ziomek - jeszcze nie ma nowych danych - nic się nie zmieniło")
            self.zastap_stare_md5(self.path_to_generated_weewx_file)
 
    def uaktualnij_plik_roboczy_csv(self, path_to_file_with_namefile):
        if (os.path.isfile(path_to_file_with_namefile)):
            shutil.copy2(path_to_file_with_namefile, path_to_file_with_namefile+".work")
        else:
            drukuj("nie znaleziono pod ścieszką "+ path_to_file_with_namefile)

    def uaktualnij_plik_csv(self, path_to_file_with_namefile):
        if (os.path.isfile(path_to_file_with_namefile+".work")):
            os.rename(path_to_file_with_namefile+".work", path_to_file_with_namefile)
        else:
            drukuj("nie znaleziono pod ścieszką "+ path_to_file_with_namefile+".work")

    def generate_md5_via_content(self, path_to_file):
        hash_md5 = hashlib.md5()
        with open(path_to_file, "r", encoding='utf-8') as new_file_to_md5:
            new_md5_content=new_file_to_md5.read()
        new_file_to_md5.close()
        drukuj(new_md5_content)
        hash_md5.update(new_md5_content.encode("utf-8"))
        return hash_md5.hexdigest()
    
    def zastap_stare_md5(self, path_to_generated_weewx_file):
        file_md5=self.path_to_generated_weewx_file+"/"+"day.md5"
        last_file_path=self.path_to_generated_weewx_file+"/"+"NOAA-last-hour.csv"
        new_md5=self.generate_md5_via_content(last_file_path)
        with open(file_md5, "w") as file_md5:
            file_md5.write(new_md5)
        file_md5.close()
    
    def czy_md5_wskazuje_nowe_dane_oto_jest_pytanie(self, path_to_generated_weewx_file):
        try:
            day_md5_last_file="day.md5"
            last_file_name="NOAA-last-hour.csv"
            day_md5_path=self.path_to_generated_weewx_file+"/"+day_md5_last_file
            last_file_path=self.path_to_generated_weewx_file+"/"+last_file_name
            if os.path.exists(day_md5_path):
                old_md5=""
                with open(day_md5_path, "r", encoding='utf-8') as old_md5_file:
                    old_md5=old_md5_file.read()
                old_md5_file.close()
                new_md5=self.generate_md5_via_content(last_file_path)
                drukuj(old_md5)
                drukuj(new_md5)
                if old_md5 != new_md5:
                    # with open(day_md5_path, "w") as file_md5:
                    #     file_md5.write(new_md5)
                    return True
                else:
                    return False
            else:
                hash_md5=generate_md5_via_content(last_file_path)
                with open(day_md5_path, "w+") as file_md5:
                    file_md5.write(hash_md5)
                file_md5.close()
                return True
        except FileNotFoundError as e:
            drukuj(e)
            drukuj("FileNotFoundError")
            print(traceback.print_exc())

    def sprawdzanie_czy_dzien_sie_skonczyl(self, data_i_reszta, path_to_generated_weewx_file):
        dane=data_i_reszta.split(";")
        data=dane[0]
        datetime_pomiaru = datetime.strptime(data, "%d/%m/%y %H:%M:%S")
        drukuj(datetime_pomiaru)
        with open(path_to_generated_weewx_file+"/"+'obecny_dzien.txt', "r") as obecny_dzien_txt:
            poczatek_i_koniec=obecny_dzien_txt.read().split(";")
        drukuj(poczatek_i_koniec[0])
        drukuj(poczatek_i_koniec[1])
        poczatek_datetime_obiekt = datetime.strptime(poczatek_i_koniec[0], "%d/%m/%y %H:%M:%S")
        koniec_datetime_obiekt = datetime.strptime(poczatek_i_koniec[1], "%d/%m/%y %H:%M:%S")
        drukuj(poczatek_datetime_obiekt)
        drukuj(koniec_datetime_obiekt)
        if datetime_pomiaru > poczatek_datetime_obiekt and datetime_pomiaru < koniec_datetime_obiekt:
            return False
        elif datetime_pomiaru > koniec_datetime_obiekt and datetime_pomiaru > poczatek_datetime_obiekt: 
            nowa_nazwa_dla_pliku="NOAA_"+str(poczatek_datetime_obiekt.strftime("%Y_%m_%d"))+".csv"
            os.rename(path_to_generated_weewx_file+"/"+"NOAA_this_day.csv", path_to_generated_weewx_file+"/"+nowa_nazwa_dla_pliku)
            shutil.copy2(path_to_generated_weewx_file+"/"+"NOAA_wzor.csv", path_to_generated_weewx_file+"/"+"NOAA_last_day.csv")
            #dodanie dnia do granic w "obecny dzien"
            poczatek_datetime_obiekt = poczatek_datetime_obiekt + timedelta(days=1)
            koniec_datetime_obiekt = koniec_datetime_obiekt + timedelta(days=1)
            drukuj("--Verti est sua aeterni, Corda nostra solum tibi. Sprawdzenie czy delta działa")
            #print(poczatek_datetime_obiekt)
            #print(datetime.datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S"))
            poczatek_nowego_dnia=datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S")
            #print(koniec_datetime_obiekt)
            #print(datetime.datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S"))
            koniec_nowego_dnia=datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S")

            with open(path_to_generated_weewx_file+"/"+"obecny_dzien.txt", "w") as obecny_dzien_txt:
                obecny_dzien_txt.write(str(poczatek_nowego_dnia)+";"+str(koniec_nowego_dnia))
            obecny_dzien_txt.close()
        else:
            drukuj("koleś te dane już są starsze niż przewidzieliśmy")
            return False
    
    def sprawdzanie_czy_tydzien_sie_skonczyl(self, data_i_reszta, path_to_generated_weewx_file):
        dane=data_i_reszta.split(";")
        data=dane[0]
        datetime_pomiaru = datetime.strptime(data, "%d/%m/%y %H:%M:%S")
        drukuj(datetime_pomiaru)
        with open(path_to_generated_weewx_file+"/"+'obecny_tydzien.txt', "r") as obecny_tydzien_txt:
            poczatek_i_koniec=obecny_tydzien_txt.read().split(";")
        drukuj(poczatek_i_koniec[0])
        drukuj(poczatek_i_koniec[1])
        poczatek_datetime_obiekt = datetime.strptime(poczatek_i_koniec[0], "%d/%m/%y %H:%M:%S")
        koniec_datetime_obiekt = datetime.strptime(poczatek_i_koniec[1], "%d/%m/%y %H:%M:%S")
        drukuj(poczatek_datetime_obiekt)
        drukuj(koniec_datetime_obiekt)
        if datetime_pomiaru > poczatek_datetime_obiekt and datetime_pomiaru < koniec_datetime_obiekt:
            return False
        elif datetime_pomiaru > koniec_datetime_obiekt and datetime_pomiaru > poczatek_datetime_obiekt: 
            nowa_nazwa_dla_pliku="NOAA_tydzien_ktory_juz_minal.csv"
            os.rename(path_to_generated_weewx_file+"/"+"NOAA_this_week.csv", path_to_generated_weewx_file+"/"+nowa_nazwa_dla_pliku)
            shutil.copy2(path_to_generated_weewx_file+"/"+"NOAA_wzor.csv", path_to_generated_weewx_file+"/"+"NOAA_last_week.csv")
            #dodanie dnia do granic w "obecny tydzien"
            poczatek_datetime_obiekt = poczatek_datetime_obiekt + timedelta(days=7)
            koniec_datetime_obiekt = koniec_datetime_obiekt + timedelta(days=7)
            drukuj("--Verti est sua aeterni, Corda nostra solum tibi. Sprawdzenie czy delta działa")
            poczatek_nowego_tygodnia=datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S")
            koniec_nowego_tygodnia=datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S")
            drukuj("POCZATEK NOWEGO tygodnia "+str(poczatek_nowego_tygodnia))
            drukuj("KONIEC NOWEGO tygodnia "+str(koniec_nowego_tygodnia))
            with open(path_to_generated_weewx_file+"/"+"obecny_tydzien.txt", "w") as obecny_tygodnia_txt:
                obecny_tygodnia_txt.write(str(poczatek_nowego_tygodnia)+";"+str(koniec_nowego_tygodnia))
            obecny_tygodnia_txt.close()
            return True
        else:
            drukuj("koleś te dane już są starsze niż przewidzieliśmy")
            return False
    
    def pierwszy_dzien_kolejnego_miesiaca(self, poczatek_datetime_obiekt):
        if poczatek_datetime_obiekt.month == 12:
            return poczatek_datetime_obiekt.replace(year=poczatek_datetime_obiekt.year+1, month=1, day=1)
        return poczatek_datetime_obiekt.replace(month=poczatek_datetime_obiekt.month+1, day=1)
    
    def ostatni_dzien_kolejnego_miesiaca(self, poczatek_datetime_obiekt):
        if poczatek_datetime_obiekt.month == 12:     # jeśli jest grudzien - biore 1 stycznia - by odjac od niego 1 dzien i uzyskać 31 grudnia
            return poczatek_datetime_obiekt.replace(year=poczatek_datetime_obiekt.year+1, month=1, day=1, hour=23, minute=59, second=59) - timedelta(days=1) 
        #trik - bierzemy pierwszy dzien KOLEJNEGO miesiaca - i potem odejmujemy od niego jeden dzień     
        return poczatek_datetime_obiekt.replace(month=poczatek_datetime_obiekt.month+1, day=1, hour=23, minute=59, second=59) - timedelta(days=1)
    
    def sprawdzanie_czy_miesiac_sie_skonczyl(self, data_i_reszta, path_to_generated_weewx_file):
        dane=data_i_reszta.split(";")
        data=dane[0]
        datetime_pomiaru = datetime.strptime(data, "%d/%m/%y %H:%M:%S")
        drukuj(datetime_pomiaru)
        with open(path_to_generated_weewx_file+"/"+'obecny_miesiac.txt', "r") as obecny_miesiac_txt:
            poczatek_i_koniec=obecny_miesiac_txt.read().split(";")
        poczatek_datetime_obiekt = datetime.strptime(poczatek_i_koniec[0], "%d/%m/%y %H:%M:%S")
        koniec_datetime_obiekt = datetime.strptime(poczatek_i_koniec[1], "%d/%m/%y %H:%M:%S")
        if datetime_pomiaru > poczatek_datetime_obiekt and datetime_pomiaru < koniec_datetime_obiekt:
            return False
        elif datetime_pomiaru > koniec_datetime_obiekt and datetime_pomiaru > poczatek_datetime_obiekt: 
            nowa_nazwa_dla_pliku="NOAA_"+str(poczatek_datetime_obiekt.strftime("%Y_%m_%d"))+".csv"
            os.rename(path_to_generated_weewx_file+"/"+"NOAA_this_month.csv", path_to_generated_weewx_file+"/"+nowa_nazwa_dla_pliku)
            shutil.copy2(path_to_generated_weewx_file+"/"+"NOAA_wzor.csv", path_to_generated_weewx_file+"/"+"NOAA_last_month.csv")
            #dodanie dnia do granic w "obecny dzien"
            poczatek_datetime_obiekt = pierwszy_dzien_kolejnego_miesiaca(poczatek_datetime_obiekt)
            koniec_datetime_obiekt = ostatni_dzien_kolejnego_miesiaca(poczatek_datetime_obiekt)
            #koniec_datetime_obiekt = koniec_datetime_obiekt + datetime.timedelta(days=1)
            drukuj("--Verti est sua aeterni, Corda nostra solum tibi. Sprawdzenie czy delta działa")
            poczatek_nowego_miesiaca=datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S")
            koniec_nowego_miesiaca=datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S")
            drukuj("POCZATEK NOWEGO MIESIACA "+str(poczatek_nowego_miesiaca))
            drukuj("KONIEC NOWEGO MIESIACA "+str(koniec_nowego_miesiaca))
            with open(path_to_generated_weewx_file+"/"+"obecny_miesiac.txt", "w") as obecny_miesiac_txt:
                obecny_miesiac_txt.write(str(poczatek_nowego_miesiaca)+";"+str(koniec_nowego_miesiaca))
            obecny_miesiac_txt.close()
            return True
        else:
            drukuj("koleś te dane już są starsze niż przewidzieliśmy dla tego raportu")
            return False
    
    def pierwszy_dzien_kolejnego_roku(self, poczatek_datetime_obiekt):
        return poczatek_datetime_obiekt.replace(year=poczatek_datetime_obiekt.year+1, month=1, day=1)
    
    def ostatni_dzien_kolejnego_roku(self, poczatek_datetime_obiekt):
        return poczatek_datetime_obiekt.replace(year=poczatek_datetime_obiekt.year+1, month=12, day=31, hour=23, minute=59, second=59)
    
    def sprawdzanie_czy_rok_sie_skonczyl(self, data_i_reszta, path_to_generated_weewx_file):
        dane=data_i_reszta.split(";")
        data=dane[0]
        datetime_pomiaru = datetime.strptime(data, "%d/%m/%y %H:%M:%S")
        drukuj("datetime_pomiaru"+str(datetime_pomiaru))
        with open(path_to_generated_weewx_file+"/"+'obecny_rok.txt', "r") as obecny_rok_txt:
            poczatek_i_koniec=obecny_rok_txt.read().split(";")
        poczatek_datetime_obiekt = datetime.strptime(poczatek_i_koniec[0], "%d/%m/%y %H:%M:%S")
        koniec_datetime_obiekt = datetime.strptime(poczatek_i_koniec[1], "%d/%m/%y %H:%M:%S")
        if datetime_pomiaru > poczatek_datetime_obiekt and datetime_pomiaru < koniec_datetime_obiekt:
            return False
        elif datetime_pomiaru > koniec_datetime_obiekt and datetime_pomiaru > poczatek_datetime_obiekt: 
            nowa_nazwa_dla_pliku="NOAA_"+str(poczatek_datetime_obiekt.strftime("%Y_%m_%d"))+".csv"
            os.rename(path_to_generated_weewx_file+"/"+"NOAA_this_year.csv", path_to_generated_weewx_file+"/"+nowa_nazwa_dla_pliku)
            shutil.copy2(path_to_generated_weewx_file+"/"+"NOAA_wzor.csv", path_to_generated_weewx_file+"/"+"NOAA_last_year.csv")
            #dodanie dnia do granic w "obecny rok"
            poczatek_datetime_obiekt = pierwszy_dzien_kolejnego_roku(poczatek_datetime_obiekt)
            koniec_datetime_obiekt = ostatni_dzien_kolejnego_roku(koniec_datetime_obiekt)
            drukuj("--Verti est sua aeterni, Corda nostra solum tibi. Sprawdzenie czy delta działa")
            poczatek_nowego_roku=datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S")
            koniec_nowego_roku=datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S")
            drukuj("POCZATEK NOWEGO ROKU "+str(poczatek_nowego_roku))
            drukuj("KONIEC NOWEGO ROKU "+str(koniec_nowego_roku))
            with open(path_to_generated_weewx_file+"/"+"obecny_rok.txt", "w") as obecny_rok_txt:
                obecny_rok_txt.write(str(poczatek_nowego_roku)+";"+str(koniec_nowego_roku))
            obecny_rok_txt.close()
            return True
        else:
            drukuj("koleś te dane już są starsze niż przewidzieliśmy dla tego raportu")
            return False
    

def main():
    aktualizuj_csv_pliki=AktualizujCsvPliki()

if __name__ == "__main__":
    drukuj("------AKTUALIZUJ_CSV_PLIKI--------")
    main()
