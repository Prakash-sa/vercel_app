from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
import json
import os
from bson.json_util import dumps
# from flask_cors import CORS

api = Flask(__name__)
cors = CORS(api)

client = pymongo.MongoClient(
    "mongodb+srv://nextgen:OVh1edzm5KoDudsU@cluster0.btngql0.mongodb.net/test")
passworddb = client.credentials
projectdb = client.projects

passwords = passworddb.password
projects = projectdb.project


@api.route('/', methods=['GET'])
def index():
    return api.send_static_file('index.html')


@api.errorhandler(404)
def not_found(e):
    return


@api.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript"
    }
    return response_body


@api.route('/api/login/', methods=['POST'])
def log():
    print(request.json)
    if login(request.json['userid'], request.json['password']):
        return jsonify({"data": 200})
    return jsonify({"data": 208})


@api.route('/api/signup/', methods=['POST'])
def sign():
    print(request.json)
    myquery = {"userId": request.json['userid']}
    x = passwords.find_one(myquery)
    if (x == None):
        password_document = {
            "name": request.json['name'],
            "userId": request.json['userid'],
            "password": request.json['password']
        }
        passwords.insert_one(password_document)
        return jsonify({"data": "success"})
    return jsonify({"data": "failure"})


@api.route('/api/createproject/', methods=['POST'])
def createProject():
    print(request.json)
    users = []
    users.append(request.json['user'])
    projectDocument = {
        "ProjectName": request.json['projectName'],
        "hwset1": request.json['hwset1'],
        "hwset2": request.json['hwset2'],
        "users": users
    }
    projects.insert_one(projectDocument)
    return jsonify({"data": "success"})


@api.route('/api/getProjects/', methods=['POST', 'GET'])
def getProjects():
    data = list(projects.find())
    return json.loads(dumps(data))


@api.route('/api/checkin/<projectid>/<qty>', methods=['POST', 'GET'])
def checkIn_hardware(projectid, qty):
    return jsonify(projectid, qty)


@api.route('/api/checkout/<projectid>/<qty>', methods=['POST', 'GET'])
def checkOut_hardware(projectid, qty):
    return jsonify(projectid, qty)


@api.route('/api/join/<projectid>', methods=['POST', 'GET'])
def joinProject(projectid):
    return projectid


@api.route('/api/leave/<projectid>', methods=['POST', 'GET'])
def leaveProject(projectid):
    return projectid


def login(user_input, pass_input):
    myquery = {"userId": user_input, "password": pass_input}
    x = passwords.find_one(myquery)
    if (x == None):
        return False
    return True


if __name__ == "__main__":
    api.run(host='0.0.0.0', debug=False,
            port=os.environ.get('PORT', 82))
