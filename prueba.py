import requests  # Librería para poder acceder a una página
from bs4 import BeautifulSoup  # Librería para poder buscar en el HTML

url_Wikipedia = "https://es.wikipedia.org/wiki/"  # URL de Wikipedia sin tema
tema = "Edad_Media"
#tema = tema.replace(' ', '_')

response = requests.get(url_Wikipedia + tema)  # Cargamos la página de Wikipedia con el tema

soup = BeautifulSoup(response.content, 'html.parser')  # El contenido que devuelve la página se formateo en HTML para poder analizarlo

for element in soup.find_all(['sup']):  # Eliminamos los elementos que no queremos mostrar (citas) Busca todos los "sup"
    element.decompose()  #  Saca todos los "sup"

tag_limitador = soup.find('meta', {'property': 'mw:PageProp/toc'})  # Buscamos el tag limitador de sección (<meta property="mw:PageProp/toc">) para que traiga solamente los primeros párrafos del artículo

parrafos = tag_limitador.find_all_previous('p')  # Buscamos todos los párrafos que se encuentran antes del tag limitador (va buscando hacia arriba)

parrafos = list(reversed(parrafos))   # Invertimos la lista de párrafos para mostrarlos en el orden correcto

texto_para_mostrar = '\n'.join([p.get_text() for p in parrafos])  # Obtenemos el texto plano de los párrafos en una sola variable tipo string

print(texto_para_mostrar)
