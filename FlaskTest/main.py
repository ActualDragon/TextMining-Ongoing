from flask import Flask, render_template

#Import the library that converts the flask web app to a desktop app
from flaskwebgui import FlaskUI

app = Flask(__name__)

#Create a user interface of our desktop app. The "app" parameter is the one created in line 6
ui = FlaskUI(app=app, server="flask")

@app.route('/')
def index_page():
    return render_template('index.html')

if __name__ == '__main__':
    #app.run() This one gets commented
    #Run the web app as a desktop app
    ui.run()