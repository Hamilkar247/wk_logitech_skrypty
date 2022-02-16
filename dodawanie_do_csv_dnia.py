#!/usr/bin/python
# - *- coding: utf- 8 - *-

import os

path_to_generated_weewx_file='/var/www/html/weewx/our_site/NOAA'
name_dest_of_file="NOAA-15.02.2022.csv"
name_source_of_file="NOAA-last-hour.csv"

path_source=path_to_generated_weewx_file+"/"+name_source_of_file
path_destination=path_to_generated_weewx_file+"/"+name_dest_of_file
if os.path.exists(path_source):
    if os.path.exists(path_destination):
        with open(path_source) as csv_file:
            lines = csv_file.readlines()
        f_dest=open(path_to_generated_weewx_file+"/"+name_dest_of_file,"w") 
        for line in lines: 
            f_dest.write()
        f_dest.close()
        print("zakonczono dodawanie tekstu do pliku")
    else:
        print("nie ma pliku docelowego - to po co mnie budzisz koleś?")
else: 
    print("nie ma pliku źródłowego - to po co mnie budzisz koleś?")