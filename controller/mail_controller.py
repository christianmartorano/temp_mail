try:
    import requests
except Exception as e:
    print("Instalar biblioteca requests")

try:
    from bs4 import BeautifulSoup
except Exception as e:
    print("Instalar biblioteca bs4")

import re

import os

from helper import prog_bar

def mail_capture(args):

    url = "https://tempail.com/pt/"

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }

    with requests.Session() as s:
        try:
            request = s.get(url, headers=headers)
        except Exception as e:
            print("Erro na requisição GET!")

        email = BeautifulSoup(request.text, 'html.parser').find('input', {'class':'adres-input'}).get('value')

        print('E-mail para utilizar: {0}'.format(email))

        while True:
            prog_bar.prog_bar_show(args.seg)
            request = s.get(url, headers=headers)
            emails = BeautifulSoup(request.text, 'html.parser').findAll(id=re.compile('^(mail_)\d{8,}$'))
            for e in emails:
                #Acessando os e-mails
                #print(e)
                print('{}\nRemetente: {} - Assunto: {}'.format(email, e.find('div', {'class':'gonderen'}).getText(), e.find('div', {'class':'baslik'}).getText()))

                try:
                    request = s.get(e.find('a')['href'], headers=headers)
                except Exception as e:
                    print('Erro na requisição GET!')

                html_page = BeautifulSoup(request.text, 'html.parser')

                try:
                    request = s.get(html_page.find('iframe')['src'], headers=headers)
                except Exception as e:
                    print('Erro na requisição GET!')

                if not os.path.exists('tmp{0}{1}'.format(os.sep, email)):
                    os.makedirs('tmp{0}{1}'.format(os.sep, email))


                file_download = open('tmp{0}{1}{0}{2}.txt'.format(os.sep, email,
                                html_page.find('iframe')['src'].split('&')[-1]), 'w').write(BeautifulSoup(request.text,
                                'html.parser').find('div',{'dir':'ltr'}).get_text())

                #Excluir e-mail
                params = html_page.find('button',{'onclick':re.compile('^(sil_posta\\(")\\w{1,}(",")\\d{1,}("\\));$')})['onclick'].replace('"',
                                '').split('(')[1].replace(');','').split(',')


                data = {
                    'oturum':html_page.find('iframe')['src'].split('/?')[-1].split('&')[0].split('=')[-1],
                    'veri[]':[params[0],params[1]]
                }

                try:
                    s.post('{}api/sil/'.format(url), data=data, headers=headers)
                except Exception as e:
                    print('Erro na requisição POST!')
