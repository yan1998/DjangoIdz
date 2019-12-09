from django.shortcuts import render, redirect
from django.http import HttpResponse

import pprint

import requests
from bs4 import BeautifulSoup as BS

# Create your views here.
def index_2(request):
    max_page = 6
    pages = []
    for x in range(1, max_page + 1):
        pages.append(requests.get('https://stopgame.ru/review/new/stopchoice/p' + str(x)))
    titles = []
    for r in pages:
        html = BS(r.content, 'html.parser')
        for el in html.select('.lent-block'):
            title = el.select('.lent-title > a')
            titles.append(title[0].text)
    return HttpResponse(titles)

def autorize(request):
    s = requests.Session()
    auth_html = s.get('https://smartprogress.do/')
    auth_bs = BS(auth_html.content, 'html.parser')
    csrf = auth_bs.select('input[name=YII_CSRF_TOKEN]')[0]['value']

    payload = {
        'YII_CSRF_TOKEN': csrf,
        'returnUrl': '/',
        'UserLoginForm[email]': 'test54321@test.ru',
        'UserLoginForm[password]': '12345',
        'UserLoginForm[rememberMe]': 1
    }

    answ = s.post('https://smartprogress.do/user/login/', data=payload)
    anw_bs = BS(answ.content, 'html.parser')

    print('имя - ' + anw_bs.select('.user-menu__name')[0].text.strip())
    print('уровень - ' + anw_bs.select('.user-menu__info-text--lvl')[0].text.strip())
    print('опыт - ' + anw_bs.select('.user-menu__info-text--exp')[0].text.strip())

    return HttpResponse('1')

def index(request):
    if request.method == "POST":
        # Текст не может быть больше 100 000
        if request.POST['text'] != "":
            postload = {
                'id_lang': 'ru',
                'job_text': request.POST['text']
            }
            s = requests.Session()
            answ = s.post('https://advego.com/text/seo/', data=postload)
            anw_bs = BS(answ.content, 'html.parser')

            divs = anw_bs.findAll("table", {"class": "seo_table"})
            if divs:
                table_trs = divs[0].findAll('tr')
                semantics = []
                for i in range(1, len(table_trs)):
                    semantics.append({
                        'title': table_trs[i].findAll('td')[0].text.strip(),
                        'val': table_trs[i].findAll('td')[1].text.strip()
                    })


                words = []
                table_word_trs = divs[2].findAll('tr')
                for i in range(1, len(table_word_trs)):
                    cur = table_word_trs[i]
                    words.append({
                        'word': cur.findAll('td')[0].text.strip(),
                        'count': cur.findAll('td')[1].text.strip(),
                        'frequency': cur.findAll('td')[2].text.strip()
                    })

                stop_words = []
                stop_words_trs = divs[3].findAll('tr')
                for i in range(1, len(stop_words_trs)):
                    cur = stop_words_trs[i]
                    stop_words.append({
                        'word': cur.findAll('td')[0].text.strip(),
                        'count': cur.findAll('td')[1].text.strip(),
                        'frequency': cur.findAll('td')[2].text.strip()
                    })

                content = {
                    'semantics': semantics,
                    'words': words,
                    'stop_words': stop_words
                }
                return render(request, 'parser/result.html', content)
            else:
                return HttpResponse('Перейдите на сайт и пройдите рекапчу <a href="https://advego.com/text/seo/">Ссылка</a>')
        else:
            return redirect('parser')
    else:
        return render(request, 'parser/index.html')
