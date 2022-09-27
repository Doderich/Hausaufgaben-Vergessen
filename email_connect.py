
from configparser import ConfigParser
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
msg = "Hello World"
print(msg)

def read_email_config(filename='config.ini', section='email'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    ls = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            ls[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return ls
email_dic = read_email_config()

MY_ADDRESS = email_dic['my_address']
MY_PASSWORD = email_dic['my_password']
RECIPIENT_ADDRESS = email_dic['recipient_address']
HOST_ADDRESS = email_dic['host_address']
HOST_PORT = email_dic['host_port']


print(email_dic)
# Connection with the server
def send_email(recipient_email = RECIPIENT_ADDRESS, amount = 1):
    server = smtplib.SMTP(host=HOST_ADDRESS, port=HOST_PORT)
    server.starttls()
    server.login(MY_ADDRESS, MY_PASSWORD)
    # Creation of the MIMEMultipart Object
    message = MIMEMultipart()
    

    # Setup of MIMEMultipart Object Header
    message['From'] = MY_ADDRESS
    message['To'] = recipient_email
    message['Subject'] = "Automatische E-Mail Hausaufgaben Vergessen"

# Creation of a MIMEText Part
    file = open('automated_email.txt')
    txt = file.readlines()
    file.close()
    text = ''
    for line in txt:
       text = text + line 
    args = ('Name', 'Mathematik', amount)
    print(text % args)
    textPart = MIMEText(text, 'plain')

    # Part attachment
    message.attach(textPart)

    # Send Email and close connection
    #server.send_message(message)
    server.quit()
send_email()