from flaskwebgui import FlaskUI #import FlaskUI class
import os

#You can also call the run function on FlaskUI class instantiation
try:
    FlaskUI(server='django').run()
except:
    print("exception")