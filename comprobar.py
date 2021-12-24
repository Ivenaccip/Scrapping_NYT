import requests
import lxml.html as html
import os
import datetime

from scrapperNYT import parse_notice

URL = 'https://www.nytimes.com/es/'
URL2 = 'https://www.nytimes.com'

links = '//h2[@class = "css-byk1jx e1hr934v1"]/a/@href'
titulo = '//div[@class = "css-1vkm6nb ehdk2mb0"]/h1/text()'
articulo = '//div[@class = "css-53u6y8"]/p[@class = "css-axufdj evys1bk0"]/text()'


def parse_notice(corregido, today):
    try:
        response = requests.get(corregido)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(titulo)[0]
                body = parsed.xpath(articulo)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            Home = response.content.decode('utf-8')
            parsed = html.fromstring(Home)
            links_to_notice = parsed.xpath(links)
            #print(links_to_notice)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notice:
                corregido = URL2 + link
                parse_notice(corregido, today)

        else:
            raise ValueError(f'Error:  {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()


if __name__ == '__main__':
    run()