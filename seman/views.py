from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import HttpResponse
from .domain.reader import Reader
from .domain.parser import Parser
import requests
import re
from operator import itemgetter

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
                cache.set('report', parsedData)
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
    parseResult = Parser.parseAdvego(response)
    parseResult['semantics'].append(processPunctuationChars(fileContent))
    parseResult['english_words'] = processEnglishWords(fileContent)
    return parseResult

def sort_results(request, command):
    parsedData = cache.get('report')
    if parsedData == None:
        return redirect('/')
    if command == "valueAsc":
        parsedData['semantics'] = sorted(parsedData['semantics'], key=itemgetter('val'), reverse=False)
        parsedData['words'] = sorted(parsedData['words'], key=itemgetter('count'), reverse=False)
        parsedData['stop_words'] = sorted(parsedData['stop_words'], key=itemgetter('count'), reverse=False)
        parsedData['english_words'] = sorted(parsedData['english_words'], key=itemgetter('count'), reverse=False)
    elif command == "valueDesc":
        parsedData['semantics'] = sorted(parsedData['semantics'], key=itemgetter('val'), reverse=True)
        parsedData['words'] = sorted(parsedData['words'], key=itemgetter('count'), reverse=True)
        parsedData['stop_words'] = sorted(parsedData['stop_words'], key=itemgetter('count'), reverse=True)
        parsedData['english_words'] = sorted(parsedData['english_words'], key=itemgetter('count'), reverse=True)
    elif command == "nameAsc":
        parsedData['semantics'] = sorted(parsedData['semantics'], key=itemgetter('title'), reverse=False)
        parsedData['words'] = sorted(parsedData['words'], key=itemgetter('word'), reverse=False)
        parsedData['stop_words'] = sorted(parsedData['stop_words'], key=itemgetter('word'), reverse=False)
        parsedData['english_words'] = sorted(parsedData['english_words'], key=itemgetter('word'), reverse=False)
    else:
        parsedData['semantics'] = sorted(parsedData['semantics'], key=itemgetter('title'), reverse=True)
        parsedData['words'] = sorted(parsedData['words'], key=itemgetter('word'), reverse=True)
        parsedData['stop_words'] = sorted(parsedData['stop_words'], key=itemgetter('word'), reverse=True)
        parsedData['english_words'] = sorted(parsedData['english_words'], key=itemgetter('word'), reverse=True)
    return render(request, 'seman/result.html', parsedData)

def processPunctuationChars(fileContent):
    punctuationChars = re.findall(r'\.|,|\?|-|;|:|!', fileContent)
    result = {
        'title': 'Знаки пунктуации',
        'val': len(punctuationChars)
    }
    return result

def processEnglishWords(fileContent):
    englishWords = re.findall(r'\w*[а-яА-Я]*[a-zA-Z]+[а-яА-Я]*\w*', fileContent)
    countOfEnglishWords = len(englishWords)
    uniqueEnglishWords = list(set(englishWords))
    englishWordsResult = []
    for uniqueEnglishWord in uniqueEnglishWords:
        countUniqueEnglishWord = englishWords.count(uniqueEnglishWord)
        englishWordsResult.append({
            'word': uniqueEnglishWord,
            'count': countUniqueEnglishWord,
            'frequency': round(100 / countOfEnglishWords * countUniqueEnglishWord, 2)
        })
    return sorted(englishWordsResult, key=itemgetter('count'), reverse=True)

def create_pdf(request):
    from Idz.settings import MEDIA_ROOT_W,BASE_DIR
    import pdfkit
    import os

    if request.method == 'POST':

        # from selenium import webdriver
        #
        # DRIVER = BASE_DIR + '\\Idz\\phantomjs\\bin\\phantomjs.exe'
        #
        # driver = webdriver.PhantomJS(DRIVER)
        # driver.get("https://ru.stackoverflow.com/")
        # screenshot = driver.save_screenshot(MEDIA_ROOT_W + "\\my_screenshot.png")
        # driver.quit()

        str_html = request.POST.get('html')

        path_wkhtmltopdf = BASE_DIR + '\\Idz\\wkhtmltox\\bin\\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        pdf = MEDIA_ROOT_W + '\\out.pdf'
        pdfkit.from_string(str_html, pdf, configuration=config)
        return HttpResponse('true')
    else:
        return HttpResponse('false')



