from bs4 import BeautifulSoup

class Parser:

    @staticmethod
    def parseAdvego(advegoResponse):
        request_bs = BeautifulSoup(advegoResponse.content, 'html.parser')
        divs = request_bs.findAll("table", {"class": "seo_table"})
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
                'stop_words': stop_words,
                'english_words': None
            }
            return content
        else:
            return None
