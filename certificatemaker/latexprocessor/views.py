from django.shortcuts import render

# Create your views here.

#print


from django.template.loader import get_template


from import_export import resources

from import_export.admin import ImportExportModelAdmin

from django.template import Context



import subprocess, os, sys, io, datetime, pwd



from .models import LatexProcess
from preprintrecorder.models import PrePrintRecord
from certificatestore.models import Certificate, CertificateOrgy


from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files import File
from django.template import Template

from slugify import slugify_ru






def read_file(file_path = '', mode = 'r', encoding="utf-8"):

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


def write_file(file_path = '', content = '', mode = 'w+', encoding="utf-8"):
    with open(file_path, mode=mode) as file:
        try:
            file.write(content)
        except Exception as e:
            print(e)
            return


    return True



def run_linux_command(command='', shell=True, timeout=30):
    p = subprocess.Popen(command, shell=shell, stderr=subprocess.PIPE)

    p.wait(timeout=timeout)

    return True



def get_list_of_attrs(attrs_input):

    list_of_split_attrs = attrs_input.split(',')
    #print('GET list_of_split_attrs', list_of_split_attrs)
    if not len(list_of_split_attrs):
        return []

    attrs = []
    for attr in list_of_split_attrs:
        #print('ATTR', attr)
        if len(attr) < 1:
            continue
        #print('APPEND', attr)

        attrs.append(attr)

    return attrs


def change_user(user = 'www-data'):
    user_id = 33
    os.setgid(user_id)
    os.setuid(user_id)



def name_string_checker(name):

    if not len(name):
        name = '\hspace{0pt}'

    return name


def get_translated(text, src='ru', dest='en'):
    #from googletrans import Translator
    from translate import Translator

    translator = Translator(from_lang=src, to_lang=dest)
    translate = translator.translate(text)

    return translate



def make_certificate(preprint_record, orgy):

    change_user()

    UPLOAD_TO_ATTACHMENTS = 'attachments'

    LATEX_PROCESS_CYCLE_NUMBER = 3



    print('preprint_record', preprint_record.id)

    context = Context()


    context['pathtoattachments'] = os.path.join(settings.MEDIA_ROOT, UPLOAD_TO_ATTACHMENTS, ) + '/'

    context['lastname'] = name_string_checker(preprint_record.last_name)
    context['firstname'] = name_string_checker(preprint_record.first_name)
    context['secondname'] = name_string_checker(preprint_record.second_name)

    context['gender_female'] = False
    if preprint_record.gender == 'f':
        context['gender_female'] = True


    context_attrs_names = get_list_of_attrs(preprint_record.process.attrs_names)
    context_attrs = get_list_of_attrs(preprint_record.attrs)

    #print('preprint_record.process.attrs_names', preprint_record.process.attrs_names)
    #print('context_attrs_names', context_attrs_names)
    #print('preprint_record.attrs', preprint_record.attrs)
    #print('context_attrs',context_attrs)





    for attr_index in range(len(context_attrs_names)):
        context[context_attrs_names[attr_index]] = context_attrs[attr_index]


    print('Context', context)
    print('OK', 'Make attrs')


    process = preprint_record.process

    template_path = process.template.upload.path
    if not template_path:
        return
    print('OK', 'Get template path')


    template_content = read_file(template_path)
    if not template_content:
        return
    print('OK', 'Read template')


    try:
        template = Template(template_content)
    except Exception as e:
        print(e)
        return

    print('OK', 'Load template')



    try:
        output_render_template = template.render(context)
    except Exception as e:
        print(e)
        return
    print('OK', 'Render template')



    # Clear all temp data
    result = run_linux_command('rm output*')
    if not result:
        return
    print('OK', 'rm output*')



    output_temp_name = 'output-temp'
    path_output_latex_temp_name = os.path.join(settings.BASE_DIR, output_temp_name + '.tex')


    result = write_file(path_output_latex_temp_name, output_render_template, encoding=None)
    if not result:
        return
    print('Write_file', 'output_latex_temp')


    latex_command_to_gen_pdf = 'pdflatex  ' + path_output_latex_temp_name
    for cycle in range(LATEX_PROCESS_CYCLE_NUMBER):
        print('Cycle', cycle, 'start')
        result = run_linux_command(latex_command_to_gen_pdf, shell=True)
        if not result:
            print('RESULT', result)
            return

        print('OK', 'Cycle', cycle, '\n\n')

    certificate = Certificate.objects.create()
    print('OK', 'Create certificate')



    print(get_translated('матем'))

    subject_en = ''

    if 'subject' in context:
        subject_en = get_translated(context['subject'])

    list_file_name = [
        'certificate',
        slugify_ru(context['lastname'], to_lower = True ),
        slugify_ru(context['firstname'][0], to_lower = True ),
        slugify_ru(context['secondname'][0], to_lower = True ),
        slugify_ru(subject_en, to_lower=True),
        slugify_ru(preprint_record.process.slug, to_lower = True ),
        'aesc',
        slugify_ru(str(certificate.created), to_lower = True ).replace('-00-00',''),
    ]
    certificate_file_name = '-'.join(list_file_name) + '.pdf'



    result = run_linux_command('cp -p ' + output_temp_name + '.pdf' + ' ' + 'media/certificates/' + certificate_file_name)
    if not result:
        return
    print('OK', 'cp -p  ')

    #result = run_linux_command(
    #    'ps2pdf -dPDFSETTINGS=/prepress ' + 'media/certificates/' + 'small-' + certificate_file_name + ' ' +'media/certificates/' + certificate_file_name)
    #if not result:
    #    return
    #print('OK', 'ps2pdf  ')


    # For make sign
    #run_linux_command('ps2pdf -dPDFSETTINGS=/prepress output-temp-latex-processor.pdf output-final.pdf')

    #path_temp_pdf_file = os.path.join(settings.BASE_DIR, output_temp_name + '.pdf')

    #pdf_temp_file = read_file(path_temp_pdf_file, mode='rb', encoding=None)
    #if not pdf_temp_file:
    #    return
    #print('Read_file', 'pdf_temp_file', 'OK')




    certificate.upload = 'certificates/' + certificate_file_name
    print('OK', 'Set name')
    #print('Join slug name')

    print('certificate_file_name', certificate_file_name)
    certificate.filename = certificate_file_name
    print('OK', 'Set name')


    #certificate.upload = pdf_temp_file
    print('OK', 'COMMENT certificate.upload')

    certificate.parent_record = preprint_record
    print('OK', 'certificate.parent_record')

    certificate.latex_process = preprint_record.process
    print('OK', 'certificate.latex_process')



    certificate.orgy = orgy
    print('OK', 'Set orgy')



    certificate.save()
    print('OK', 'Save cert')

    # Clear all temp data

    result = run_linux_command('rm output*')
    if not result:
        return
    print('OK', 'rm output*')


    preprint_record.gen_cert = True
    preprint_record.save()


    return




