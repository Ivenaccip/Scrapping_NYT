import requests
from requests.models import Response
import lxml.html as html
import os #crea una carpeta con la fecha de hoy
import datetime #trae la fecha de hoy

HOME_URL = 'https://www.nytimes.com/es/'

XPATH_LINK_TO_ARTICLE = '//h2[@class = "css-byk1jx e1hr934v1"]/a/@href' #Anteriormente funcionaba con: //h2[@class = "headline"]/a/@href, se actualizó
XPATH_TITLE = '//div[@class = "css-1vkm6nb ehdk2mb0"]/h1/text()'
#XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_BODY = '//div[@class = "css-53u6y8"]/p[@class = "css-axufdj evys1bk0"]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link) 
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            #parsed va a tener el html que tendrá el xpath

            try:
                title = parsed.xpath(XPATH_TITLE)[1]
                #esto tuvo que ser modificado el indice, debido a que la actualizacion no corria con h2
                #en el caso del titulo, solamente entrarán si no tienen comillas
                title = title.replace('\"', '')
                #summary = parsed.xpath(XPATH_SUMMARY)[0]
                #puede que haya noticias que no tienen resumen, por lo que daria un error, por lo que solo tomará noticias con resumen
                body = parsed.xpath(XPATH_BODY)#En este caso no vamos a utilizar 0, porque es una lista de parrafos
            except IndexError:
                return


            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                #f.write(summary)
                f.write('\n\n')
                for p in body: #esto es porque son varias listas
                    f.write(p)
                    f.write('\n')
            #va a buscar la carpeta que se creo anteriormente con la fecha y el titulo de hoy
            #manejador contextual, si tu archivo se cierra, entonces mantiene todo seguro
            #guardar en un archivo
            #w es para modo escritura
            #encoding para carcter especial se transforma
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        #si el estatus código no es 200, entonces va a imprimir el error


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            #response.content devuelve documento html de la respuesta
            #decode transforma información ñ y tildes 
            parsed = html.fromstring(home)
            #toma el contenido de html en home ↑ y lo transforma en xpath
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices) para comprobar que todo salga bien

            today = datetime.date.today().strftime('%d-%m-%Y')
            #datetime ayuda a traer fechas
            #strftime entrega el formato en el que quieres las cosas
            if not os.path.isdir(today):
                #pregunta si no existe os.path toady hace algo
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
            #la f la estamos usando para un mensaje personalizado
            #al parecer con {} podemos recuperar datos dentro de un text
    except ValueError as ve: #Esto lo vamos a hacer porque no siempre tendremos un file200
        #a veces tendremos un 404 que marcará error
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()