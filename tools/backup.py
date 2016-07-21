#! /usr/bin/env python3

import zipfile
import os
import time
import threading
import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

ZIP_FILE_NAME = '/home/backup/myhomezip'
BACKUP_FOLDER = '/root/home/'

SENDER = 'sender@163.com'
RECEIVER = 'receiver@163.com';
MSG_FORM = 'sender@163.com<sender@163.com>';
MSG_TO = 'receiver@163.com<receiver@163.com>';
MAIL_SUBJECT = 'homepage';
MSG_BODY = 'homepage';
SMTP_SERVER = 'smtp.163.com';
SMTP_PORT = 25;
SMTP_USERNAME = 'sender';
SMTP_PASSWORD = 'password';

TIME_INTERVAL = 24 * 60 * 60;

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='backup.log',
                    filemode='a')


# zip the file in path folder with name filename
def zip_file(filename, path):
    f = zipfile.ZipFile(filename, 'w')
    write_zip(f, path)
    logging.info('zip write succed')
    f.close()


# recursion write folder to zip_file
def write_zip(zip_file, path):
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            zip_file.write(os.path.join(path, file))
            write_zip(zip_file, os.path.join(path, file))
        else:
            zip_file.write(os.path.join(path, file))


# mail that file to me!
def send_attach_mail(file):
    zip_file(ZIP_FILE_NAME, BACKUP_FOLDER)
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
    logging.info('send succeed')
    smtp.quit()
    os.remove(ZIP_FILE_NAME)
    logging.info('file removed')


# run the task
def timer_start(file):
    while True:
        logging.info('task started')
        t = threading.Timer(0, send_attach_mail, (file,))
        t.start()
        time.sleep(TIME_INTERVAL)


if __name__ == '__main__':
    timer_start(ZIP_FILE_NAME)
