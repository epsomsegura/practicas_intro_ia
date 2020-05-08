from flask import Flask
from flask import request
from pyDatalog import Logic
from lib.knowledgebase import knowledgebase as kbConnect
from lib.mongo_con import mongo_con as conexion

kbCon = kbConnect(conexion())

app = Flask(__name__)

class webserver:

    def __init__(self):
        app.run(host='0.0.0.0')

    @app.route('/patient/save',methods = ['POST'])
    def save():
        if request.method == 'POST':
            data = request.form
            rs = kbCon.assertPatient(data.get('name'),data.get('age'),data.get('sick'))
            return rs

    @app.route('/patient/read',methods = ['POST'])
    def read():
        if request.method == 'POST':
            data = request.form
            rs = kbCon.readPatient(data.get('name'))
            return rs

    @app.route('/patient/delete',methods = ['POST'])
    def delete():   
        if request.method == 'POST':
            data = request.form
            rs = kbCon.retractPatient(data.get('name'))
            return rs

    @app.route('/preferences/update',methods = ['GET'])
    def prefupdate():   
        rs = kbCon.retractpreferences()
        return rs

