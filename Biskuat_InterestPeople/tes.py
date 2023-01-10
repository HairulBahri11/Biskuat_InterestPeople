from code import interact
from inspect import Parameter
import os
import uuid
import flask
import urllib
import tensorflow
import os
from fastai.vision.all import *
from fastai.vision import *
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, send_file
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from scrab_instagram import ambil_foto
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import redirect, render_template, request, redirect, url_for, session, flash
import re
import secrets
import random
import pathlib

app = Flask(__name__)

secret = secrets.token_urlsafe(32)

app.secret_key = secret
app.config[' MYSQL HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biskuat_interest'
mysql = MySQL(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = Path('model1.hdf5')
# model = load_learner(os.path.join(BASE_DIR, 'model1.hdf5'))
# model = load_learner('model1.hdf5')


ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT


classes = ['FASHION&BEAUTY', 'FOOD', 'OTOMOTIF', 'TRAVELING']


# def predicts(model, image):
#     return model.predict(
#         image
#     )[0]

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

path = Path(os.getcwd())
full_path = os.path.join(path, 'model.pkl')
learner = load_learner(full_path)

print(learner.predict(
    'v.syilla1.jpeg'
)[0])

# def predict(filename, model):

#     img = tensorflow.keras.utils.load_img(filename, target_size=(150, 150))
#     # image = cv2.imread(img)
#     x = tensorflow.keras.utils.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     images = np.vstack([x])
#     classes = model.predict(images, batch_size=10)

#     food = 'FOOD'
#     traveling = 'TRAVELING'
#     otomotif = 'OTOMOTIF'
#     # animal = 'ANIMAL'
#     fashion = 'FASHION&BEAUTY'
#     # if classes[0][0] == 1:
#     #     klasifikasi_animal = animal
#     #     return (klasifikasi_animal)
#     if classes[0][0] == 1:
#         klasifikasi_fashion = fashion
#         return (klasifikasi_fashion)
#     elif classes[0][1] == 1:
#         klasifikasi_food = food
#         return (klasifikasi_food)

#     elif classes[0][3] == 1:
#         klasifikasi_traveling = traveling
#         return (klasifikasi_traveling)

#     elif classes[0][2] == 1:
#         klasifikasi_otomotif = otomotif
#         return (klasifikasi_otomotif)
#     else:
#         return ('NO DETECT')


# @app.route('/')
# def home():
#     return render_template("index.html")


# @app.route('/login')
# def login():
#     return render_template("login.html")


# @app.route('/widget')
# def widget():
#     return redirect('/')


# @app.route('/register')
# def register():
#     return render_template("register.html")


# @app.route('/login_proses', methods=['GET', 'POST'])
# def login_proses():
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute(
#             'SELECT * FROM user WHERE username = %s AND password = %s', (username, password, ))
#         account = cursor.fetchone()
#         if account:
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['name'] = account['name']
#             session['username'] = account['username']
#             session['email'] = account['email']
#             msg = 'Logged in successfully !'
#             return redirect('/')
#         else:
#             msg = 'Incorrect username / password !'
#     return render_template('register.html', msg=msg)


# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('name', None)
#     session.pop('username', None)
#     session.pop('email', None)
#     return redirect(url_for('login'))


# @app.route('/register_proses', methods=['GET', 'POST'])
# def register_proses():
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         name = request.form['name']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute(
#             'SELECT * FROM user WHERE username = %s', (username, ))
#         account = cursor.fetchone()
#         if account:
#             msg = 'Account already exists !'
#             return render_template('register.html', msg=msg)
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address !'
#             return render_template('register.html', msg=msg)
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers !'
#             return render_template('register.html', msg=msg)
#         elif not username or not password or not email:
#             msg = 'Please fill out the form !'
#             return render_template('register.html', msg=msg)
#         else:
#             cursor.execute(
#                 'INSERT INTO user VALUES (NULL, %s, %s, %s, %s)', (name, email, username, password,))
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#             return render_template('login.html', msg=msg)
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('register.html', msg=msg)


# @app.route('/dashboard')
# def dashboard():
#     data2 = session.get('id'),
#     instagram_id = session.get('instagram_id')
#     cur = mysql.connection.cursor()
#     parameter = (data2, instagram_id, )
#     cur.execute(
#         "SELECT lg.id_gambar as id, i.username as username, lg.gambar as gambar, lg.klasifikasi as klasifikasi  FROM load_gambar as lg INNER JOIN instagram as i ON lg.instagram_id = i.id  WHERE user_id = %s AND instagram_id =%s", parameter)
#     fetchdata = cur.fetchall()

#     cur.execute(
#         "SELECT COUNT(*) FROM load_gambar WHERE user_id = %s AND klasifikasi = 'FOOD' AND instagram_id =%s", parameter)
#     food = cur.fetchone()

#     cur.execute(
#         "SELECT COUNT(*) as total FROM load_gambar WHERE user_id = %s AND klasifikasi ='TRAVELING' AND instagram_id =%s", parameter)
#     traveling = cur.fetchone()

#     cur.execute(
#         "SELECT COUNT(*) FROM load_gambar WHERE user_id = %s AND klasifikasi ='OTOMOTIF' AND instagram_id =%s", parameter)
#     otomotif = cur.fetchone()

#     cur.execute(
#         "SELECT COUNT(*) as total FROM load_gambar WHERE user_id = %s AND klasifikasi ='FASHION&BEAUTY' AND instagram_id =%s", parameter)
#     fashion = cur.fetchone()

#     return render_template('success.html', data=fetchdata,  food=food,  otomotif=otomotif, traveling=traveling, fashion=fashion)
#     # else:
#     #     return redirect('login')


# @app.route('/success', methods=['GET', 'POST'])
# def success():
#     data = []
#     username = request.form.get('username')
#     id_user = request.form.get('id_user')
#     ambil_foto(username)
#     pathnya = 'static/' + username
#     if len(os.listdir(pathnya)) == 0:
#         return render_template('index.html', error='Username tidak ditemukan')
#     else:
#         number = random.randint(1000, 99999)
#         session['instagram_id'] = number
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO instagram VALUES (%s,%s)",
#                     (number, username))
#         mysql.connection.commit()

#         for i in range(len(os.listdir(pathnya))):
#             img_path = os.path.join(pathnya, os.listdir(pathnya)[i])

#             class_result = predict(img_path, model)
#             cur.execute("INSERT INTO load_gambar VALUES (%s,%s,%s,%s,%s)",
#                         ('', number, id_user, img_path, class_result))
#             mysql.connection.commit()

#             print(class_result)
#             data.append({
#                 'img':  img_path,
#                 'class': class_result,
#             })
#     cur.execute(
#         "SELECT COUNT(*) as total, klasifikasi FROM load_gambar WHERE user_id = %s AND instagram_id =%s GROUP BY klasifikasi ORDER BY total DESC limit 1", (id_user, number))
#     data = cur.fetchall()
#     for a in data:
#         interest = a[1]

#     flash(interest)
#     return redirect(url_for('dashboard'))
#     # else:
#     #     return redirect('login')


# if __name__ == "__main__":
#     app.run(debug=True)
