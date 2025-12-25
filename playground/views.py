from django.shortcuts import render
from .tasks import notify_customers

def say_hello(request):
    # try:
    #     # send_mail('subject',
    #     #           'message',
    #     #           'info@mav.com',
    #     #           ['xivalor.gmail.com'])
    #     # mail_admins('admin_subject',
    #     #             'admin_message',
    #     #             html_message='<p>Hello Admin!</p>')
    #     # message = EmailMessage('subject',
    #     #              'message',
    #     #              'from@mail.com',
    #     #              ['xivalor@mail.com'])
    #     # message.attach_file('playground/static/images/vinland.png')
    #     # message.send()
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Mav'},
    #     )
    #     message.send(['xivalor@domain.com'])
    # except BadHeaderError:
    #     pass
    notify_customers.delay('Hello, celery')
    return render(request, 'hello.html', {"name": "Mav"})
