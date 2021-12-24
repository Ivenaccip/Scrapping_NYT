import requests
import lxml.html as html


#Los links aparecen sin la verificación


#Invalid URL '/es/2021/12/20/espanol/gabriel-boric-chile-elecciones.html': No schema supplied. Perhaps you meant http:///es/2021/12/20/espanol/gabriel-boric-chile-elecciones.html?


URL = 'https://www.nytimes.com/es/'
URL2 = 'https://www.nytimes.com'

links = '//h2[@class = "css-byk1jx e1hr934v1"]/a/@href'
titulo = '//div[@class = "css-1vkm6nb ehdk2mb0"]/h1/text()'
articulo = '//div[@class = "css-53u6y8"]/p[@class = "css-axufdj evys1bk0"]/text()'



def parse_home():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            Home = response.content.decode('utf-8')
            parsed = html.fromstring(Home)
            links_to_notice = parsed.xpath(links)
            print(links_to_notice)
            for link in links_to_notice:
                corregido = URL2 + link
                print(corregido)
        else:
            raise ValueError(f'Error:  {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()


if __name__ == '__main__':
    run()