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

"""
Importar librerias de python
En terminal de VS Code:  py -m pip install libreria
En terminal Python: import libreria
                    print(libreria.__file__)
"""
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