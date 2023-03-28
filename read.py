import spacy
nlp = spacy.load('es_core_news_sm') #Cargar el modelo en español de spaCy
"""
text = "Estaré disponible durante las próximas dos años."
doc = nlp(text) #Procesar el texto con spaCy

# Extraer todas las palabras relacionadas con tiempo que sean sustantivos o adjetivos
tiempos = [f"{doc[i-1].text} {token.text}" for i, token in enumerate(doc) if token.pos_ in ['NOUN', 'ADJ'] and ('día' in token.text or 'semana' in token.text or 'mes' in token.text or 'año' in token.text or 'años' in token.text)]

print(tiempos)
"""
class Search:
    Term = 0
    Line = -1
    Time = [0]

def Find_Syn(terms,f):
    IAM = Search()
    for i in range(len(terms)): #Ir recorriendo la lista de términos para buscar coincidencias en el texto
        for j in range(len(f)):
            k = f[j].find(terms[i])
            if k != -1: #Si encuentra coincidencias, agregarla al objeto
                IAM.Term = f[j] #El término encontrado en el texto
                IAM.Line = j #Qué número de oración es
    return IAM

def Find_Time(f,x):
    text = f[x.Line]
    doc = nlp(text) #Procesar el texto con spaCy
    # Extraer todas las palabras relacionadas con tiempo que sean sustantivos o adjetivos
    tiempos = [f"{doc[i-1].text} {token.text}" for i, token in enumerate(doc) if token.pos_ in ['NOUN', 'ADJ'] and ('día' in token.text or 'semana' in token.text or 'mes' in token.text or 'año' in token.text or 'años' in token.text)]
    if tiempos != []:
        del x.Time[0]
        x.Time.append(tiempos)
        return tiempos[0]
    return 0

f = ["hola como estas", "infarto agudo hace 6 meses"]
terms =["infarto agudo de miocardio", "im", "ima", "iam", "infarto", "infarto cardiaco", "infarto agudo", "ataque cardiaco", "ataque al corazón", "infarto de miocardio", "infarto miocárdico", "síndrome isquémico coronario agudo", "sica", "infarto agudo al miocardio con elevación del segmento st", "infarto agudo al miocardio sin elevación del segmento st"]
text = Find_Syn(terms,f)
time = Find_Time(f,text)
print(time)
if time != 0:
    i = time.split()
    match i[1]:
        case "meses":
            if int(i[0]) <=6:
                print("Hace menos de 6 meses")
        case "semanas":
            if int(i[0]) <=24:
                print("Hace menos de 6 meses")
        case "dias":
            if int(i[0]) <=183:
                print("Hace menos de 6 meses")
        case _:
            print("El paciente no tuvo el infarto hace menos de 6 meses")