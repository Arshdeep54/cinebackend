from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def sendEmail(data):
        email=EmailMessage(
            subject=data['email_subject'],
            body=data["email_body"],
            from_email=os.environ.get('EMAIL_HOST'),
            to=[data['email_to']]
        )
        email.send()
