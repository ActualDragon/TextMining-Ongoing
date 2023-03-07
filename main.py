from flask import Flask, redirect, url_for, request, render_template, session, abort #Framework que permite crear aplicaciones web
from werkzeug.utils import secure_filename #validar el archivo -> "Never trust user input"
import os #usar funcionalidades dependientes del sistema operativo
import aspose.words as aw #Lectura de archivos
import webbrowser #Manejar el navegador
import filetype
from nltk.corpus import wordnet as wn

#CLASES
class Goldman_Index:
    edad = 0 #Valor encontrado [Edad]
    edad_p = -1 #Puntaje asignado segun el indice

    IAM = 0 #Infarto agudo de miocardio
    IAM_p = -1

    JVD = 0 #Distención de la vena yugular o ruido cardiaco en S3
    JVD_p = -1

    EA = 0 #Estenosis aórtica
    EA_p = -1

    ECG = 0 #Ritmo distinto al sinusal o CAP (contracciones auriculares prematuras) en su último ECG
    ECG_p = -1

    CVP = 0 #5 contracciones ventriculares prematuras / min documentadas en cualquier momento
    CVP_p = -1

    #PO2 (presión parcial de oxígeno) < 60 o PCO2 (presión parcial de dióxido de carbono) > 50 mm Hg, K (potasio) < 3.0 o HCO3 (bicarbonato) < 20 meq/litro,
    #BUN (nitrógeno ureico en sangre) > 50 o Cr (creatinina) > 3.0 mg/dl, SGOT (transaminasa glutámico-oxalacética) abnormal,
    #señales de enfermedad hepática crónica o paciente postrado por causas no-cardíacas
    estado = 0
    estado_p = -1

    OR = 0 #Cirugia intraperitoneal, intratorácica, aórtica o de emergencia
    OR_p = -1

    is_empty = 0

class Puntaje_Lee:
    OR = 0  #Cirugia de alto riesgo (intraperitoneal, intratorácica o suprainguinal vascular) [Valor encontrado]
    OR_p = -1 #Puntaje asignado segun el indice

    isq = 0 #Historial de enfermedad cardíaca isquémica
    isq_p = -1

    cong = 0 #Historial de enfermedad cardíaca congestiva
    cong_p = -1

    CV = 0 #Historial de enfermedaad cerebrovascular
    CV_p = -1

    diab = 0 #Terapia de insulina para diabéticos
    diab_p = -1

    Cr = 0 #Creatinina preoperatoria > a 2 mg/dL (o > 177 micromol/L)
    Cr_p = -1

    is_empty = 0

class Detsky_Index:
    IAM = 0 #Valor encontrado Infarto agudo de miocardio < o > 6 meses
    IAM_p = -1 #Puntaje asignado segun el indice

    ang = 0 #Angina de pecho según la Sociedad Cardiovascular Canadiense -> Clase III o IV
    ang_p = -1

    angina = 0 #Angina inestable < 3 meses
    angina_p = -1

    edema = 0 #Edema pulmonar < 1 semana o cualquier otro momento
    edema_p = -1

    EA = 0 #Estenosis aórtica crítica
    EA_p = -1

    ECG = 0 #Ritmo distinto al sinusal o extrasístoles auriculares
    ECG_p = -1

    CAP = 0 # >5 CAP (contracciones auriculares prematuras) / min documentados en cualquier momento
    CAP_p = -1

    #PO2 (presión parcial de oxígeno) < 60 o PCO2 (presión parcial de dióxido de carbono) > 50 mm Hg, K (potasio) < 3.0 o HCO3 (bicarbonato) < 20 meq/litro,
    #BUN (nitrógeno ureico en sangre) > 50 o Cr (creatinina) > 3.0 mg/dl, SGOT (transaminasa glutámico-oxalacética) abnormal,
    #señales de enfermedad hepática crónica o paciente postrado por causas no-cardíacas
    estado = 0
    estado_p = -1

    edad = 0  #Edad > 70
    edad_p = -1

    ER = 0 #Cirugía de emergencia
    ER_p = -1

    is_empty = 0

class Puntaje_Padua:
    cancer = 0 #Valor encontrado Cancer activo -> metástasis y/o han pasado por quimioterapia o radioterapia en los últimos 6 meses
    cancer_p = -1 #Puntaje asignado segun el indice

    TEV = 0 #Tromboembolismo venoso (excluyendo trombosis venosa superficial)
    TEV_p = -1

    mov = 0 #Movilidad reducida -> postrado con privilegios de baño (por incapacidad del paciente u órdenes del médico) por lo menos 3 días
    mov_p = -1

    #Condición trombofília conocida (defectos de antitrombina, proteína C o S, factor V Leiden, mutación de protrombina G20210A, síndrome antifosfolípido)
    trombo = 0
    trombo_p = -1

    OR = 0 #Trauma reciente o cirugía <= 1 mes
    OR_p = -1

    edad = 0  #Edad > 70
    edad_p = -1

    falla = 0 #Falla cardíaca y/o respiratoria
    falla_p = -1

    IAM = 0 #Desorden reumatológico agudo o infarto agudo de miocardio
    IAM_p = -1

    BMI = 0 #Obesidad (BMI >= 30)
    BMI_p = -1

    TH = 0 #Tratammiento hormonal actual
    TH_p = -1

    is_empty = 0

