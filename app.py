from importlib import import_module
import os
from flask import Flask, render_template, url_for, request, \
    flash, current_app, make_response, Response, jsonify, \
    copy_current_request_context, session, redirect
    
from passlib.hash import sha256_crypt
import csv
import pandas as pd

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

#Flask server configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

filename = 'auth.csv'


camera = Camera()  

def password_hash(pass_):
    return sha256_crypt.encrypt(pass_)  
  
def auth_write(name, email, passcode):
    filesize = os.path.getsize('auth.csv')
    if filesize == 0:
        header = ("Email", "Name", "Password")  
        with open (filename, "w", newline = "") as csvfile:
            filer = csv.writer(csvfile)
            filer.writerow(header)       
    with open(filename, 'a') as f:
        password = password_hash(passcode)
        f.writelines(f'\n{email}, {name}, {password}')
            

def password_verify(password_):
    col_list = ["Password"]
    df = pd.read_csv(filename, usecols = col_list)   
    password_search = df["Password"]
    for password in password_search: 
        verify = sha256_crypt.verify(password_, str(password).strip())
        if(verify):
            return verify
        
                     
#Catch all route not defined
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):    
     return render_template('index.html')


#Home/Landing Page Route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        if request.form['submit'] == 'Login':
            email_ = request.form['email']
            password_ = request.form['password']
            password  = password_verify(password_) 
            
            if(password):
                url = 'cv.html'
                return render_template(url)  
            else:
                return render_template('index.html') 
                 
        elif request.form['submit'] == 'create':
            name = request.form['Name']
            email = request.form['email']
            password = request.form['password']   
            auth_write(name, email, password)
    return render_template('index.html')



def gen(camera):
    """Video streaming generator function."""
    while True: 
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
       
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
    
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
