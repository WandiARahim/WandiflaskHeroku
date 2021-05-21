import functools
from flask import Flask,jsonify,request,g
from config.Settings import Settings

import jwt
import re

app = Flask(__name__)

def login_required(func):
    @functools.wraps(func)
    def secure_login(*args, **kwargs):
        auth=True

        auth_header = request.headers.get('Authorization') #retrieve authorization bearer token
        if auth_header: 
            auth_token = auth_header.split(" ")[1]#retrieve the JWT value without the Bearer 
        else:
            auth_token = ''
            auth=False #checking for failures
        if auth_token:
            try:
                payload = jwt.decode(auth_token,Settings.secretKey,algorithms=['HS256'])
                g.userid=payload['userid']#update info in flask application context's g that lasts for one req/res cyycle
                g.role=payload['role']

            except jwt.exceptions.InvalidSignatureError as err:
                print(err)
                auth=False #Failed check

        if auth==False:
            return jsonify({"Message":"Not Authorized!"}),403 #return response

        return func(*args, **kwargs)

    return secure_login


def validateRegister(func):
    @functools.wraps(func)
    def validate(*args, **kwargs):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        role = request.json['role']
        print("username",username)
        print("email",email)
        print("password",password)
        print("role",role)
        patternUsername = re.compile('^[a-zA-Z0-9]+$')
        patternEmail = re.compile('^[a-zA-Z0-9]+[\.]?[a-zA-Z0-9]+@\w+\.\w+$')
        patternPassword = re.compile('^[a-zA-Z0-9]{8,}$') #8 character password
        print(patternUsername.match(username)) #return true or false
        print(patternEmail.match(email))
        print(patternPassword.match(password))
        if (patternUsername.match(username) and patternEmail.match(email) and patternPassword.match(password)):
            return func(*args,**kwargs)
        else:
            return jsonify({"Message": "Validation failed"}),403 #error 
    return validate



def validateNumber(num):
    patternNum=re.compile('^(([1-9][0-9]*)|0)(\.[0-9]{2})?$')
    return patternNum.match(num)