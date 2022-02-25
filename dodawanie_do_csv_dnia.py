#!/usr/bin/python3
# - *- coding: utf- 8 - *-
import os
import shutil
import hashlib
import datetime
import sys
import logging

def przerwij_i_wyswietl_czas():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    sys.exit()

def generate_md5_via_content(path_to_file):
    hash_md5 = hashlib.md5()
    with open(path_to_file, "r", encoding='utf-8') as new_file_to_md5:
        new_md5_content=new_file_to_md5.read()
    new_file_to_md5.close()
    print(new_md5_content)
    hash_md5.update(new_md5_content.encode("utf-8"))
    return hash_md5.hexdigest()

def zastap_stare_md5(path_to_generated_weewx_file):
    file_md5=path_to_generated_weewx_file+"/"+"day.md5"
    last_file_path=path_to_generated_weewx_file+"/"+"NOAA-last-hour.csv"
    new_md5=generate_md5_via_content(last_file_path)
    with open(file_md5, "w") as file_md5:
        file_md5.write(new_md5)
    file_md5.close()

def czy_md5_wskazuje_nowe_dane_oto_jest_pytanie(path_to_generated_weewx_file):
    day_md5_last_file="day.md5"
    last_file_name="NOAA-last-hour.csv" 
    day_md5_path=path_to_generated_weewx_file+"/"+day_md5_last_file
    last_file_path=path_to_generated_weewx_file+"/"+last_file_name
    if os.path.exists(day_md5_path):
        old_md5=""
        with open(day_md5_path, "r", encoding='utf-8') as old_md5_file:
            old_md5=old_md5_file.read()
        old_md5_file.close()
        new_md5=generate_md5_via_content(last_file_path)
        print(old_md5)
        print(new_md5)
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

def sprawdzanie_czy_dzien_sie_skonczyl(data_i_reszta, path_to_generated_weewx_file):
    dane=data_i_reszta.split(";")
    data=dane[0]
    datetime_pomiaru = datetime.datetime.strptime(data, "%d/%m/%y %H:%M:%S")
    print(datetime_pomiaru)
    with open(path_to_generated_weewx_file+"/"+'obecny_dzien.txt', "r") as obecny_dzien_txt:
        poczatek_i_koniec=obecny_dzien_txt.read().split(";")
    print(poczatek_i_koniec[0])
    print(poczatek_i_koniec[1])
    poczatek_datetime_obiekt = datetime.datetime.strptime(poczatek_i_koniec[0], "%d/%m/%y %H:%M:%S")
    koniec_datetime_obiekt = datetime.datetime.strptime(poczatek_i_koniec[1], "%d/%m/%y %H:%M:%S")
    print(poczatek_datetime_obiekt)
    print(koniec_datetime_obiekt)
    if datetime_pomiaru > poczatek_datetime_obiekt and datetime_pomiaru < koniec_datetime_obiekt:
        return False
    elif datetime_pomiaru > koniec_datetime_obiekt and datetime_pomiaru > poczatek_datetime_obiekt: 
        nowa_nazwa_dla_pliku="NOAA_"+str(poczatek_datetime_obiekt.strftime("%Y_%m_%d"))+".csv"
        os.rename(path_to_generated_weewx_file+"/"+"NOAA_last_day.csv", path_to_generated_weewx_file+"/"+nowa_nazwa_dla_pliku)
        shutil.copy2(path_to_generated_weewx_file+"/"+"NOAA_wzor.csv", path_to_generated_weewx_file+"/"+"NOAA_last_day.csv")
        #dodanie dnia do granic w "obecny dzien"
        poczatek_datetime_obiekt = poczatek_datetime_obiekt + datetime.timedelta(days=1)
        koniec_datetime_obiekt = koniec_datetime_obiekt + datetime.timedelta(days=1)
        print("--Verti est sua aeterni, Corda nostra solum tibi. Sprawdzenie czy delta działa")
        #print(poczatek_datetime_obiekt)
        #print(datetime.datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S"))
        poczatek_nowego_dnia=datetime.datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S")
        #print(koniec_datetime_obiekt)
        #print(datetime.datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S"))
        koniec_nowego_dnia=datetime.datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S")
        with open(path_to_generated_weewx_file+"/"+"obecny_dzien.txt", "w") as obecny_dzien_txt:
            obecny_dzien_txt.write(str(poczatek_nowego_dnia)+";"+str(koniec_nowego_dnia))
        obecny_dzien_txt.close()
    else:
        print("koleś te dane już są starsze niż przewidzieliśmy")
        return False

