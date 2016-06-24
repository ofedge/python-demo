import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

sender = 'sender@163.com'
receiver = 'receiver@163.com'


def send_attach_mail(file):
    msg = MIMEMultipart()
    msg['From'] = 'sender@163.com <sender@163.com>'
    msg['To'] = 'receiver@163.com <receiver@163.com>'
    msg['Subject'] = Header('home page db backup', 'utf-8')

    msg.attach(MIMEText('db backup', 'plain', 'utf-8'))

    att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    att['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file);
    msg.attach(att)

    smtp = smtplib.SMTP('smtp.163.com', 25)
    smtp.login('sender', 'password')
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('send success')

if __name__ == '__main__':
    send_attach_mail('myfile.file')
