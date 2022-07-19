#https://www.youtube.com/watch?v=6DD4IOHhNYo

import smtplib
import email.message
import email
import imaplib
import json
import os


class GMail:
    def __init__(self, credentials_directory = '../Credentials'):
        self.port = None
        self.email = None
        self.receiver_email = None
        self.email_subject = None
        self.password = None
        self.get_credentials(credentials_directory)
        
    def __del__(self):
        pass

    def get_credentials(self, credentials_directory):        
        if os.path.exists(credentials_directory):
            f = open(credentials_directory + '/gmail.json', 'r')
            credentials = json.load(f)
            f.close()

            self.email = credentials['email']
            self.port = credentials['port']
            self.password = credentials['password']
            credentials.clear()

        else:
            print("Credentials dorectory not found.")
            exit()

    def set_sender(self, sender_email):
        self.email = sender_email

    def set_receiver(self, receiver_email):
        self.receiver_email = receiver_email

    def set_password(self, password):
        self.password = password

    def set_port(self, port):
        self.port = port

    def set_subject(self, email_subject):
        self.email_subject = email_subject


    #ACTIONS

    def send(self, email_body):
        message = email.message.Message()
        message['Subject'] = self.email_subject
        message['From'] = self.email
        message['To'] = self.receiver_email
        message.add_header('Content-Type', 'text/html')
        message.set_payload(email_body)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(message['From'], self.password)
        s.sendmail(message['From'], [message['To']], message.as_string().encode('utf-8'))
        print('Email sent')


    def read(self):

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        print('email:', self.email)
        mail.login(self.email, self.password)
        mail.select("inbox")
        _, search_data = mail.search(None, 'UNSEEN')

        my_messages = list()
        for num in search_data[0].split():
            email_data = {}
            _, data = mail.fetch(num, '(RFC822)')
            _, b = data[0]
            email_message = email.message_from_bytes(b)

            for header in ['subject', 'to', 'from', 'date']:
                print("{}: {}".format(header, email_message[header]))
                email_data[header] = email_message[header]

            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    #email_data['body'] = body
                    #print(body.decode())
                elif part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True)
                    #email_data['html_body'] = html_body
                    #print(html_body.decode())
            print()
            #exit()
            #my_messages.append(email_data)

            print(my_messages)
        return my_messages



    


if __name__ == '__main__':
    
    mail = GMail()
    #mail.set_receiver('eduardo.statistic@gmail.com')
    #mail.set_subject('Email test alpha')

    #message = """
    #        <p>Parágrafo1</p>
    #        <p>Parágrafo2</p>
    #        """
    #mail.send(email_body=message)

    mail.read()

