#Mailing list script created by PatKuz - https://github.com/PatKuz
import json, sys, smtplib, os
from email.mime.text import MIMEText

class colors:
    RED = '\033[31m'
    CYAN = '\33[36m'
    WHITE = '\33[37m'
    YELLOW = '\33[33m'
    GREEN = '\33[32m'

class mail:
    def __init__(self):
        print(colors.YELLOW + '[ + ] Gathering credentials...', end = '')
        try:
            with open('config.json') as (file):
                creds = json.load(file)
                
            self.EMAIL_SENDER = str(creds['EMAIL'])
            self.EMAIL_PASS = str(creds['PASS'])
            self.EMAIL_SERVICE = str(creds['SERVICE']).upper()
            
            if self.EMAIL_SERVICE != 'GMAIL':
                if self.EMAIL_SERVICE != 'YAHOO':
                    print(colors.RED + '\nInvalid service selected, must be Gmail or Yahoo.\nPlease run program after changes have been made.\n' + colors.WHITE)
                    sys.exit(1)
            print(colors.GREEN + ' - SUCCESS' + colors.YELLOW)
        except Exception as err:
            print(f'ERROR: {err}')
            print(colors.WHITE)
            sys.exit(1)

    def letter(self):
        try:
            UP = '\x1b[1A'
            ERASE = '\x1b[2K'

            print(colors.YELLOW + '[ + ] Creating letter and logging into account...')
            self.SUBJECT = str(input(colors.CYAN + '\nPlease enter desired subject of mail: '))
            f = open('EmailBody.txt','r')
            message = MIMEText(''.join(f.readlines()))
            f.close()
            self.BODY = str(message)[96:]

            for i in range(5):
                sys.stdout.write(UP)
                sys.stdout.write(ERASE)
                
            if self.EMAIL_SERVICE == 'GMAIL':
                self.SMTP_SERVER = 'smtp.gmail.com'
            else:
                self.SMTP_SERVER = 'smtp.mail.yahoo.com'
                
            self.client = smtplib.SMTP(self.SMTP_SERVER, 587)
            self.client.ehlo()
            self.client.starttls()
            self.client.login(self.EMAIL_SENDER, self.EMAIL_PASS)
            print(colors.YELLOW + '[ + ] Creating letter and logging into account...' + colors.GREEN + ' - SUCCESS')
        except Exception as err:
            print(f'ERROR: {err}')
            print(colors.WHITE)
            sys.exit(1)

    def gather_recipients(self):
        try:
            print(colors.YELLOW + '[ + ] Gathering recipients...', end = '')
            with open('EmailList.txt', 'r') as f:
                self.EMAIL_LIST = [line.strip() for line in f]
            print(colors.GREEN + ' - SUCCESS')
        except Exception:
            print('ERROR: Issue with text file.')
            print(colors.WHITE)
            sys.exit(1)

    def send_mail(self):
        try:
            os.system('clear')
            header()
            CONTENT = 'Subject: {}\n\n{}'.format(self.SUBJECT, self.BODY)
            x = 0
            print(colors.YELLOW + '[ + ] Sending emails...\n')
            for RECIPIENT in self.EMAIL_LIST:
                x+=1
                self.client.sendmail(self.EMAIL_SENDER, RECIPIENT, CONTENT)
                print(colors.YELLOW + 'sent letter to ' + RECIPIENT)
            self.client.close()
            print(colors.GREEN + '\n' + str(x) + ' Emails successfully sent.')
        except Exception as err:
            print(f'ERROR: {err}')
            print(colors.WHITE)
            sys.exit(1)

def header():
    os.system('clear')
    print(colors.CYAN + '''
       _________
     .`.        `.
    /   \ .======.\   __  __               __  __       _ _ 
    |   | |______||  |  \/  |             |  \/  |     (_) |
    |   |   _____ |  | \  / | __ _ ___ ___| \  / | __ _ _| |
    |   |  /    / |  | |\/| |/ _` / __/ __| |\/| |/ _` | | |
    |   | /____/  |  | |  | | (_| \__ \__ \ |  | | (_| | | |
    | _ |         |  |_|  |_|\__,_|___/___/_|  |_|\__,_|_|_|
    |/ \|.-"```"-.|                                            
    `` |||      |||                                                                                        
 jgs   `"`      `" ''')
    print(colors.RED + ' -=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-')
    print(colors.CYAN + '                        Project By: PatKuz')
    print(colors.RED + ' -=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-\n' + colors.WHITE)

if __name__ == '__main__':
    again = 'yes'
    while again.upper() != 'N':
        header()
        letter = mail()
        letter.letter()
        letter.gather_recipients()
        letter.send_mail()
        again = str(input(colors.CYAN + '\nWould you like to send another message? Y/N: '))
    print(colors.WHITE)
    
