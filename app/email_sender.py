from flask_mail import Message
from app import mail
from flask import render_template

def send_newsletter(user, articles):
    msg = Message('Your AI Newsletter',
                  sender='noreply@ainewsletter.com',
                  recipients=[user.email])
    msg.body = render_template('email/newsletter.txt', user=user, articles=articles)
    msg.html = render_template('email/newsletter.html', user=user, articles=articles)
    mail.send(msg)
