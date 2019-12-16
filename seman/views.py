from django.shortcuts import render, redirect
from django.http import HttpResponse
from .domain.reader import Reader
from .domain.parser import Parser
import requests
import json

def index(request):
    return render(request, 'seman/index.html')

def upload_file(request):
    if request.method == 'POST':
        if request.FILES:
            type = request.FILES['file'].name.split(".")[-1]
            fileContent = str()
            if type == "txt":
                fileContent = Reader.read_txt_file(request.FILES['file'])
            elif type == "docx":
                fileContent = Reader.read_docx_file(request.FILES['file'])
            elif type == "pdf":
                fileContent = Reader.read_pdf_file(request.FILES['file'])
            # elif type == "doc":
            #    fileContent = Reader.read_doc_file()
            else:
                return HttpResponse('Ошибка! Файл с расширением " + type + " не поддерживается!')

            if len(fileContent) > 100000:
                return HttpResponse('Ошибка! Количество символов не должно превышать 100 000! Текущее количество = ' + str(len(fileContent)))
            
            parsedData = processTextViaAdvego(fileContent)
            if parsedData == None:
                return HttpResponse('Перейдите на сайт и пройдите рекапчу <a href="https://advego.com/text/seo/">Ссылка</a>')
            else:
                return render(request, 'seman/result.html', parsedData)
        else:
            return HttpResponse('Ошибка! Файл не был прикреплен!')

def processTextViaAdvego(fileContent):
    postload = {
        'id_lang': 'ru',
        'job_text': fileContent
    }
    s = requests.Session()
    response = s.post('https://advego.com/text/seo/', data=postload)
    return Parser.parseAdvego(response)
