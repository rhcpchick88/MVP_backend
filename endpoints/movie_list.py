from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query

# this endpoint is just for displaying public
# movie information.

# movie get request
# public, anyone logged in or out can see any movie.
# does not require token.


@app.get('/api/movie-list')
def movie_get():
    movie_list = run_query("SELECT * FROM movie")
    print(movie_list)
    resp =[]
    for movie in movie_list:
        movie_obj = {}
        movie_obj["title"] = movie[1]
        resp.append(movie_obj)
    return jsonify(resp),200

# post, patch, delete not allowed here as that is for 
# ADMINS only and will be on movie_edit endpoint.
