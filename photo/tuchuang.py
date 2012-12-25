from flask import Flask, request, render_template, make_response, json
from bae.core import const
from bae.api import bcs
import os
import random

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

BUCKET_NAME = 'photobucket'
HOST = const.BCS_ADDR
AK = const.ACCESS_KEY
SK = const.SECRET_KEY

app = Flask(__name__)

@app.route("/photo/")
def index():
    resp = make_response(render_template("index.html"))
    return resp

@app.route('/photo/upload', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        photo = request.files["uploaded_file"]
        if photo is None:
            return json.dumps({'code' : 403, 'message' : 'FILE IS EMPTY', 'data' : 'null'})
        else:
            if photo and allowed_file(photo.filename):
                filename_random = random_string()
                file_extension = photo.filename.rsplit('.', 1)[1]
                filename = '%s.%s' % (filename_random, file_extension)
                filedata = photo.read()
                filepath = UPLOAD_FOLDER + filename

                # bae bcs
                bbcs = bcs.BaeBCS(HOST, AK, SK)
                bbcs.put_object(BUCKET_NAME, str(filepath), filedata)
                # bae bcs

                return json.dumps({'code' : 0, 'message' : 'OK', 'data' : 'http://%s/%s%s' % (HOST, BUCKET_NAME, filepath)})
            else:
                return json.dumps({'code' : 1, 'message' : 'NOT FILE TYPE.', 'data' : 'null'})
    else:
        return ''

def random_string():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app, stdout="log", stderr="log")