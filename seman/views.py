from django.shortcuts import render, redirect
from django.http import HttpResponse
from .domain.reader import Reader
import io
# Create your views here.
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
            # elif type == "doc":
            #    fileContent = Reader.read_doc_file()
            # elif type == "pdf":
            #    fileContent = Reader.read_pdf_file(request.FILES['file'])
            else:
                fileContent = "Ошибка! File with type = " + type + " is not supported!"
            return HttpResponse(fileContent)
        else:
            return redirect('/')
