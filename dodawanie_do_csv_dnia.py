#!/usr/bin/python
# - *- coding: utf- 8 - *-
import os
import shutil
import hashlib


def generate_md5_via_content(path_to_file):
    hash_md5 = hashlib.md5()
    with open(path_to_file, "r") as new_file_to_md5:
        new_md5_content=new_file_to_md5.read()
    new_file_to_md5.close()
    print(new_md5_content)
    hash_md5.update(new_md5_content)
    return hash_md5.hexdigest()


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
            with open(day_md5_path, "w") as file_md5:
                file_md5.write(new_md5)
            return True
        else:
            return False
    else:
        hash_md5=generate_md5_via_content(day_md5_path)
        with open(day_md5_path, "w+") as file_md5:
            file_md5.write(hash_md5)
        file_md5.close()
        return True
      


def main():
    print("Per aspera ad astra")
    path_to_generated_weewx_file='/var/www/html/weewx/our_site/NOAA'
    name_dest_of_file="NOAA-16__02__2022.csv"

    name_source_of_file="NOAA-last-hour.csv"
    name_wzor_file="NOAA-wzor.csv" #w miejscu generowania weewx-a programu jest wzor z chmod 777
    
    path_source=path_to_generated_weewx_file+"/"+name_source_of_file
    path_destination=path_to_generated_weewx_file+"/"+name_dest_of_file
    path_wzor_csv_file=path_to_generated_weewx_file+"/"+name_wzor_file
    if czy_md5_wskazuje_nowe_dane_oto_jest_pytanie(path_to_generated_weewx_file):
        if os.path.exists(path_source):
            if os.path.exists(path_destination) == False:
                 shutil.copy2(path_wzor_csv_file, path_destination)
            with open(path_source) as csv_file:
                lines = csv_file.readlines()
            f_dest=open(path_to_generated_weewx_file+"/"+name_dest_of_file,"a") 
            for line in lines: 
                f_dest.write(line)
                f_dest.write("\n")
            f_dest.close()
            print("zakonczono dodawanie tekstu do pliku")
        else: 
            print("nie ma pliku źródłowego - to po co mnie budzisz koleś?")
    else:
        print("ziomek - jeszcze nie ma nowych danych - nic się nie zmieniło")


if __name__ == "__main__":
    main()