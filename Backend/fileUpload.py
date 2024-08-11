import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename
#import urllib.request as urllib2
from requests_toolbelt.multipart.encoder import MultipartEncoder
import datetime
from flask import send_file
from Thesis_Final import *;
import os
#import readFile,extractFile,writeExcel,writeCSV from Thesis_Final;



app = Flask(__name__)
cors = CORS(app)

UPLOAD_FOLDER = 'D:\\Thesis\\Project\\Backend';
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'STP','stp','STEP','step'}



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploading', methods=['GET'])
def uploading():
    print(f.filename)
    return jsonify({"name": filename, "status": "success"})



@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files.getlist('files')
        filename = ""
        print(request.files, "....")
        for f in file:
            if f and allowed_file(f.filename):
               print(f.filename)
               filename = secure_filename(f.filename)
               try:
                   f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename));
                   obj=Thesis()
                   obj.readFile(app.config['UPLOAD_FOLDER']+'\\'+filename)
                   obj.extractFile()
                   obj.writeExcel(app.config['UPLOAD_FOLDER']+'\\'+filename[0:filename.index('.')]);
                   obj.writeCSV(app.config['UPLOAD_FOLDER']+'\\'+filename[0:filename.index('.')]);
                   return jsonify({"name": filename, "status": "success"}) 
               except Exception as e:
                   return jsonify({"status":str(e)}) 
            else:
                 return jsonify({"status": "only STEP or STP file extension allowed"})   
    else:
         return jsonify({"status": "Upload API GET Request Running"})   
    
@app.route('/cleaned/<filename>', methods=['GET'])
def cleaned(filename):
    try:
        
      #  for key in my_dict.keys():
      #  print("filename::"+request.json["filename"]);
      #  print(str(data));
        obj=Thesis()
      #  obj.cleanData(app.config['UPLOAD_FOLDER']+'\\'+request.json["filename"].strip());
        obj.cleanData(app.config['UPLOAD_FOLDER']+'\\'+filename)
        return jsonify({"status": "success"})        
    except Exception as e:
        return jsonify({"status":str(e)})       
               

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
 #   obj=Thesis()
 #   obj.cleanData(app.config['UPLOAD_FOLDER']+'\\'+filename.strip());
    path = app.config['UPLOAD_FOLDER']+'\\'+filename+".csv"
    return send_file(path, as_attachment=True)
        
        
@app.route('/describe/<filename>', methods=['GET'])
def describe(filename):        
    obj=Thesis()
    return obj.describe_data(filename);
    
    
@app.route('/charts/<filename>', methods=['GET'])
def charts(filename):        
    timg=Thesis()
    
    try:
        timg.create_charts_1(filename);  
        return jsonify({"status":"success"}) 
    except Exception as e:
        return jsonify({"status":str(e)}) 
    timg.mainloop();



@app.route('/getproperties/<filename>', methods=['GET'])
def getproperties(filename):        
    timg=Thesis()
    
    try:
        if(os.path.exists(app.config['UPLOAD_FOLDER']+"\\"+filename+".STEP")):
            return jsonify(timg.step_properties(app.config['UPLOAD_FOLDER']+'\\'+filename+".STEP"));
        elif(os.path.exists(app.config['UPLOAD_FOLDER']+"\\"+filename+".STP")): 
            return jsonify(timg.step_properties(app.config['UPLOAD_FOLDER']+'\\'+filename+".STP"));
        elif(os.path.exists(app.config['UPLOAD_FOLDER']+"\\"+filename+".stp")): 
            return jsonify(timg.step_properties(app.config['UPLOAD_FOLDER']+'\\'+filename+".stp"));
        elif(os.path.exists(app.config['UPLOAD_FOLDER']+"\\"+filename+".step")): 
            return jsonify(timg.step_properties(app.config['UPLOAD_FOLDER']+'\\'+filename+".step"));
        else:
            return jsonify({"status":"File not found"}) 
       # return jsonify({"status":"success"}) 
    except Exception as e:
        return jsonify({"status":str(e)}) 
   # timg.mainloop();


@app.route('/send_email', methods=['POST'])
def send_email():
    obj=Thesis()
    sender_email=request.json["sender"];
    sender_subject=request.json["subject"];
    sender_body=request.json["body"];
    if(obj.send_email(sender_email,sender_subject,sender_body)=='success'):
        return jsonify({"status":"success"}) 
    else:
        return jsonify({"status":"falied to send"}) 
    
    
@app.route('/insert_user', methods=['POST'])
def insert_user():  
    user = json.loads(request.data) 
    obj=Thesis();

    if(obj.insert_user(user)=='success'):
        return jsonify({"status":"success"}) 
    else:
        return jsonify({"status":obj.insert_user(user)}) 
        
        
@app.route('/login_user', methods=['POST'])
def login_user():  
    user = json.loads(request.data) 
    obj=Thesis();

    if(obj.login_user(user)=='success'):
        return jsonify({"status":"success"}) 
    else:
        return jsonify({"status":obj.login_user(user)})         
if __name__ == '__main__':
    app.run()  # run our Flask app   