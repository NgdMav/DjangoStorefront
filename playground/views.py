from django.core.cache import cache
from django.shortcuts import render
import requests

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
    # notify_customers.delay('Hello, celery')
    key = 'httpbin_result'
    if cache.get(key) is None:
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        cache.set(key, data)
    return render(request, 'hello.html', {"name": cache.get(key)})