# _.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.__.~"~._.~"~._.~"~._.~"~.
#FUNCIONES

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
        p = p.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U") #Eliminar acentos para facilitar procesamiento
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
def Find_Edad(f, Goldman, Detsky, Padua):
    j = ""; l = ""
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
                l =  x #Elemento de la lista que contiene la edad
                edad = [int(i) for i in f[l].split() if i.isdigit()]
    if l == "":
        edad.append(0)
    Goldman.edad = edad
    Detsky.edad = edad
    Padua.edad = edad

    if edad[0] != 0: #Validar se que encontro la edad
        if edad[0] > 70:
            Goldman.edad_p = 5 #Si el paciente tiene mas de 70 años se le agregan 5 puntos (1 en Padua)
            Detsky.edad_p = 5
            Padua.edad_p = 1
        else:
            Goldman.edad_p = 0 #Si el paciente tiene 70 años o menos no se le agregan puntos
            Detsky.edad_p = 0
            Padua.edad_p = 0
    return 0

#Determinar si ha habido infarto agudo de miocardio
def Find_IAM(f, Goldman, Detsky):
    #Agregar Padua
    terms = ["INFARTO AGUDO DE MIOCARDIO", "IM", "IMA", "IAM", "INFARTO", "INFARTO CARDIACO", "ATAQUE CARDIACO", "ATAQUE AL CORAZON", "INFARTO DE MIOCARDIO", "INFARTO MIOCARDICO"]
    list = ""
    IAM = [0]
    syn = wn.synonyms('INFARTO', lang='spa')
    if syn[0] != []:
        list = syn[0]
        for x in list:
            x = x.upper()
            x = x.replace("_", " ")
            terms.append(x)
    terms.append("IAM")
    for i in range(len(terms)):
        for j in range(len(f)):
            k = f[j].find(terms[i])
            if k != -1:
                IAM.append(f[j])
                Goldman.IAM = f[j]
                Detsky.IAM = f[j]
    if IAM[0] == 0:
        IAM.append(0)
    if IAM != 0:
        Goldman.IAM_p = 10
    return 0

#Determinar si hay algun criterio no encontrado
def FindEmpty(Goldman, Lee, Detsky, Padua):
    G_class = ["edad_p", "IAM_p", "JVD_p", "EA_p", "ECG_p", "CVP_p", "estado_p", "OR_p"]
    L_class = ["OR_p", "isq_p", "cong_p", "CV_p", "diab_p", "Cr_p"]
    D_class = ["IAM_p", "ang_p", "angina_p", "edema_p", "EA_p", "ECG_p", "CAP_p", "estado_p", "edad_p", "ER_p"]
    P_class = ["cancer_p", "TEV_p", "mov_p", "trombo_p", "OR_p", "edad_p", "falla_p", "IAM_p", "BMI_p", "TH_p"]
    n = 0

    #Validar si existe un atributo vacio
    for x in range(8):
        if getattr(Goldman,G_class[x]) == -1:
            n = n+1
            Goldman.is_empty = 1
    for x in range(6):
        if getattr(Lee,L_class[x]) == -1:
            n = n+1
            Lee.is_empty = 1
    for x in range(10):
        if getattr(Detsky,D_class[x]) == -1:
            n = n+1
            Detsky.is_empty = 1
    for x in range(10):
        if getattr(Padua,P_class[x]) == -1:
            n = n+1
            Padua.is_empty = 1
    if n != 0:
        return 1 #Algun campo se encuentra vacio
    else:
        return 0 #Ningun campo esta vacio
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
    return redirect(url_for('indices', name=filename))

@app.route('/indices/<name>')
def indices(name):
    Goldman = Goldman_Index()
    Lee = Puntaje_Lee()
    Detsky = Detsky_Index()
    Padua = Puntaje_Padua()
    f = Read_File(name) #Leer los contenidos del archivo
    Find_Edad(f,Goldman, Detsky, Padua)
    Find_IAM(f, Goldman, Detsky)
    empty = FindEmpty(Goldman, Lee, Detsky, Padua) #Determinar si hay atributos vacios
    if empty == 1:
        return render_template('validar.html',Goldman=Goldman, Detsky=Detsky, Lee=Lee, Padua=Padua) #Si hay atributos vacios, redirigir a un form que pide los datos faltantes
    else:
        return render_template('print.html',Goldman=Goldman, Detsky=Detsky, Lee=Lee, Padua=Padua) #Si no hay atributos vacios, redirigir a una pagina que imprime los resultados

#Funcion main driver
if __name__ == '__main__':
    webbrowser.open_new("http://127.0.0.1:5000") #Abrir la pagina principal en el navegador cuando se corre la app
    app.run() #Correr la aplicación en el servidor local

#https://werkzeug.palletsprojects.com/en/2.1.x/serving/#shutting-down-the-server
