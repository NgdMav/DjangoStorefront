# from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import requests
from rest_framework import permissions
from rest_framework.views import APIView


# @cache_page(5 * 60)
# def say_hello(request):
#     # try:
#     #     # send_mail('subject',
#     #     #           'message',
#     #     #           'info@mav.com',
#     #     #           ['xivalor.gmail.com'])
#     #     # mail_admins('admin_subject',
#     #     #             'admin_message',
#     #     #             html_message='<p>Hello Admin!</p>')
#     #     # message = EmailMessage('subject',
#     #     #              'message',
#     #     #              'from@mail.com',
#     #     #              ['xivalor@mail.com'])
#     #     # message.attach_file('playground/static/images/vinland.png')
#     #     # message.send()
#     #     message = BaseEmailMessage(
#     #         template_name='emails/hello.html',
#     #         context={'name': 'Mav'},
#     #     )
#     #     message.send(['xivalor@domain.com'])
#     # except BadHeaderError:
#     #     pass
#     # notify_customers.delay('Hello, celery')
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'hello.html', {"name": data})


class HelloView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {"name": "Mav"})