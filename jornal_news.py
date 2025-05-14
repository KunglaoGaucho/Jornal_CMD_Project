from websites.sites import Sites
import os
from threading import Thread
import time
from datetime import datetime
import sys
import pickle
import webbrowser
from math import ceil
from pytimedinput import timedInput


class JornalNews:

    def __init__(self):
        self.dict_site = {}
        self.all_sites = ['globo', 'cnn']

        self.screen = 0  # Variável que indica o número da página que o programa estará
        self.kill = False  # Variável para encerrar o programa a hora que eu quiser
        self.page = 1  # Variável definida para página que eu estou

        self.news = self._read_file('news') if 'news' in os.listdir() else []  # Armazenará as notícias capturadas pelo programa para que quando reiniciado, elas continuem lá
        self._update_file(self.news, 'news')  # Vai atualizar o arquivo criado
        self.site = self._read_file('site') if 'site' in os.listdir() else []  # Armazenará os site capturados pelo programa para que quando reiniciado, eles continuem lá
        self._update_file(self.site, 'site')  # Vai criar o arquivo novo

        # Loop que colocará os sites e notícias dentro de um dicionário
        for noticiario in self.all_sites:
            self.dict_site[noticiario] = Sites(noticiario)

        self.news_thread = Thread(target=self.update_news)
        self.news_thread.setDaemon(True)
        self.news_thread.start()

    # Função que atualizará os arquivos
    def _update_file(self, lista, mode='news'):
        with open(mode, 'wb') as fp:
            pickle.dump(lista, fp)

    # Função que irá ler os arquivos
    def _read_file(self, mode='news'):
        with open(mode, 'rb') as fp:
            n_list = pickle.load(fp)
            return n_list

    # Função que trata das opções que o usuário tem para escolher
    def _recieve_command(self, valid_commands, timeout=30):
        command, timed = timedInput('>>', timeout)
        while command.lower()not in valid_commands and not timed:
            print('Comando inválido. Tente novamente\n')
            command, timed = timedInput('>>', timeout)
        command = 0 if command == '' else command
        return command

    # Função que vai fazer as telas funcionarem
    def main_loop(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            match self.screen:

                # Tela principal
                case 0:
                    print('BEM VINDO AO SEU NOTICIÁRIO FAVORITO!')
                    print('Escolha um item do menu:')
                    print('')
                    print('1. Ultímas notícias\n2. Adicionar site\n3. Remover site\n4. Fechar programa\n')
                    self.screen = int(self._recieve_command(['1', '2', '3', '4'], 5))
                    print(self.screen, type(self.screen))

                case 1:
                    self.display_news()
                    command = self._recieve_command(['p', 'a', 'l', 'v'], 5)
                    match command:
                        case 'p':
                            if self.page < self.max_page:
                                self.page += 1

                        case 'a':
                            if self.page > 1:
                                self.page -= 1

                        case 'l':
                            entrada = input('>> Insira o número da matéria que deseja abrir: ')

                            if not entrada.isdigit():
                                print('Entrada inválida! Digite apenas números.')
                            else:
                                link = int(entrada)
                                if link < 1 or link > len(self.filtered_news):
                                    print('Matéria inexistente!')
                                else:
                                    webbrowser.open(self.filtered_news[link - 1]['link'])

                        case 'v':
                            self.screen = 0
                            continue

                # Comando para ativar um site
                case 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Digite o número do site que deseja adicionar para a lista de sites ativos.\nPressione 0 para voltar')
                    print('\tSITES ATIVOS ============\n')
                    for i in self.site:
                        print('\t', i)

                    print('\n\tSITES INATIVOS ============\n')
                    offline_sites = [i for i in self.all_sites if i not in self.site]
                    for i in range(len(offline_sites)):
                        print(f'\t{i + 1}. {offline_sites[i]}')
                    inativos = int(self._recieve_command([str(i) for i in range(len(offline_sites) + 1)], 50))

                    if inativos == 0:
                        self.screen = 0
                        continue
                    self.site += [offline_sites[inativos - 1]]
                    self._update_file(self.site, 'site')

                # Comando para desativar um site
                case 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Digite o número do site que deseja remover. Digite 0 para voltar ao menu.\n')
                    for i in range(len(self.site)):
                        print(f'\t{i + 1}. {self.site[i]}')
                    ativos = int(self._recieve_command([str(i) for i in range(len(self.site) + 1)], 50))
                    if ativos == 0:
                        self.screen = 0
                        continue

                    del self.site[ativos - 1]
                    self._update_file(self.site, 'site')

                # Comando para fechar o programa
                case 4:
                    self.kill = True
                    sys.exit()

    # Função que vai mostrar as notícias, atualizadas e somente dos sites ativos
    def display_news(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'Último update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')

        self.filtered_news = [i for i in self.news if i['fonte'] in self.site]
        self.max_page = ceil(len(self.filtered_news) / 20)  # Arredonda o numero quebrado para o numero maior mais próximo

        if self.page > self.max_page:
            self.page = 1

        constante = (self.page - 1) * 10
        for i, article in enumerate(self.filtered_news[constante:constante + 10]):
            print(f'{constante + i}. {article['data'].strftime('%d/%m/%Y %H:%M')} - {article['fonte'].upper()} - {article['materia']}')
        print(f'Page {self.page}/{self.max_page}')

        print('\n=========================================================================================\n')
        print('Comandos:')
        print('P - Próxima página | A - Página anterior | L - Abrir matéria no navegador | V -  Voltar')

    # Função que atualizará as notícias em tempo real
    def update_news(self):
        while not self.kill:
            for site in self.all_sites:
                self.dict_site[site].update_news()

                for key, value in self.dict_site[site].news.items():
                    dict_aux = {}
                    dict_aux['data'] = datetime.now()
                    dict_aux['fonte'] = site
                    dict_aux['materia'] = key
                    dict_aux['link'] = value

                    if len(self.news) == 0:
                        self.news.insert(0, dict_aux)
                        continue

                    add_news = True
                    for news in self.news:
                        if dict_aux["materia"] == news["materia"] and dict_aux["fonte"] == news["fonte"]:
                            add_news = False
                            break
                    if add_news:
                        self.news.insert(0, dict_aux)
            self.news = sorted(self.news, key=lambda d: d['data'], reverse=True)
            self._update_file(self.news, 'news')
            time.sleep(10)


self = JornalNews()
self.main_loop()
