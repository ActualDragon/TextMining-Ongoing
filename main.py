import codecs #implementar una clase para codificar y decodificar archivos y provee acceso para administrar errores en el proceso de busqueda
import collections #alternativa para contenedores como contenedores como dictados, listas, tuplas y conjuntos.
 
import numpy as np
import pandas as pd #manipulacion y analisis de datos
import nltk #libreria usada para procesamiento de lenguaje natural
from nltk.tokenize import WordPunctTokenizer #nos permite separar el texto en tokens
import matplotlib
from nltk.stem import PorterStemmer #stem es un sub-paquete de nltk que elimina los afijos morfológicos (producto extra) para una cadena o contenidos
                                    #el algoritmo porter stemmer hace el stemming

f = open("C:/Users/danyg/Documents/Internado/Pacientes/PACIENTE_1.txt","r", encoding='utf-8-sig') #abrir el archivo del paciente
lines = len(f.readlines()) #encontrar el numero de líneas en el documento
f.seek(0) #volver al inicio del archivo
text = f.readlines() #leer el contenido del archivo
print(text[2:30]) #imprimir ciertas lineas del archivo
print(lines)
f.close() #cerrar el archivo