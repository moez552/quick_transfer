from quick_transfer.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def send_account_verification(key,name,receiver):
    link = 'prefix/'+key
    send_mail(
    'Quick transfer Email verification',
    "Hello {}, this is supposed to be a template for the email verification so here is you key {} or you can use the link: {}".format(name,key,link),
    EMAIL_HOST_USER,
    [receiver],
    fail_silently=False)
