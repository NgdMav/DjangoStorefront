from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError
from store.models import Product, Collection


def say_hello(request):
    try:
        send_mail('subject',
                  'message',
                  'info@mav.com',
                  ['xivalor.gmail.com'])
        mail_admins('admin_subject',
                    'admin_message',
                    html_message='<p>Hello Admin!</p>')
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {"name": "Mav"})
