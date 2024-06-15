import requests  # Librería para poder acceder a una página
from bs4 import BeautifulSoup  # Librería para poder buscar en el HTML
from flask import Flask, render_template, request


#app = Flask(__name__)
app = Flask(__name__, static_folder='static')

def mostrar_texto(tema):

    url_Wikipedia = "https://es.wikipedia.org/wiki/"  # URL de Wikipedia sin tema

    response = requests.get(url_Wikipedia + tema)  # Cargamos la página de Wikipedia con el tema

    if response.status_code == 200:  # Si no es 200, no se encontró la página o hubo algún tipo de error

        soup = BeautifulSoup(response.content, 'html.parser')  # El contenido que devuelve la página se formateo en HTML para poder analizarlo

        for element in soup.find_all(['sup']):  # Eliminamos los elementos que no queremos mostrar (citas) Busca todos los "sup"
            element.decompose()  #  Saca todos los "sup"

        tag_limitador = soup.find('meta', {'property': 'mw:PageProp/toc'})  # Buscamos el tag limitador de sección (<meta property="mw:PageProp/toc">) para que traiga solamente los primeros párrafos del artículo

        if tag_limitador is not None:  # Preguntamos si encontró el limitador (hay artículos que existen en Wikipedia pero tienen varias posibles opciones para ese término y no tienen el limitador)

            parrafos = tag_limitador.find_all_previous('p')  # Buscamos todos los párrafos que se encuentran antes del tag limitador (va buscando hacia arriba)

            parrafos = list(reversed(parrafos))   # Invertimos la lista de párrafos para mostrarlos en el orden correcto

            texto_para_mostrar = '\n'.join([p.get_text() for p in parrafos])  # Obtenemos el texto plano de los párrafos en una sola variable tipo string

            texto_para_mostrar = tema.title() + '\n\n' + texto_para_mostrar  # Agregamos al texto el tema a modo de título

            return texto_para_mostrar  # Devolvemos el texto
        else:
            return False
    else:
        return False  # Devolvemos falso si no se pudo localizar el texto



@app.route("/")  # La primera vez que se cargue la página la carga "normal"
def index():
     return render_template("index.html")


@app.route("/analizar", methods=["POST"])  # Acá es cuando se carga porque apretaron el botón en el formulario
def analizar_busqueda():
    busqueda = request.form["busqueda"]  # El nombre del input text lo guarda en la variable busqueda

    aux = mostrar_texto(busqueda)  # Busca el tema y lo guarda en una variable aux
    if aux:  # Si no es false, lo encontró entonces en resultado guarda el texto
        resultado = aux 
    else:  # Si es false, no lo encontró entonces en resultado guarda el mensaje
        resultado = "Información no encontrada"    
    return render_template("index.html", resultado=resultado)  #  Recarga la página mandando la variable resultado para copmpletar el html


if __name__ == "__main__":
    app.run()