def sprawdzanie_czy_tydzien_sie_skonczyl(data_i_reszta, path_to_generated_weewx_file):
    dane=data_i_reszta.split(";")
    data=dane[0]
    datetime_pomiaru = datetime.datetime.strptime(data, "%d/%m/%y %H:%M:%S")
    print(datetime_pomiaru)
    with open(path_to_generated_weewx_file+"/"+'obecny_tydzien.txt', "r") as obecny_tydzien_txt:
        poczatek_i_koniec=obecny_tydzien_txt.read().split(";")
    print(poczatek_i_koniec[0])
    print(poczatek_i_koniec[1])
    poczatek_datetime_obiekt = datetime.datetime.strptime(poczatek_i_koniec[0], "%d/%m/%y %H:%M:%S")
    koniec_datetime_obiekt = datetime.datetime.strptime(poczatek_i_koniec[1], "%d/%m/%y %H:%M:%S")
    print(poczatek_datetime_obiekt)
    print(koniec_datetime_obiekt)
    if datetime_pomiaru > poczatek_datetime_obiekt and datetime_pomiaru < koniec_datetime_obiekt:
        return False
    elif datetime_pomiaru > koniec_datetime_obiekt and datetime_pomiaru > poczatek_datetime_obiekt: 
        nowa_nazwa_dla_pliku="NOAA_tydzien_ktory_juz_minal.csv"
        os.rename(path_to_generated_weewx_file+"/"+"NOAA_last_week.csv", path_to_generated_weewx_file+"/"+nowa_nazwa_dla_pliku)
        shutil.copy2(path_to_generated_weewx_file+"/"+"NOAA_wzor.csv", path_to_generated_weewx_file+"/"+"NOAA_last_week.csv")
        #dodanie dnia do granic w "obecny tydzien"
        poczatek_datetime_obiekt = poczatek_datetime_obiekt + datetime.timedelta(days=7)
        koniec_datetime_obiekt = koniec_datetime_obiekt + datetime.timedelta(days=7)
        print("--Verti est sua aeterni, Corda nostra solum tibi. Sprawdzenie czy delta działa")
        poczatek_nowego_tygodnia=datetime.datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S")
        koniec_nowego_tygodnia=datetime.datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S")
        print("POCZATEK NOWEGO tygodnia "+str(poczatek_nowego_tygodnia))
        print("KONIEC NOWEGO tygodnia "+str(koniec_nowego_tygodnia))
        with open(path_to_generated_weewx_file+"/"+"obecny_tydzien.txt", "w") as obecny_tygodnia_txt:
            obecny_tygodnia_txt.write(str(poczatek_nowego_tygodnia)+";"+str(koniec_nowego_tygodnia))
        obecny_tygodnia_txt.close()
        return True
    else:
        print("koleś te dane już są starsze niż przewidzieliśmy")
        return False

def pierwszy_dzien_kolejnego_miesiaca(poczatek_datetime_obiekt):
    if poczatek_datetime_obiekt.month == 12:
        return poczatek_datetime_obiekt.replace(year=poczatek_datetime_obiekt.year+1, month=1, day=1)
    return poczatek_datetime_obiekt.replace(month=poczatek_datetime_obiekt.month+1, day=1)

def ostatni_dzien_kolejnego_miesiaca(poczatek_datetime_obiekt):
    if poczatek_datetime_obiekt.month == 12:     # jeśli jest grudzien - biore 1 stycznia - by odjac od niego 1 dzien i uzyskać 31 grudnia
        return poczatek_datetime_obiekt.replace(year=poczatek_datetime_obiekt.year+1, month=1, day=1, hour=23, minute=59, second=59) - datetime.timedelta(days=1) 
    #trik - bierzemy pierwszy dzien KOLEJNEGO miesiaca - i potem odejmujemy od niego jeden dzień     
    return poczatek_datetime_obiekt.replace(month=poczatek_datetime_obiekt.month+1, day=1, hour=23, minute=59, second=59) - datetime.timedelta(days=1)

