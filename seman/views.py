from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'seman/index.html')

def upload_file(request):
    if request.method == 'POST':
        if request.FILES:
            type = request.FILES['file'].name.split(".")[-1]
            return HttpResponse(type)
        else:
            return redirect('/')
