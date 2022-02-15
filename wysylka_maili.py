#!/usr/bin/python
# - *- coding: utf- 8 - *-
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
mail_content = '''Testowe wyslanie mejla - wkl
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
print('Mejl wysłany '+str(datetime.datetime.now()))