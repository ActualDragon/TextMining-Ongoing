import aspose.words as aw #Lectura de archivos
from nltk.corpus import wordnet as wn

f = []
s = []
text = []
doc = aw.Document("C:\\Users\\danyg\\Documents\\Internado\\prueba.doc") # Cargar el archivo a leer
    # Leer el contenido de los parrafos tipo nodo
for paragraph in doc.get_child_nodes(aw.NodeType.PARAGRAPH, True) :    
    paragraph = paragraph.as_paragraph()
    p = paragraph.to_string(aw.SaveFormat.TEXT)
    p = p.replace("\\", "/").replace('"','\\"').replace("'","\'") #Escapar caracteres especiales
    p = p.replace('\n', '').replace('\r', '') #Eliminar saltos de linea y el retorno de carro
    f.append(p)
size = len(f)
for x in range(1,size-2):
    s.append(f[x])
text = s[0].split(".") #Separar en oraciones

syn = wn.synonyms('INFARTO', lang='spa')
print("Synonym: ",syn,"\n")

syn = wn.lemmas('Infarto', lang='spa')
print("Lemmas: ",syn)
print("Lemmas type: ",type(syn[0]),"\n")

syn = wn.synsets("Infarto", lang='spa')
print("Synsets: ",syn)
eng = syn[0].name()
print("Synset name: ",eng)
print("Synset name type: ",type(eng))
eng = syn[0].lemma_names('spa')
print("Lemma names: ",eng,"\n")

print("Definition: ",syn[0].definition())