import os
import uuid
import flask
import urllib
import tensorflow
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.preprocessing.image import load_img , img_to_array
import numpy as np
from get_image2 import ambil_foto
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL


app = Flask(__name__)
# Mysql Connection
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Irul12345'
# app.config['MYSQL_DB'] = 'tes'
# mysql = MySQL(app)

# settings
# app.secret_key = "mysecretkey"

# cur = mysql.connect().cursor()
# cur.execute('SELECT * FROM contacts')
# data = cur.fetchall()
# cur.close()

# cursor.execute("SELECT * from user")
# data = cursor.fetchone()
# print(data)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'model4-86.hdf5'))


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

classes = ['ANIMAL','FASHION&BEAUTY','FOOD','OTOMOTIF','TRAVELING']


def predict(filename , model):
    
    img = tensorflow.keras.utils.load_img( filename,target_size = (150,150))
    x = tensorflow.keras.utils.img_to_array(img)
    x = np.expand_dims(x,axis = 0)
    images = np.vstack([x])
    classes = model.predict(images, batch_size = 150)
    
    food = 'FOOD'
    traveling = 'TRAVELING'
    otomotif = 'OTOMOTIF'
    animal = 'ANIMAL'
    fashion = 'FASHION&BEAUTY'
    if classes [0][0] == 1:
      klasifikasi_animal = animal
      return (klasifikasi_animal)
    elif classes [0][1] == 1:
      klasifikasi_fashion = fashion
      return (klasifikasi_fashion) 
    elif classes [0][2] == 1:
      klasifikasi_food = food
      return (klasifikasi_food) 
     
    elif  classes [0][3] == 1:
      klasifikasi_traveling = traveling
      return (klasifikasi_traveling) 

    elif  classes [0][4] == 1:
      klasifikasi_otomotif = otomotif
      return (klasifikasi_otomotif) 
    else:
      return ('NO DETECT')




@app.route('/')
def home():
        return render_template("index.html")

@app.route('/success' , methods = ['GET' , 'POST'])
def success():
  data = []
  username = request.form.get('username')
  ambil_foto(username)
  pathnya = 'static/' + username
  if len(os.listdir(pathnya)) == 0:
    return render_template('index.html', error = 'Username tidak ditemukan')
  else:
    for i in range(len(os.listdir(pathnya))):
      img_path = os.path.join( pathnya , os.listdir(pathnya)[i])
      class_result = predict(img_path , model)
      print(class_result)
      data.append({
        'img' :  img_path,
        'class' : class_result,
        'username' : username
      })
  return render_template('success.html', data = data)

if __name__ == "__main__":
    app.run(debug = True)


