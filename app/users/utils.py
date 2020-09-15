import random
import string
from app import mail
from flask_mail import Message
from flask import render_template
from app import app

def generate_verification_code(size=8):
    verification_code = ''.join(
        [
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            ) for n in range(size)
        ]
    )
    
    return verification_code

def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(
        subject,
        sender=sender,
        recipients=recipients,
    )
    msg.text = text_body
    msg.html = html_body
    mail.send(msg)
    
def send_verification_email(user):
    token = user.generate_token()
    print(token)
    subject = '[FlaskBlog] User Verification'
    sender = app.config['ADMINS'][0]
    recipients = user.email
    text_body = render_template('emails/verification.txt', user=user, token=token)
    html_body = render_template('emails/verification.html', user=user, token=token)
