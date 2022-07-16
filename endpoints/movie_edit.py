from app import app
from flask import jsonify, request
import uuid
import bcrypt

# this endpoint displays editing options for movies
# only added by THE ADMIN THAT IS LOGGED IN.
# THIS IS ONLY FOR ADMIN USERS! NO ONE ELSE CAN SEE
# THIS ENDPOINT.

# movie get request
# requires is_admin boolean, as well as admin and
# related movie ID to uploaded movies.
# CANNOT get others uploaded movies. only users.
# requires token.

@app.get('/api/movie-editing')
def fetch_movie():
    pass

# movie post request
# requires is_admin boolean
# this is for submitting new movies into the 
# database.
# requires token.

@app.post('/api/movie-editing')
def post_movie():
    pass

# movie patch request
# CANNOT edit others uploaded movies.
# requires is_admin boolean
# requires token.

@app.patch('/api/movie-editing')
def edit_movie():
    pass

# movie delete request
# IS NOT ALLOWED due to confusing new and old movies
# and others uploading titles etc.
# the patch request should be enough for fixing mistakes