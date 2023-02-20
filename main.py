from flask import Flask, redirect, url_for, request, render_template, session, abort #Framework que permite crear aplicaciones web
from werkzeug.utils import secure_filename #validar el archivo -> "Never trust user input"
import os #usar funcionalidades dependientes del sistema operativo
import aspose.words as aw #Lectura de archivos
import webbrowser #Manejar el navegador
import filetype
import nltk #libreria usada para procesamiento de lenguaje natural
from nltk.corpus import wordnet as wn

#Validar que el archivo sea del tipo permitido (sin importar la extension que tenga)
def validate_file(file):
    header = file.read()
    file.seek(0)
    format = filetype.guess(header)
    if (format is None):
        return None
    format = format.extension
    if (format != "doc") and (format != "docx"):
        return None
    return '.' + format

#Leer la copia local del archivo que se subió
def Read_File(name):
    f = []
    text = []
    basedir = os.path.abspath(os.path.dirname(__file__)) #Obtener el directorio actual
    path = "".join([basedir,"\\static\\uploads\\", name]) #Obtener el directorio del archivo temporal
    doc = aw.Document(path) # Cargar el archivo a leer
    # Leer el contenido de los parrafos tipo nodo
    for paragraph in doc.get_child_nodes(aw.NodeType.PARAGRAPH, True) :    
        paragraph = paragraph.as_paragraph()
        p = paragraph.to_string(aw.SaveFormat.TEXT)
        p = p.replace("\\", "/").replace('"','\\"').replace("'","\'") #Escapar caracteres especiales
        p = p.replace('\n', '').replace('\r', '') #Eliminar saltos de linea y el retorno de carro
        f.append(p)
    #Eliminar la copia temporal del archivo
    if os.path.exists(path):
        os.remove(path)
    else:
        print("El archivo no existe")
    #Eliminar el texto adicional que agrega la libreria aspose.words
    size = len(f)
    for x in range(1,size-2):
        text.append(f[x])
    return text

#Encontrar la edad del paciente
def Edad(f):
    j = ""
    edad = []
    #De acuerdo con el analisis de la estructura de los expedientes, la edad siempre se encuentra antes del tag "ANTECEDENTES"
    for x in range(len(f)):
        i = f[x].find("ANTECEDENTES")
        if i != -1:
            j =  x #Encontrar el elemento de la lista donde empiezan los antecedentes (pues la edad va a estar antes)
    if j != "":
        for x in range(j):
            k = f[x].find("A\u00d1OS")
            if k != -1:
                k = f[x].find("MESES") #Validar su el paciente tiene menos de un año de edad
                if k != -1:
                    l =  x #Elemento de la lista que contiene la edad
                    edad = [int(i) for i in f[l].split() if i.isdigit()]
            else:
                edad.append(0)
    else:
        edad.append(0)
    return edad

# _.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.

# CONSTRUCTOR DE FLASH
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 #Limitar archivos a maximo 1MB
app.config['UPLOAD_PATH'] = r'./static/uploads' #Path al que se subira la copia temporal de los archivos a ser procesados
app.config['UPLOAD_EXTENSIONS'] = ['.doc', '.docx'] #Extensiones permitidas

#Generar la home page
@app.route('/')
def index():
    return render_template('index.html')
 
#Recibir el archivo subido
@app.route('/index', methods=['POST'])
def load():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename) #validar el nombre del archivo 
    if filename != '': #validar que si se subió un archivo
        file_ext = os.path.splitext(filename)[1]
        #agregar validación de si no hay archivo
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_file(uploaded_file):
            print("Error controlado")
            abort(400)
        basedir = os.path.abspath(os.path.dirname(__file__)) #Obtener el directorio actual
        uploaded_file.save(os.path.join(basedir,app.config['UPLOAD_PATH'], filename)) #Guardar una copia temporal del archivo subido
    return redirect(url_for('main', name=filename))

@app.route('/main/<name>')
def main(name):
    f = Read_File(name)
    age = Edad(f)[0]
    if age != 0:
        print("El paciente tiene:" ,age, "años")
        #Funcion que imprime la edad
    else:
        print("No tengo la edad")
        #Funcion que pide la edad
    return f
    
#Funcion main driver
if __name__ == '__main__':
    webbrowser.open_new("http://127.0.0.1:5000") #Abrir la pagina principal en el navegador cuando se corre la app
    app.run() #Correr la aplicación en el servidor local

#https://werkzeug.palletsprojects.com/en/2.1.x/serving/#shutting-down-the-server