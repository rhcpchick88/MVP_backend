from lib2to3.pgen2 import token
from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid
import bcrypt

# basic login and logout session endpoint. 

#login post request
@app.post('/api/user-login')
def user_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email:
        return jsonify ("Missing required argument: email"), 401
    if not password:
        return jsonify ("Missing required argument: password"), 401
    password_check = run_query("SELECT password FROM user WHERE email=?",[email])
    user_password = password_check[0][0]
    if bcrypt.checkpw(password.encode(), user_password.encode()):
        token = uuid.uuid4().hex
        print(token)
        user_check = run_query("SELECT id FROM user WHERE email=?", [email])
        user_id = user_check[0][0]
        run_query("INSERT INTO user_session (id, token) VALUES (?,?)", [user_id, token])
        return jsonify ([token]),201
    else:
        return jsonify ("Error logging in, email and password combination invalid."), 401


#login delete request

@app.delete('/api/user-login')
def user_logout():
    token = request.headers.get("token")
    if not token:
        return jsonify ("Error, missing valid token"), 401
    user_check = run_query("SELECT id FROM user_session WHERE token=?", [token])
    user_id = user_check[0][0]
    if user_id:
        run_query("DELETE FROM user_session WHERE id=?", [user_id])
        return jsonify ("Logout successful"), 204
    else:
        return jsonify ("Error logging out"), 401
