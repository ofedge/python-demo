#! /usr/bin/env python3

import zipfile
import os
import time
import threading
import smtplib
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

ZIP_FILE_NAME = '/root/backup/myhome.zip'
BACKUP_FOLDER = '/root/home/'

SENDER = 'sender@163.com'
RECEIVER = 'receiver@163.com';
MSG_FORM = 'sender@163.com<vicitf@163.com>';
MSG_TO = 'receiver@163.com<silcata@163.com>';
MAIL_SUBJECT = '自动备份';
MSG_BODY = 'root备份';
SMTP_SERVER = 'smtp.163.com';
SMTP_PORT = 25;
SMTP_USERNAME = 'sender';
SMTP_PASSWORD = 'password';

TIME_INTERVAL = 24 * 60 * 60;


# zip the file in path folder with name filename
def zip_file(filename, path):
    f = zipfile.ZipFile(filename, 'w')
    write_zip(f, path)
    print('zip write succed:', datetime.datetime.now())
    f.close()


# recursion write folder to zip_file
def write_zip(zip_file, path):
    for file in os.listdir(path):
        print(file)
        if os.path.isdir(os.path.join(path, file)):
            zip_file.write(os.path.join(path, file))
            write_zip(zip_file, os.path.join(path, file))
        else:
            zip_file.write(os.path.join(path, file))


# mail that file to me!
def send_attach_mail(file):
    msg = MIMEMultipart()
    msg['From'] = MSG_FORM
    msg['To'] = MSG_TO
    msg['Subject'] = Header(MAIL_SUBJECT, 'utf-8')
    msg.attach(MIMEText(MSG_BODY, 'plain', 'utf-8'))
    att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    att['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file);
    msg.attach(att)

    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
    smtp.sendmail(SENDER, RECEIVER, msg.as_string())
    print('send succeed:', datetime.datetime.now())
    smtp.quit()


# run the task
def timer_start(file):
    while True:
        print('task started:', datetime.datetime.now())
        t = threading.Timer(0, send_attach_mail, (file,))
        t.start()
        time.sleep(TIME_INTERVAL)


if __name__ == '__main__':
    zip_file(ZIP_FILE_NAME, BACKUP_FOLDER)
    timer_start(ZIP_FILE_NAME)
