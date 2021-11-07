from os import name
import dtos
from flask import Flask, json, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

users = []
images = []
videos = []

users.append(dtos.User("Guillermo Peitzner",
                 "M", "admin", "admin@ipc1", "admin@ipc1.com"))

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data["name"]
    gender = data["gender"]
    username = data["username"]
    password = data["password"]
    email = data["email"]
    for user in users:
        if user.email == email:
            return jsonify({"message": "email repeated"}), 400
    users.append(dtos.User(name,
                 gender, username, password, email))
    return jsonify(request.get_json()), 200


@app.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    for user in users:
        if user.email == email:
            if user.password == password:
                return jsonify({
                    "name" : user.name,
                    "gender" : user.gender,
                    "username" : user.username,
                    "email" : user.email
                }), 200
            else:
                return jsonify({
                    "message" : "bad credentials"
                }), 400
    return jsonify({
        "message": "user not found"
    }), 400    

@app.route("/modify", methods = ["PUT"])
def modify():
    data = request.get_json()
    username = data["username"]
    for user in users:
        if user.username == username:
            return jsonify({
                "error": "arg invalid"
            }),400
        else:
            user.username = data["username"] 
            user.name = data["name"]   
            user.password = data["password"]
            user.email = data["email"]
            return jsonify({
                "name" : user.name,
                "gender" : user.gender,
                "username" : user.username,
                "email" : user.email
            }), 200 
            
@app.route("/new_post", methods = ["POST"])
def new_post():
    data = request.get_json()
    url = data["url"]
    tipo = data["tipo"]
    category = data["category"]
    date = time.strftime("%d/%m/%y")
    if tipo == "I":
        for imagen in images:
            if imagen.url == url:
                 return jsonify({
                "message": "arg invalid"
            }),400
           
        else:
            images.append(dtos.Image(url,date,category))
            print(images)
            return jsonify({
                "accion":" imagen created"
                }), 200
    if tipo == "V" :
        for video in videos:
           
            if video.url == url:
                return jsonify({
                "message": "arg invalid"
                }),400
        else:

            videos.append(dtos.Video(url,date,category))
            return jsonify({
                "accion":"video add"
            }), 200                

    
@app.route("/cargaI", methods = ["GET"])
def cargaI():
    if request.method == "GET":
        tmp = []
        for imagen in images:
            tmp.append({"url": imagen.url, "date": imagen.date, "category" : imagen.category})
        return jsonify(tmp),200    
  
@app.route("/cargaV", methods = ["GET"])
def cargaV():
    if request.method == "GET":
        tmp = []
        for video in videos:
            tmp.append({"url": video.url, "date": video.date, "category" : video.category})    
        return jsonify(tmp),200


                    