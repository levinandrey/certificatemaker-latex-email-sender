from django.shortcuts import render

# Create your views here.

from django.core.mail import send_mail, EmailMessage

from .models import Message, MessageStatus



# KEY FROM UNISEMDER MAILER

KEY = 'key-api-key-api-key-api-key-api'

# LIST OF UNISENDER CONTACTS
X = '17301581'

LANG = 'ru'

CC = 'letlevin@gmail.com'





import os, io


def read_file(file_path='', mode='r', encoding="utf-8"):
    if not os.path.exists(file_path):
        print('E path.exists', file_path)
        return

    with io.open(file_path, mode=mode, encoding=encoding) as file:
        try:
            data = file.read()
        except Exception as e:
            print(e)
            return

    if not data:
        print('E Read no DATA')
        return

    return data


import requests
from requests.exceptions import HTTPError
import json


def make_request(url='', attrs={}):



    if not url:
        return None

    response = None

    try:
        response = requests.post(url, data=attrs)
        # print(response.content)
        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()
    except HTTPError as http_err:
        print('HTTP error occurred: ')  # Python 3.6
    except Exception as err:
        print('Other error occurred: ')  # Python 3.6
    else:
        print('Success request!')

    json_response_content = json.loads(response.content.decode('utf-8'))

    print(json.dumps(json_response_content, indent=4, sort_keys=True))

    return json_response_content


import time
from urllib.parse import quote


def send_email(attrs, attachment_file_name='', attachment_data='', certificate = None):
    if attachment_file_name and attachment_data:
        attrs['attachments[' + attachment_file_name + ']'] = attachment_data

    url_send = 'https://api.unisender.com/ru/api/sendEmail'


    response_content = make_request(url=url_send, attrs=attrs)

    print('LNE response_content', len(response_content['result']))

    for res in response_content['result']:
        mstatus = MessageStatus.objects.create()
        if 'email' in res:
            print('res[email]', res['email'])
            mstatus.email_to = res['email']

        if 'id' in res:
            print('res[id]', res['id'])
            mstatus.result_id = res['id']

        mstatus.certificate = certificate
        mstatus.save()



def gen_message():


    subject = message.subject

    email_from = message.email_from
    reply_to = message.reply_to
    body = message.body
    bcc_email = message.bcc_email

    return subject, body, email_from, bcc_email, reply_to



def send(certificate):

    if not certificate:
        print ('not certificate')
        return

    if not certificate.parent_record.email:
        print ('not email')
        return




    messages = Message.objects.filter(slug='sumolymp')

    if not len(messages):
        print('len(messages)')
        return None

    message = messages[0]


    attrs = {}
    attrs['format'] = 'json'
    attrs['api_key'] = KEY

    email_send = certificate.parent_record.email
    print('EMAIL', email_send)
    #email_send = 'svireppka@yandex.ru'
    #email_send = 'adnp@ya.ru'
    print('EMAIL', email_send)

    attrs['email'] = email_send
    attrs['sender_name'] = message.from_name
    attrs['sender_email'] = message.email_from
    attrs['subject'] = message.subject
    attrs['body'] = message.body
    attrs['list_id'] = X
    attrs['lang'] = LANG
    attrs['error_checking'] = '1'

    if message.bcc_email:
        attrs['cc'] = message.bcc_email

    file_path = 'media/' + certificate.upload

    data = read_file(file_path=file_path, mode='rb', encoding=None)

    send_email(attrs,
               attachment_file_name=certificate.upload,
               attachment_data=data,
               certificate=certificate,
               )


from  latexprocessor.models import LatexProcess

from certificatestore.models import Certificate
import time

def send_cert():

    processs =  LatexProcess.objects.filter(slug='sumolymp')
    if not len(processs):
        print('len(processs')
        return

    process = processs[0]


    certificates = Certificate.objects.filter(latex_process=process).filter(id__gte=1727).order_by('created')

    if not len(certificates):
        print('len(certificates')
        return

    print('len(certificates)', len(certificates))

    for certificate in certificates:
        print("CERT: ", certificate.id, certificate.filename)
        send(certificate)

        print('time.sleep(3)')
        time.sleep(3)


def check_emails():
    message_statuses = MessageStatus.objects.all().filter(id__gte=684)

    if not len(message_statuses):
        return

    for mstatus in message_statuses:

        print('id', mstatus.id)

        url_check_email = 'https://api.unisender.com/ru/api/checkEmail'

        attrs = {}

        attrs['format'] = 'json'

        attrs['api_key'] = KEY

        if not mstatus.result_id:
            print('not mstatus.result_id')
            continue

        attrs['email_id'] = mstatus.result_id


        response_content = make_request(url_check_email, attrs)

        time.sleep(1)

        if not 'result' in response_content:
            mstatus.result_status = str(response_content)
            mstatus.save()
            continue

        if not 'statuses' in response_content['result']:
            mstatus.result_status = str(response_content)
            mstatus.save()
            continue

        statuses = response_content['result']['statuses']

        if not len(statuses):
            mstatus.result_status = str(response_content)
            mstatus.save()
            continue

        status = statuses[0]

        mstatus.result_status = status['status']
        mstatus.save()