def get_pdfs(queryset = ''):

    orgy = CertificateOrgy.objects.create()

    list_of_records = queryset

    if not isinstance(queryset, list):
        list_of_records = PrePrintRecord.objects.filter(gen_cert=False).order_by('id')

    print('len(list_of_records)', len(list_of_records))

    for record in list_of_records:
        certificate = make_certificate(record, orgy)
        print('\n\n ================================== \n\n')



    now = datetime.datetime.now()
    html = '\nTime now ' + str(now)

    print(html)













def import_csv_into_preprint_recorder():

    file_to_read = 'io-aesc-dimploms-21-03-14.csv'

    data = read_file(file_to_read)

    list_of_split_data = data.split('\n')

    print('LEN', len(list_of_split_data))

    for row in list_of_split_data[1:]:
        cols = row.split(',')

        if len(cols) < 2:
            print('len(cols) < 2', 'ROW', row, 'COLS', cols)
            continue

        #print(row)

        last_name = cols[1]
        first_name = cols[2]
        second_name = cols[3]
        email = cols[0]
        gender = cols[4]
        process_slug = cols[5]
        attrs = ''
        for attr in cols[6:]:
            attr += ','
            attrs += attr


        processes = LatexProcess.objects.filter(slug=process_slug)
        if not len(processes):
            print('len(processes)')
            continue

        process = processes[0]

        record = PrePrintRecord.objects.create(
            last_name=last_name,
            first_name=first_name,
            second_name=second_name,
            gender=gender,
            email=email,
            attrs=attrs,
            process=process,
        )
        record.save()

        #print('OK', '\n\n')


# def get_test():
#
#
#     t = b''
#
#     path_temp_pdf_file = '/var/www/certificatemaker/certificatemaker/test.pdf'
#
#     pdf_temp_file = read_file(path_temp_pdf_file, mode='rb', encoding=None)
#     if not pdf_temp_file:
#         return
#     print('OK', 'Read_file', 'pdf_temp_file')
#
#
#     certificate = TestCertificate.objects.create()
#     print('OK', 'Create certificate')
#
#
#     certificate_file_name = 'test-cert.pdf'
#     certificate.filename = certificate_file_name
#     print('OK', 'Set name', 'OK')
#
#     from django.core.files.base import ContentFile
#     import base64
#
#     pdf_temp_file = ContentFile(base64.b64decode(pdf_temp_file))
#
#     print('pdf', '\n\n\n', pdf_temp_file)
#
#     certificate.upload = pdf_temp_file
#     print('OK', 'certificate.upload')
#
#
#     certificate.save()
#     print('OK', 'Save cert')



def test():
    path = Certificate.upload.path
    print('path', path)




def make_gen():
    preprints = PrePrintRecord.objects.all()

    print('len(preprints)',len(preprints))


    counter = 0
    for preprint in preprints:
        certificates = Certificate.objects.filter(parent_record=preprint)

        print('len(certificates)', len(certificates),)

        if not len(certificates):
            continue

        counter += 1

        preprint.gen_cert = True
        preprint.save()



    print('counter', counter)




def un_gne_preprint():

    process = LatexProcess.objects.get(slug='dist')
    preprints = PrePrintRecord.objects.filter(process=process)

    print('LEN', len(preprints))

    for preprint in preprints:
        preprint.gen_cert = False
        preprint.save()

