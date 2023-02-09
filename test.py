from flask import Flask, redirect, url_for, request, render_template, session, abort #Framework que permite crear aplicaciones web
from werkzeug.utils import secure_filename #validar el archivo -> "Never trust user input"
import os #usar funcionalidades dependientes del sistema operativo
import aspose.words as aw #Lectura de archivos
import webbrowser #Manejar el navegador
import filetype

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
    basedir = os.path.abspath(os.path.dirname(__file__)) #Obtener el directorio actual
    path = "".join([basedir,"\\static\\uploads\\", name]) #Obtener el directorio del archivo temporal
    doc = aw.Document(path) # Cargar el archivo a leer
    # Leer el contenido de los parrafos tipo nodo
    for paragraph in doc.get_child_nodes(aw.NodeType.PARAGRAPH, True) :    
        paragraph = paragraph.as_paragraph()
        f.append(paragraph.to_string(aw.SaveFormat.TEXT))

    escaped = f.encode('unicode-escape').replace("'", "\\'") #reemplazar caracteres especiales
    #print(len(f))
    return escaped

# _.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.

# CONSTRUCTOR DE FLASH
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 #Limitar archivos a maximo 1MB
app.config['UPLOAD_PATH'] = r'./static/uploads' #Path al que se subira la copia temporal de los archivos a ser procesados
app.config['UPLOAD_EXTENSIONS'] = ['.doc', '.docx', '.txt'] #Extensiones permitidas

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
    return f
    
#Funcion main driver
if __name__ == '__main__':
    webbrowser.open_new("http://127.0.0.1:5000") #Abrir la pagina principal en el navegador cuando se corre la app
    app.run() #Correr la aplicación en el servidor local

#hacer una función ligada a JS que detecte cuando se cierre la ventana
# JS -> window.unonload
# https://werkzeug.palletsprojects.com/en/2.1.x/serving/#shutting-down-the-server
# import os
# os.system("comando de la terminal")
#os.kill
# os.kill(CTRL_C_EVENT)