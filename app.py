import mysql.connector.errorcode
import requests  # Librería para poder acceder a una página
from bs4 import BeautifulSoup  # Librería para poder buscar en el HTML
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector


#app = Flask(__name__)
app = Flask(__name__, static_folder='static')
CORS(app)  # Esto habilitará CORS para todas las rutas

def formatear_tema(tema):
    tema = tema.strip().upper()
    return tema

def mostrar_texto(tema):

    url_Wikipedia = "https://es.wikipedia.org/wiki/"  # URL de Wikipedia sin tema

    respuesta = requests.get(url_Wikipedia + tema)  # Cargamos la página de Wikipedia con el tema

    if respuesta.status_code == 200:  # Si no es 200, no se encontró la página o hubo algún tipo de error

        soup = BeautifulSoup(respuesta.content, 'html.parser')  # El contenido que devuelve la página se formateo en HTML para poder analizarlo

        for elemento in soup.find_all(['sup']):  # Eliminamos los elementos que no queremos mostrar (citas) Busca todos los "sup"
            elemento.decompose()  #  Saca todos los "sup"

        tag_limitador = soup.find('meta', {'property': 'mw:PageProp/toc'})  # Buscamos el tag limitador de sección (<meta property="mw:PageProp/toc">) para que traiga solamente los primeros párrafos del artículo

        if tag_limitador is not None:  # Preguntamos si encontró el limitador (hay artículos que existen en Wikipedia pero tienen varias posibles opciones para ese término y no tienen el limitador)

            parrafos = tag_limitador.find_all_previous('p')  # Buscamos todos los párrafos que se encuentran antes del tag limitador (va buscando hacia arriba)

            parrafos = list(reversed(parrafos))   # Invertimos la lista de párrafos para mostrarlos en el orden correcto

            texto_para_mostrar = '\n'.join([p.get_text() for p in parrafos])  # Obtenemos el texto plano de los párrafos en una sola variable tipo string

            texto_para_mostrar = tema.title() + '\n\n' + texto_para_mostrar

            return texto_para_mostrar  # Devolvemos el texto
        else:
            return False
    else:
        return False  # Devolvemos falso si no se pudo localizar el texto
    
class Altapedia:

    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS temas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tema VARCHAR(255) NOT NULL,
            popularidad INT NOT NULL)''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def consultar_bd(self, tema):
        # Buscamos el tema en la tabla tema
        # formateamos tema de acuerdo a como hayamos decidido hacerlo (tema, Tema, TEMA)
        # tema = formatear_tema(tema)
        self.cursor.execute(f"SELECT * FROM temas WHERE tema = {tema}")
        return self.cursor.fetchone() #fetchone devuelve un sólo registro    

    def aumentar_popularidad(self, tema):
        sql = "UPDATE temas SET popularidad = popularidad + 1 WHERE tema = %s"
        valores = (tema)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def agregar_tema(self, tema): 
        sql = "INSERT INTO temas (tema, popularidad) VALUES (%s, %s)"
        valores = (tema, 1)
        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid

    def listar_popu(self):
        self.cursor.execute("SELECT * FROM temas ORDER BY popularidad LIMIT 10")
        productos = self.cursor.fetchall()
        return productos

    def listar_alfa(self):
        self.cursor.execute("SELECT * FROM temas ORDER BY tema")
        productos = self.cursor.fetchall()
        return productos

    def eliminar_tema(self, tema):
        self.cursor.execute(f"DELETE FROM temas WHERE tema = {tema}")
        self.conn.commit()
        return self.cursor.rowcount > 0


altapedia = Altapedia(host='localhost', user='root', password='root', database='miapp')


@app.route("/")  # La primera vez que se cargue la página la carga "normal"
def index():
     return render_template("prueba.html")


@app.route("/analizar", methods=["POST"])  # Acá es cuando se carga porque apretaron el botón en el formulario
def analizar_busqueda():
    busqueda = request.form["busqueda"]  # El nombre del input text lo guarda en la variable busqueda

    aux = mostrar_texto(busqueda)  # Busca el tema en Wikipedia y lo guarda en una variable aux
    if aux:  # Si no es false, lo encontró entonces en resultado guarda el texto
        resultado = aux 

        busqueda = formatear_tema(busqueda)  #  Formatea la cadena busqueda 

        if altapedia.consultar_bd(busqueda):  # Busca el tema en la base de datos, si lo encuentra aumenta la popularidad
            altapedia.aumentar_popularidad(busqueda)  # UPDATE
        else:
            altapedia.agregar_tema(busqueda)  # Si no lo encuentra, agrega el tema a la base de datos  CREATE

    else:  # Si es false, no lo encontró en Wikipedia entonces en resultado guarda el mensaje
        resultado = "Información no encontrada"    
    return render_template("prueba.html", resultado=resultado)  #  Recarga la página mandando la variable resultado para copmpletar el html


@app.route("/limpiar", methods=["POST"])
def limpiar_bd():
    contador = 0
    # leer archivo de palabras prohibidas a lista datos
    with open("datos.txt", "r") as archivo:
        lista_temas = [formatear_tema(linea) for linea in archivo.readlines()]
    # recorrer la lista preguntando si está en nuestra base de datos consultar_bd(dato)
    for tema in lista_temas:
        if altapedia.consultar_bd(tema):  # si está, eliminar_bd(dato)

            if altapedia.eliminar_tema(tema):  # DELETE
                #Si el tema se elimina correctamente contamos cuántos se eliminaron
                contador += 1   
            else:
                #Si ocurre un error durante la eliminación se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
                return jsonify({"mensaje": "Error al eliminar el término"}), 500

    if contador != 0:  # si se eliminó algún registro de la base de datos
        mensaje_eliminados = f"Se eliminaron {contador} términos"
        return jsonify({"mensaje": mensaje_eliminados}), 200   
    else:
        return jsonify({"mensaje": "No se eliminaron términos"}), 200


@app.route("/listaralfa", methods=["GET"])
def listar_alfa():
    #listar por orden alfabetico
    listado = altapedia.listar_alfa()
    return jsonify(listado)

@app.route("/listarpopu", methods=["GET"])
def listar_popu():
    #listar por orden popularidad
    listado = altapedia.listar_popu()
    return jsonify(listado)
    

if __name__ == "__main__":
    app.run()