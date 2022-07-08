from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid
import bcrypt

# for user profile information.


# user get request
# displays user profile information. 
# requires login token.

@app.get('/api/user')
def profile_get():
    pass


# user post request 
# create user profile 
# does not require token

@app.post('/api/user')
def profile_create():
    pass


# user patch request
# update user profile
# requires login token.

@app.patch('/api/user')
def profile_edit():
    pass


# user delete request
# delete a user profile
# requires login token.

@app.delete('/api/user')
def profile_delete():
    pass