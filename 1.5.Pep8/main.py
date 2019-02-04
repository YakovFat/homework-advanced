import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import user_email, password_email


class MailHandler:
    def __init__(self, user_login, password, DEFAULT_SMTP="smtp.gmail.com",
                 DEFAULT_IMAP="imap.gmail.com", MAIL_SELECT="inbox"):
        self.user_login = user_login
        self.password = password
        self.DEFAULT_SMTP = DEFAULT_SMTP
        self.DEFAULT_IMAP = DEFAULT_IMAP
        self.MAIL_SELECT = MAIL_SELECT

    def send_a_message(self, recipients, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.user_login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        ms = smtplib.SMTP(self.DEFAULT_SMTP, 587)
        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()

        ms.login(self.user_login, self.password)
        ms.sendmail(self.user_login, recipients, msg.as_string())

        ms.quit()
        # send end

    def receive_a_message(self, header):
        mail = imaplib.IMAP4_SSL(self.DEFAULT_IMAP)
        mail.login(self.user_login, self.password)
        mail.list()
        mail.select(self.MAIL_SELECT)
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        mail.logout()
        # end recieve
        return email_message


if __name__ == '__main__':
    user_1 = MailHandler(user_email, password_email)
    user_1.send_a_message(['vasya@email.com', 'petya@email.com'],
                          'Subject', 'Message')
    user_1.receive_a_message(None)
