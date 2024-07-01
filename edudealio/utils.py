import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import uuid

def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_email(email, otp):
    subject = 'Verification'

    # Render the HTML template
    html_content = render_to_string(
        'edudealio/email_templates/register-otp.html',{'otp':otp})
    text_content = strip_tags(html_content)

    # Create the EmailMultiAlternatives object
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])

    # Attach the HTML content to the email
    msg.attach_alternative(html_content, "text/html")

    # Send email
    msg.send()

def send_subscription_successful_email(email):
    subject = 'Subscription Successful'

    # Render the HTML template
    html_content = render_to_string(
        'edudealio/email_templates/subscribe-email.html')
    text_content = strip_tags(html_content)

    # Create the EmailMultiAlternatives object
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])

    # Attach the HTML content to the email
    msg.attach_alternative(html_content, "text/html")

    # Send email
    msg.send()

def send_signup_successful_email(email,name):
    subject = 'Welcome to EduDealio!'

    # Render the HTML template
    html_content = render_to_string(
        'edudealio/email_templates/signup-email.html',
        {'name':name})
    text_content = strip_tags(html_content)

    # Create the EmailMultiAlternatives object
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])

    # Attach the HTML content to the email
    msg.attach_alternative(html_content, "text/html")

    # Send email
    msg.send()

def send_message_successful_email(email,name,message):
    subject = 'Message Received'
    # Render the HTML template
    html_content = render_to_string(
        'edudealio/email_templates/message-email.html',
        {
            'name':name,
            'message':message
            })
    text_content = strip_tags(html_content)

    # Create the EmailMultiAlternatives object
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])

    # Attach the HTML content to the email
    msg.attach_alternative(html_content, "text/html")

    # Send email
    msg.send()

def generate_referral_code():
    """Generates an 8-character code"""
    return str(uuid.uuid4()).replace('-', '')[:8]

def send_referee_successful_email(referee_email,referee_name,referrer_name):
    subject = 'Congratulations on being Referred to Edudealio!'
    # Render the HTML template
    html_content = render_to_string(
        'edudealio/email_templates/referee-email.html',
        {
            'referee_name':referee_name,
            'referrer_name':referrer_name
            })
    text_content = strip_tags(html_content)

    # Create the EmailMultiAlternatives object
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [referee_email])

    # Attach the HTML content to the email
    msg.attach_alternative(html_content, "text/html")

    # Send email
    msg.send()

def send_referrer_successful_email(referrer_email,referee_name,referrer_name):
    subject = 'Congratulations on Referring to Edudealio!'
    # Render the HTML template
    html_content = render_to_string(
        'edudealio/email_templates/referrer-email.html',
        {
            'referee_name':referee_name,
            'referrer_name':referrer_name
            })
    text_content = strip_tags(html_content)

    # Create the EmailMultiAlternatives object
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [referrer_email])

    # Attach the HTML content to the email
    msg.attach_alternative(html_content, "text/html")

    # Send email
    msg.send()