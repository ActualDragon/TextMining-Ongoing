from flask import Flask, redirect, url_for, request, render_template, session, abort #Framework que permite crear aplicaciones web
from werkzeug.utils import secure_filename #validar el archivo -> "Never trust user input"
import os #usar funcionalidades dependientes del sistema operativo
import aspose.words as aw #Lectura de archivos
import webbrowser #Manejar el navegador
import filetype
import nltk #libreria usada para procesamiento de lenguaje natural
from nltk.corpus import wordnet as wn

#CLASES
class Goldman_Index:
    def edad(self, edad, edad_p): #Edad > 70
        self.edad = edad #Valor encontrado
        self.edad_p = edad_p #Puntaje asignado segun el indice

    def IAM(self, IAM, IAM_p): #Infarto agudo de miocardio
        self.IAM = IAM
        self.IAM_p = IAM_p
    
    def JVD(self, JVD, JVD_p): #Distención de la vena yugular o ruido cardiaco en S3
        self.JVD = JVD
        self.JVD_p = JVD_p

    def EA(self, EA, EA_p): #Estenosis aórtica
        self.EA = EA
        self.EA_p = EA_p

    def ECG(self, ECG, ECG_p): #Ritmo distinto al sinusal o CAP (contracciones auriculares prematuras) en su último ECG
        self.ECG = ECG
        self.ECG_p = ECG_p

    def CVP(self, CVP, CVP_p): #5 contracciones ventriculares prematuras / min documentadas en cualquier momento
        self.CVP = CVP
        self.CVP_p = CVP_p

    #PO2 (presión parcial de oxígeno) < 60 o PCO2 (presión parcial de dióxido de carbono) > 50 mm Hg, K (potasio) < 3.0 o HCO3 (bicarbonato) < 20 meq/litro,
    #BUN (nitrógeno ureico en sangre) > 50 o Cr (creatinina) > 3.0 mg/dl, SGOT (transaminasa glutámico-oxalacética) abnormal, 
    #señales de enfermedad hepática crónica o paciente postrado por causas no-cardíacas
    def estado(self, estado, estado_p): 
        self.estado = estado
        self.estado_p = estado_p

    def OR(self, OR, OR_p): #Cirugia intraperitoneal, intratorácica o aórtica
        self.OR = OR
        self.OR_p = OR_p

    def ER(self, ER, ER_p): #Cirugía de emergencia
        self.ER = ER
        self.ER_p = ER_p
    
    def __str__(self): 
        return "Edad: %s \n" \
               "Puntaje edad: %i \n" % (self.edad, self.edad_p)

class Puntaje_Lee:
    def OR(self, OR, OR_p): #Cirugia de alto riesgo (intraperitoneal, intratorácica o suprainguinal vascular)
        self.OR = OR #Valor encontrado
        self.OR_p = OR_p #Puntaje asignado segun el indice

    def isq(self, isq, isq_p): #Historial de enfermedad cardíaca isquémica
        self.isq = isq
        self.isq_p = isq_p
    
    def cong(self, cong, cong_p): #Historial de enfermedad cardíaca congestiva
        self.cong = cong
        self.cong_p = cong_p

    def CV(self, CV, CV_p): #Historial de enfermedaad cerebrovascular
        self.CV = CV
        self.CV_p = CV_p

    def diab(self, diab, diab_p): #Terapia de insulina para diabéticos
        self.diab = diab
        self.diab_p = diab_p

    def Cr(self, Cr, Cr_p): #Creatinina preoperatoria > a 2 mg/dL (o > 177 micromol/L)
        self.Cr = Cr
        self.Cr_p = Cr_p

