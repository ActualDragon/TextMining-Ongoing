# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, request, render_template, session
from werkzeug.utils import secure_filename
import os
import aspose.words as aw #nos permmite leer archivos .doc
 
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.config['UPLOAD_PATH'] = r'./static/uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.doc', '.docx', '.txt']

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/index', methods=['POST'])
def load():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        basedir = os.path.abspath(os.path.dirname(__file__))
        uploaded_file.save(os.path.join(basedir,app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('main', name=filename))

@app.route('/main/<name>')
def main(name):
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = "".join([basedir,"\\static\\uploads\\", name])
    print(path)
    #Variables globales
    f = []
    # Cargar el archivo a leer
    doc = aw.Document(path)
    # Leer el contenido de los parrafos tipo nodo
    for paragraph in doc.get_child_nodes(aw.NodeType.PARAGRAPH, True) :    
        paragraph = paragraph.as_paragraph()
        f.append(paragraph.to_string(aw.SaveFormat.TEXT))

    print(len(f))
    return "Exito" 
    

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()

