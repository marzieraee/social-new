
from django.core.mail import EmailMessage

# Create your views here.

class sendemail:
    '''send email with subject and body and the email of user'''
    @staticmethod
    def send_email(data):
        email=EmailMessage(subject=data["subject"],body=data["email_body"],to=[data["to_email"],])
        email.send()