class Detsky_Index:
    def IAM_new(self, IAM_new, IAM_new_p): #Infarto agudo de miocardio < 6 meses
        self.IAM_new = IAM_new #Valor encontrado
        self.IAM_new_p = IAM_new_p #Puntaje asignado segun el indice

    def IAM_old(self, IAM_old, IAM_old_p): #Infarto agudo de miocardio > 6 meses
        self.IAM_old = IAM_old
        self.IAM_old_p = IAM_old_p
    
    def ang_III(self, ang_III, ang_III_p): #Angina de pecho según la Sociedad Cardiovascular Canadiense -> Clase III
        self.ang_III = ang_III
        self.ang_III_p = ang_III_p

    def ang_IV(self, ang_IV, ang_IV_p): #Angina de pecho según la Sociedad Cardiovascular Canadiense -> Clase IV
        self.ang_IV = ang_IV
        self.ang_IV_p = ang_IV_p

    def angina(self, angina, angina_p): #Angina inestable < 3 meses
        self.angina = angina
        self.angina_p = angina_p 

    def edema_new(self, edema_new, edema_new_p): #Edema pulmonar < 1 semana
        self.edema_new = edema_new
        self.edema_new_p = edema_new_p

    def edema_old(self, edema_old, edema_old_p): #Edema pulmonar en cualquier otro momento
        self.edema_old = edema_old
        self.edema_old_p = edema_old_p

    def EA(self, EA, EA_p): #Estenosis aórtica crítica
        self.EA = EA
        self.EA_p = EA_p
    
    def ECG(self, ECG, ECG_p): #Ritmo distinto al sinusal o extrasístoles auriculares
        self.ECG = ECG
        self.ECG_p = ECG_p

    def CAP(self, CAP, CAP_p): # >5 CAP (contracciones auriculares prematuras) / min documentados en cualquier momento
        self.CAP = CAP
        self.CAP_p = CAP_p

    #PO2 (presión parcial de oxígeno) < 60 o PCO2 (presión parcial de dióxido de carbono) > 50 mm Hg, K (potasio) < 3.0 o HCO3 (bicarbonato) < 20 meq/litro,
    #BUN (nitrógeno ureico en sangre) > 50 o Cr (creatinina) > 3.0 mg/dl, SGOT (transaminasa glutámico-oxalacética) abnormal, 
    #señales de enfermedad hepática crónica o paciente postrado por causas no-cardíacas
    def estado(self, estado, estado_p): 
        self.estado = estado
        self.estado_p = estado_p

    def edad(self, edad, edad_p): #Edad > 70
        self.edad = edad 
        self.edad_p = edad_p 
    
    def ER(self, ER, ER_p): #Cirugía de emergencia
        self.ER = ER
        self.ER_p = ER_p

    def __str__(self): 
        return "Edad: %s \n" \
               "Puntaje edad: %i \n" % (self.edad, self.edad_p)

class Puntaje_Padua:
    def cancer(self, cancer, cancer_p): #Cancer activo -> metástasis y/o han pasado por quimioterapia o radioterapia en los últimos 6 meses
        self.cancer = cancer #Valor encontrado
        self.cancer_p = cancer_p #Puntaje asignado segun el indice

    def TEV(self, TEV, TEV_p): #Tromboembolismo venoso (excluyendo trombosis venosa superficial)
        self.TEV = TEV
        self.TEV_p = TEV_p
    
    def mov(self, mov, mov_p): #Movilidad reducida -> postrado con privilegios de baño (por incapacidad del paciente u órdenes del médico) por lo menos 3 días
        self.mov = mov
        self.mov_p = mov_p

    #Condición trombofília conocida (defectos de antitrombina, proteína C o S, factor V Leiden, mutación de protrombina G20210A, síndrome antifosfolípido)
    def trombo(self, trombo, trombo_p): 
        self.trombo = trombo
        self.trombo_p = trombo_p

    def OR(self, OR, OR_p): #Trauma reciente o cirugía <= 1 mes
        self.OR = OR
        self.OR_p = OR_p

    def edad(self, edad, edad_p): #Edad > 70
        self.edad = edad 
        self.edad_p = edad_p  

    def falla(self, falla, falla_p): #Falla cardíaca y/o respiratoria
        self.falla = falla
        self.falla_p = falla_p
    
    def IAM(self, IAM, IAM_p): #Desorden reumatológico agudo o infarto agudo de miocardio
        self.IAM = IAM
        self.IAM_p = IAM_p

    def BMI(self, BMI, BMI_p): #Obesidad (BMI >= 30)
        self.BMI = BMI
        self.BMI_p = BMI_p

    def TH(self, TH, TH_p): #Tratammiento hormonal actual
        self.TH = TH
        self.TH_p = TH_p

    def __str__(self): 
        return "Edad: %s \n" \
            "Puntaje edad: %i \n" % (self.edad, self.edad_p)

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
    return redirect(url_for('indices', name=filename))

@app.route('/indices/<name>')
def indices(name):
    Goldman = Goldman_Index()
    Lee = Puntaje_Lee()
    Detsky = Detsky_Index()
    Padua = Puntaje_Padua()
    f = Read_File(name) #Leer los contenidos del archivo
    age = Edad(f)[0]
    if age != 0: #Validar se que encontro la edad
        if age > 70:
            Goldman.edad(age,5) #Si el paciente tiene mas de 70 años se le agregan 5 puntos
            Detsky.edad(age,5)
            Padua.edad(age,1)
        else: 
            Goldman.edad(age,0) #Si el paciente tiene 70 años o menos no se le agregan puntos
            Detsky.edad(age,0)
            Padua.edad(age,0)
    else: 
        Goldman.edad(age,-1) #El -1 indica que es un dato faltante que se le debe pedir al usuario
        Detsky.edad(age,-1)
        Padua.edad(age,-1)
    return render_template('validar.html',Goldman=Goldman, Detsky=Detsky, Lee=Lee, Padua=Padua)
    
#Funcion main driver
if __name__ == '__main__':
    webbrowser.open_new("http://127.0.0.1:5000") #Abrir la pagina principal en el navegador cuando se corre la app
    app.run() #Correr la aplicación en el servidor local

#https://werkzeug.palletsprojects.com/en/2.1.x/serving/#shutting-down-the-server
