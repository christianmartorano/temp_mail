try:
    import requests
except Exception as e:
    print("Instalar biblioteca requests")

try:
    from bs4 import BeautifulSoup
except Exception as e:
    print("Instalar biblioteca bs4")

import re

from helper import prog_bar

def mail_capture(args):

    url = "https://tempail.com/pt/"

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }

    with requests.Session() as s:
        try:
            r = s.get(url, headers=headers)
        except Exception as e:
            print("Erro na requisição GET!")

        email = BeautifulSoup(r.text, 'html.parser').find('input', {'class':'adres-input'}).get('value')

        print('E-mail para utilizar: {0}'.format(email))

        while True:
            prog_bar.prog_bar_show(args.seg)
            r = s.get(url, headers=headers)
            emails = BeautifulSoup(r.text, 'html.parser').findAll(id=re.compile('^(mail_)\d{8,}$'))
            for e in emails:
                #Acessando os e-mails
                #print(e)
                print('{}\nRemetente: {} - Assunto: {}'.format(email, e.find('div', {'class':'gonderen'}).getText(), e.find('div', {'class':'baslik'}).getText()))

                try:
                    e_request = s.get(e.find('a')['href'])
                except Exception as e:
                    print('Erro na requisição GET!')

                file_download = open('tmp{0}{}{0}{}.html'.format(os.sep, email,
                                e.find('a')['href'].rstrip('/').split('/')[-1]), 'wb').write(e_request.content)
