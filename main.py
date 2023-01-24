import codecs #implementar una clase para codificar y decodificar archivos y provee acceso para administrar errores en el proceso de busqueda
import collections #alternativa para contenedores como contenedores como dictados, listas, tuplas y conjuntos.
 
import numpy as np
import pandas as pd #manipulacion y analisis de datos
import nltk #libreria usada para procesamiento de lenguaje natural
from nltk.tokenize import WordPunctTokenizer #nos permite separar el texto en tokens
import matplotlib
from nltk.stem import PorterStemmer #stem es un sub-paquete de nltk que elimina los afijos morfológicos (producto extra) para una cadena o contenidos
                                    #el algoritmo porter stemmer hace el stemming

with codecs.open("C:/Users/danyg/Documents/Internado/TextMining/Pacientes/PACIENTE-1.txt","r", encoding='utf-8') as f: 
    text = f.read()

#despues de que se implementa la funcion, regresa una lista de diccionarios, y el numero total de tokens
def total_tokens(text):
    n = WordPunctTokenizer().tokenize(text) #contar el numero total de tokens en el archivo
    return collections.Counter(n), len(n) #collection.counter nos permite almacenar cada token individual como llaves en un diccionario

#funcion que calcule la frecuencia absoluta y relativa de las palabras mas comunes en el archivo
def make_df(counter, size):
    #obtener frecuencias absoluta y relativa para cada token en la lista de counter
    abs_freq = np.array([el[1] for el in counter])
    rel_freq = abs_freq / size

    #crear un dataframe con la informacion obtenida
    df = pd.DataFrame(data=np.array([abs_freq, rel_freq]).T, index = [el[0] for el in counter], columns = ["Absolute frequency", "Relative frecuency"])
    df.index.name = "Most common words"
    return df

#aplicar las funciones al archivo
text_counter, text_size = total_tokens(text)
print(make_df(text_counter.most_common(10),text_size))

"""f = open("C:/Users/danyg/Documents/Internado/Pacientes/PACIENTE_1.txt","r", encoding='utf-8') #abrir el archivo del paciente
lines = len(f.readlines()) #encontrar el numero de líneas en el documento
f.seek(0) #volver al inicio del archivo
text = f.readlines() #leer el contenido del archivo
print(text[2:30]) #imprimir ciertas lineas del archivo
print(lines)
f.close() #cerrar el archivo """