def sprawdzanie_czy_miesiac_sie_skonczyl(data_i_reszta, path_to_generated_weewx_file):
    dane=data_i_reszta.split(";")
    data=dane[0]
    datetime_pomiaru = datetime.datetime.strptime(data, "%d/%m/%y %H:%M:%S")
    print(datetime_pomiaru)
    with open(path_to_generated_weewx_file+"/"+'obecny_miesiac.txt', "r") as obecny_miesiac_txt:
        poczatek_i_koniec=obecny_miesiac_txt.read().split(";")
    poczatek_datetime_obiekt = datetime.datetime.strptime(poczatek_i_koniec[0], "%d/%m/%y %H:%M:%S")
    koniec_datetime_obiekt = datetime.datetime.strptime(poczatek_i_koniec[1], "%d/%m/%y %H:%M:%S")
    if datetime_pomiaru > poczatek_datetime_obiekt and datetime_pomiaru < koniec_datetime_obiekt:
        return False
    elif datetime_pomiaru > koniec_datetime_obiekt and datetime_pomiaru > poczatek_datetime_obiekt: 
        nowa_nazwa_dla_pliku="NOAA_"+str(poczatek_datetime_obiekt.strftime("%Y_%m_%d"))+".csv"
        os.rename(path_to_generated_weewx_file+"/"+"NOAA_last_month.csv", path_to_generated_weewx_file+"/"+nowa_nazwa_dla_pliku)
        shutil.copy2(path_to_generated_weewx_file+"/"+"NOAA_wzor.csv", path_to_generated_weewx_file+"/"+"NOAA_last_month.csv")
        #dodanie dnia do granic w "obecny dzien"
        poczatek_datetime_obiekt = pierwszy_dzien_kolejnego_miesiaca(poczatek_datetime_obiekt)
        koniec_datetime_obiekt = ostatni_dzien_kolejnego_miesiaca(poczatek_datetime_obiekt)
        #koniec_datetime_obiekt = koniec_datetime_obiekt + datetime.timedelta(days=1)
        print("--Verti est sua aeterni, Corda nostra solum tibi. Sprawdzenie czy delta działa")
        poczatek_nowego_miesiaca=datetime.datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S")
        koniec_nowego_miesiaca=datetime.datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S")
        print("POCZATEK NOWEGO MIESIACA "+str(poczatek_nowego_miesiaca))
        print("KONIEC NOWEGO MIESIACA "+str(koniec_nowego_miesiaca))
        with open(path_to_generated_weewx_file+"/"+"obecny_miesiac.txt", "w") as obecny_miesiac_txt:
            obecny_miesiac_txt.write(str(poczatek_nowego_miesiaca)+";"+str(koniec_nowego_miesiaca))
        obecny_miesiac_txt.close()
        return True
    else:
        print("koleś te dane już są starsze niż przewidzieliśmy dla tego raportu")
        return False

def pierwszy_dzien_kolejnego_roku(poczatek_datetime_obiekt):
    return poczatek_datetime_obiekt.replace(year=poczatek_datetime_obiekt.year+1, month=1, day=1)

def ostatni_dzien_kolejnego_roku(poczatek_datetime_obiekt):
    return poczatek_datetime_obiekt.replace(year=poczatek_datetime_obiekt.year+1, month=12, day=31, hour=23, minute=59, second=59)

def sprawdzanie_czy_rok_sie_skonczyl(data_i_reszta, path_to_generated_weewx_file):
    dane=data_i_reszta.split(";")
    data=dane[0]
    datetime_pomiaru = datetime.datetime.strptime(data, "%d/%m/%y %H:%M:%S")
    print(datetime_pomiaru)
    with open(path_to_generated_weewx_file+"/"+'obecny_rok.txt', "r") as obecny_rok_txt:
        poczatek_i_koniec=obecny_rok_txt.read().split(";")
    poczatek_datetime_obiekt = datetime.datetime.strptime(poczatek_i_koniec[0], "%d/%m/%y %H:%M:%S")
    koniec_datetime_obiekt = datetime.datetime.strptime(poczatek_i_koniec[1], "%d/%m/%y %H:%M:%S")
    if datetime_pomiaru > poczatek_datetime_obiekt and datetime_pomiaru < koniec_datetime_obiekt:
        return False
    elif datetime_pomiaru > koniec_datetime_obiekt and datetime_pomiaru > poczatek_datetime_obiekt: 
        nowa_nazwa_dla_pliku="NOAA_"+str(poczatek_datetime_obiekt.strftime("%Y_%m_%d"))+".csv"
        os.rename(path_to_generated_weewx_file+"/"+"NOAA_last_year.csv", path_to_generated_weewx_file+"/"+nowa_nazwa_dla_pliku)
        shutil.copy2(path_to_generated_weewx_file+"/"+"NOAA_wzor.csv", path_to_generated_weewx_file+"/"+"NOAA_last_year.csv")
        #dodanie dnia do granic w "obecny rok"
        poczatek_datetime_obiekt = pierwszy_dzien_kolejnego_roku(poczatek_datetime_obiekt)
        koniec_datetime_obiekt = ostatni_dzien_kolejnego_roku(koniec_datetime_obiekt)
        print("--Verti est sua aeterni, Corda nostra solum tibi. Sprawdzenie czy delta działa")
        poczatek_nowego_roku=datetime.datetime.strftime(poczatek_datetime_obiekt, "%d/%m/%y %H:%M:%S")
        koniec_nowego_roku=datetime.datetime.strftime(koniec_datetime_obiekt, "%d/%m/%y %H:%M:%S")
        print("POCZATEK NOWEGO ROKU "+str(poczatek_nowego_roku))
        print("KONIEC NOWEGO ROKU "+str(koniec_nowego_roku))
        with open(path_to_generated_weewx_file+"/"+"obecny_rok.txt", "w") as obecny_rok_txt:
            obecny_rok_txt.write(str(poczatek_nowego_roku)+";"+str(koniec_nowego_roku))
        obecny_rok_txt.close()
        return True
    else:
        print("koleś te dane już są starsze niż przewidzieliśmy dla tego raportu")
        return False

