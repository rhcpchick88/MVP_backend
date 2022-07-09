from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid
import bcrypt

# MOVIE SEARCH ENDPOINT!!! This is separate
# from a list of movies. Aim to make it a 
# "fuzzy search" - this optimizes data return

# search get request
# search for and display specific movies. 
# anyone can do this.

#TODO lookup filtered search

@app.get('/api/movie-search')
def movie_search():
    movie_list = run_query("SELECT * FROM movie WHERE id=1")
    return jsonify(movie_list), 200
    

# post, patch, delete not allowed here as that is for 
# ADMINS only and will be on movie_edit endpoint.
