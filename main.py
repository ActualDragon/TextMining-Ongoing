import codecs #implementar una clase para codificar y decodificar archivos y provee acceso para administrar errores en el proceso de busqueda
import collections #alternativa para contenedores como contenedores como dictados, listas, tuplas y conjuntos.
 
import numpy as np
import pandas as pd #manipulacion y analisis de datos
import nltk #libreria usada para procesamiento de lenguaje natural
from nltk.tokenize import WordPunctTokenizer #nos permite separar el texto en tokens
import matplotlib
from nltk.stem import PorterStemmer #stem es un sub-paquete de nltk que elimina los afijos morfológicos (producto extra) para una cadena o contenidos
                                    #el algoritmo porter stemmer hace el stemming
import aspose.words as aw #nos permmite leer archivos .doc

#Variables globales
f = []

# Cargar el archivo a leer
doc = aw.Document(r"C:/Users/danyg/Documents/Internado/TextMining/Pacientes/PACIENTE-2.doc")

# Leer el contenido de los parrafos tipo nodo
for paragraph in doc.get_child_nodes(aw.NodeType.PARAGRAPH, True) :    
    paragraph = paragraph.as_paragraph()
    f.append(paragraph.to_string(aw.SaveFormat.TEXT))

print(len(f))
print(f[3:5])





#name = r'C:/Users/danyg/Documents/Internado/TextMining/Pacientes/PACIENTE-2.doc'
#out = pypandoc.convert_file(name, 'plain', outputfile=r"C:/Users/danyg/Documents/Internado/TextMining/Pacientes/PACIENTE-2.txt")
#assert out == ""
#text = txt.process(r"C:/Users/danyg/Documents/Internado/TextMining/Pacientes/PACIENTE-2.DOC", encoding="UTF-8")
#text = text.decode("utf8")
#text = textract.process("C:/Users/danyg/Documents/Internado/TextMining/Pacientes/PACIENTE-2.DOC", encoding = 'unicode_escape')
