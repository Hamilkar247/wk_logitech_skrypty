#!/usr/bin/python
# - *- coding: utf- 8 - *-
import os
import shutil
import hashlib
import datetime
import sys

def generate_md5_via_content(path_to_file):
    hash_md5 = hashlib.md5()
    with open(path_to_file, "r") as new_file_to_md5:
        new_md5_content=new_file_to_md5.read()
    new_file_to_md5.close()
    print(new_md5_content)
    hash_md5.update(new_md5_content)
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
        with open(day_md5_path, "r") as old_md5_file:
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


def sprawdzanie_czy_dzien_sie_nieskonczyl(data_i_reszta, path_to_generated_weewx_file):
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
        return True
    elif datetime_pomiaru > koniec_datetime_obiekt and datetime_pomiaru > poczatek_datetime_obiekt: 
        nowa_nazwa_dla_pliku="NOAA_"+str(datetime_pomiaru.strftime("%Y_%m_%d"))+".csv"
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


def main():

    print("Per aspera ad astra")

    path_to_generated_weewx_file='/var/www/html/weewx/our_site/NOAA'
    #fragment os.chdir i powrotem jest by zaspokoić marudnego cron-a
    os.chdir(path_to_generated_weewx_file)
    path_to_generated_weewx_file="."
    #name_dest_of_file="NOAA-16__02__2022.csv"
    list_name_dest_file=["NOAA_last_day.csv", "NOAA_last_week.csv", "NOAA_last_month.csv", "NOAA_last_year.csv"]

    name_source_of_file="NOAA-last-hour.csv"
    name_wzor_file="NOAA-wzor.csv" #w miejscu generowania weewx-a programu jest wzor z chmod 777
    

    path_source=path_to_generated_weewx_file+"/"+name_source_of_file
    path_wzor_csv_file=path_to_generated_weewx_file+"/"+name_wzor_file
    wskazywacz=False
    for name_dest_of_file in list_name_dest_file:    
        path_destination=path_to_generated_weewx_file+"/"+name_dest_of_file
        wskazywacz=czy_md5_wskazuje_nowe_dane_oto_jest_pytanie(path_to_generated_weewx_file)
        if wskazywacz:
            if os.path.exists(path_source):
                if os.path.exists(path_destination) == False:
                    shutil.copy2(path_wzor_csv_file, path_destination)
                with open(path_source) as csv_file:
                    lines = csv_file.readlines()
                sprawdzanie_czy_dzien_sie_nieskonczyl(lines[0], path_to_generated_weewx_file)
                sys.exit()
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
    if wskazywacz:
        zastap_stare_md5(path_to_generated_weewx_file)


if __name__ == "__main__":
    main()