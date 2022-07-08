from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid
import bcrypt

# this endpoint is just for displaying public
# movie information.

# movie get request
# public, anyone logged in or out can see any movie.
# does not require token.

@app.get('/api/movie-search')
def movie_get():
    pass

# post, patch, delete not allowed here as that is for 
# ADMINS only and will be on movie_edit endpoint.