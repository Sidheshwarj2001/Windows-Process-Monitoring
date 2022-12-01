import os
import time
import psutil
from sys import *
from datetime import datetime
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import urllib.request

def is_connected():
    try:
        urllib.request.urlopen(r"https://www.google.com/",timeout=1)
        return True
    except urllib.request.URLError as err:
        print("Internet is not connected")
        print(err)
        return False

def sendMail(EmailID,file):
    fromEmail = EmailID
    EmailPawword = "evogucrtwpjcknco"
    sendToEmail = "Sidjawale007@gmail.com"

    # making instance of multipart
    msg = MIMEMultipart()
    msg["From"] = fromEmail
    msg["To"] = sendToEmail

    msg["Subject"] = "Log file Which contain the proces "

    body = " This process contain all the process with pid ,username and user"
    # open the file which you  want to send
    filename = "file name with extension"
    attachment = open(file,'rb')

    msg.attach(MIMEText(body, "plain"))

    # instance of MINEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    p.set_payload(attachment.read())  # file attach

    encoders.encode_base64(p)

    p.add_header('current-Disponsition', 'attachment; filename = %s' % filename)

    msg.attach(p)

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(fromEmail,EmailPawword)

    text = msg.as_string()

    server.sendmail(fromEmail,sendToEmail,text)

    server.quit()

    print("mail successfully send")

def WriteProcessInLog(arr,dirname):

    if not os.path.exists(dirname):
        try:
            os.mkdir(dirname)
        except:
            pass
    log_path = os.path.join(dirname,"sid%s.txt"%time.strftime("%Y%m%d-%H%M%S"))

    fd = open(log_path, 'w')
    fd.write("-" * 40 + "\n")
    fd.write("sid process logger " + time.ctime() + '\n')
    fd.write("-" * 40 + "\n")

    for process in arr:
        fd.write("-"*40+"\n")
        fd.write('%s\n' %process)
        fd.write(" ")

    return log_path
    
def process_monitor():

    list_process= []

    for proc in psutil.process_iter():
        pinfo = proc.as_dict(attrs = ['pid','name','username'])

        list_process.append(pinfo)

    return list_process

def main():
    print("Welcome to our process Monitor and log file generate script")

    print("Name of Application is : "+argv[0])

    if (len(argv) !=3):
        print("INVALID NUMBER OF ARGUMENTS : ______")
        print("Use -U for usage and -H for the help")
        exit()

    if argv[1] == "-u" or argv[1] == '-U':
        print("USAEGE : the script is use for the monitor the proces and write that process in the log file send this log file to users email ")
        exit()

    if argv[1] == '-h' or argv[1]=='-H':
        print("This script require one argument")
        print("First Argument is : Name of Directory")
        print("second Argument is : Email id")
        exit()

    try:
        def schedule_Fuc():
            arr = []
            arr = process_monitor()
            fileName = WriteProcessInLog(arr, argv[1])
            sendMail(argv[2],fileName)

        connect = is_connected()
        if connect:
            schedule.every(60).minutes.do(schedule_Fuc)

        else:
            print("Unable to connect to internet !.")

    except Exception as E:
        print("Invalid Error : ",E)

    while True:
        schedule.run_pending()
        time.sleep(5)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()

    print("Total time require to this script is : ",end-start)
