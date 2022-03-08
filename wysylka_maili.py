#!/usr/bin/python
# - *- coding: utf- 8 - *-
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback
from datetime import datetime

def nazwa_programu():
    return "wysylka_maili.py"

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

mail_content = '''
Aut Caesar aut nihil,
Hic abundant leones,
Hic sunt leones,
Alea iacta est!

English translation:
Caesar or nothing,
Here lions abound,
Here are lions,
The die is cast!
'''
#The mail addresses and password
#sender_address = 'acegmp@op.pl'
#sender_pass = 'hd#xgVRn8jvmtQhC'
sender_address = 'acegmp1acegmp@gmail.com'
sender_pass = "acegmp.local"
receiver_address = 'acegmp1acegmp@gmail.com'
#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'ahoj_wkl.'   #The subject line
#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))
#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login(sender_address, sender_pass) #login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
drukuj('Mejl wysłany - Aut Caesar aut nihil! '+str(datetime.datetime.now()))