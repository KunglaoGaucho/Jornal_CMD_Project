import requests
from bs4 import BeautifulSoup


class Sites:
    def __init__(self, site):
        self.sites = site
        self.news = []

    def update_news(self):
        if self.sites.lower() == 'globo':
            url = 'https://www.globo.com/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
            page = requests.get(url, headers=browsers)

            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')

            noticias = soup.find_all('a')

            tg_class1 = 'post__title'
            tg_class2 = 'post-multicontent__link--title__text'

            news_dict_globo = {}

            for noticia in noticias:
                if noticia.h2 is not None:
                    if (tg_class1 in noticia.h2.get('class')) or (tg_class2 in noticia.h2.get('class')):
                        news_dict_globo[noticia.h2.text] = noticia.get('href')

            self.news = news_dict_globo

        if self.sites.lower() == 'cnn':
            url = 'https://www.cnnbrasil.com.br/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
            page = requests.get(url, headers=browsers)

            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')

            noticias = soup.find_all('a')

            tg_class1 = 'block__news__title'
            tg_class2 = 'block__news__title sidebar--item__title'

            news_dict_cnn = {}

            for noticia in noticias:
                if noticia.h3 is not None:
                    if (tg_class1 in noticia.h3.get('class')) or (tg_class2 in noticia.h3.get('class')):
                        news_dict_cnn[noticia.h3.text] = noticia.get('href')

            self.news = news_dict_cnn


self = Sites('cnn')
