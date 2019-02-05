import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import user_email, password_email, DEFAULT_SMTP, \
    DEFAULT_IMAP, MAIL_SELECT


class MailHandler:
    def __init__(self, user_login, password, smtp=DEFAULT_SMTP,
                 imap=DEFAULT_IMAP):
        self.user_login = user_login
        self.password = password
        self.smtp = smtp
        self.imap = imap

    def send_a_message(self, recipients, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.user_login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        ms = smtplib.SMTP(self.smtp, 587)
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

    def receive_a_message(self, header=None, folder=MAIL_SELECT):
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(self.user_login, self.password)
        mail.list()
        mail.select(folder)
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
    user_1.receive_a_message()
