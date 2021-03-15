from jinja2 import Template

import subprocess, os, sys


def read_file(file):
    f = open(file, "r")
    data = f.read()
    f.close()
    return data
    

    
def write_file(file, data):
    f = open(file, "w")
    f.write(data)
    f.close()


def run_command(command = ''):
    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    p.wait(timeout=30)


def generate_pdf(lastname = 'Levin', name = 'Andrey', surname = 'Aleksandrovich'):
    template_file = 'template-aesc-cdo-certificate-example.tex'

    template_file_text = read_file(template_file)
    
    template = Template(template_file_text)
    output_data = template.render(lastname=lastname, name=name, surname=surname)
    
    tex_tmp_file = 'output.tex'
    write_file(tex_tmp_file, output_data)
    
    pdflatex_com = 'pdflatex ' + tex_tmp_file
    
    print(pdflatex_com)

    run_command('ls -lh')

    run_command(pdflatex_com)
    
    run_command(pdflatex_com)
    
    run_command(pdflatex_com)
    
    run_command('ps2pdf -dPDFSETTINGS=/prepress output.pdf andrey-levin-certificate.pdf')
    
    
    run_command('rm output.*')
    
    
    


    
    
    print('End')
    
   
    
    
generate_pdf()