def main():

    print("Per aspera ad astra")
    path_to_generated_weewx_file='/var/www/html/weewx/lightlog_sensors/media/config/csv/NOAA'
    path_to_media='/var/www/html/weewx/lightlog_sensors/media/config/csv/NOAA'
    #fragment os.chdir i powrotem jest by zaspokoić marudnego cron-a
    os.chdir(path_to_generated_weewx_file)
    path_to_generated_weewx_file='/var/www/html/weewx/lightlog_sensors/media/config/csv/NOAA'
    #name_dest_of_file="NOAA-16__02__2022.csv"
    list_name_dest_file=["NOAA_last_day.csv", "NOAA_last_week.csv", "NOAA_last_month.csv", "NOAA_last_year.csv"]

    name_source_of_file="NOAA-last-hour.csv"
    name_wzor_file="NOAA-wzor.csv" #w miejscu generowania weewx-a programu jest wzor z chmod 777
    

    path_source=path_to_generated_weewx_file+"/"+name_source_of_file
    path_wzor_csv_file=path_to_generated_weewx_file+"/"+name_wzor_file
    wskazywacz=czy_md5_wskazuje_nowe_dane_oto_jest_pytanie(path_to_generated_weewx_file)
    if wskazywacz:
        for name_dest_of_file in list_name_dest_file:    
            path_destination=path_to_generated_weewx_file+"/"+name_dest_of_file
            wskazywacz=czy_md5_wskazuje_nowe_dane_oto_jest_pytanie(path_to_generated_weewx_file)
            if wskazywacz:
                if os.path.exists(path_source):
                    if os.path.exists(path_destination) == False:
                        shutil.copy2(path_wzor_csv_file, path_destination)
                    with open(path_source) as csv_file:
                        lines = csv_file.readlines()
                    if name_dest_of_file == "NOAA_last_day.csv":
                        sprawdzanie_czy_dzien_sie_skonczyl(lines[0], path_to_generated_weewx_file)
                    elif name_dest_of_file == "NOAA_last_week.csv":
                        sprawdzanie_czy_tydzien_sie_skonczyl(lines[0], path_to_generated_weewx_file)
                    if name_dest_of_file == "NOAA_last_month.csv":
                        sprawdzanie_czy_miesiac_sie_skonczyl(lines[0], path_to_generated_weewx_file)
                    if name_dest_of_file == "NOAA_last_year.csv":
                        sprawdzanie_czy_rok_sie_skonczyl(lines[0], path_to_generated_weewx_file)
                    f_dest=open(path_to_generated_weewx_file+"/"+name_dest_of_file,"a") 
                    for line in lines:
                        f_dest.write("\n")
                        f_dest.write(line)
                    f_dest.close()
                    print("zakonczono dodawanie tekstu do pliku")
                else: 
                    print("nie ma pliku źródłowego - to po co mnie budzisz koleś?")
            else:
                print("ziomek - jeszcze nie ma nowych danych - nic się nie zmieniło")
        zastap_stare_md5(path_to_generated_weewx_file)


if __name__ == "__main__":
    logging.root.setLevel(logging.DEBUG)
    logging.debug("wyspa węży")
    #przerwij_i_wyswietl_czas()
    main()
