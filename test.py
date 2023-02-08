# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, request, render_template, session
from werkzeug.utils import secure_filename
import textract
import os
 
f = []
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'files'
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
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return "Exito"

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()

