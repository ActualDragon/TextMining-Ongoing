import codecs #implementar una clase para codificar y decodificar archivos y provee acceso para administrar errores en el proceso de busqueda
import collections #alternativa para contenedores como contenedores como dictados, listas, tuplas y conjuntos.
 
import numpy as np
import pandas as pd
import nltk #libreria usada para procesamiento de lenguaje natural
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
import matplotlib

f = open("C:/Users/danyg/Documents/Internado/Pacientes/PACIENTE_1.txt","r", encoding='utf-8-sig') #abrir el archivo del paciente
lines = len(f.readlines()) #encontrar el numero de líneas en el documento
f.seek(0) #volver al inicio del archivo
text = f.readlines() #leer el contenido del archivo
print(text[2:30]) #imprimir ciertas lineas del archivo
print(lines)
f.close() #cerrar el archivo