from flask import render_template
from flask.ext.mail import Message

from config import ADMINS
from app import app, mail
from app.decorators import async


@async
def send_async_email(app, msg):
  # the application context required by Flask-Mail will not be
  # automatically set, so the app instance is passed to the thread,
  # and the application context is set up manually
  with app.app_context():
    mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
  """Sends an email using Flask-Mail library
  """
  msg = Message(subject, sender=sender, recipients=recipients)
  msg.body = text_body
  msg.html = html_body
  send_async_email(app, msg)


def follower_notification(followed, follower):
  """Send an email when a user (follower) follows another user (followed)
  """
  send_email(
    "[microblog] %s is now following you!" % follower.nickname,
    ADMINS[0],
    [followed.email],
    render_template(
      "follower_email.txt",
      user=followed,
      follower=follower
    ),
    render_template(
      "follower_email.html",
      user=followed,
      follower=follower
    )
  )
