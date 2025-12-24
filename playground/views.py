from django.shortcuts import render
from django.core.mail import EmailMessage, BadHeaderError
from store.models import Product, Collection


def say_hello(request):
    try:
        # send_mail('subject',
        #           'message',
        #           'info@mav.com',
        #           ['xivalor.gmail.com'])
        # mail_admins('admin_subject',
        #             'admin_message',
        #             html_message='<p>Hello Admin!</p>')
        message = EmailMessage('subject',
                     'message',
                     'from@mail.com',
                     ['xivalor@mail.com'])
        message.attach_file('playground/static/images/vinland.png')
        message.send()
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {"name": "Mav"})
