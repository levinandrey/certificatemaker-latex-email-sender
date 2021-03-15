from django.shortcuts import render

# Create your views here.

#print

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


from import_export import resources

from import_export.admin import ImportExportModelAdmin

from django.template import Context


def link_callback(uri, rel):

    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/


    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)


    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path








from io import StringIO

def print_to_pdf(file_name, path_to_template, context):
    template = get_template(path_to_template)
    html = template.render(context)
    f = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(cStringIO.StringIO(html.encode('utf-8')), dest=f, link_callback=link_callback, encoding='UTF-8', show_error_as_pdf=True)
    f.seek(0)
    pdf = f.read()
    f.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + file_name + '.pdf"'

    return response



def context_base_admin():
    return Context({
    })



def get_test_pdf(request):

    context = context_base_admin()

    context = context_base_admin()
    context['time'] = datetime.datetime.now()
    context['name'] = 'Andrey Levin'

    file_name = 'test-one-pdf'
    path_to_template = 'pdf-template-one.html'

    response = print_to_pdf(file_name, path_to_template, context.flatten())

    return response




from django.http import HttpResponse
import datetime


def get_pdf(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)















