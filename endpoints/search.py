from random import choices
from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
from rapidfuzz import fuzz, process

# this endpoint is just for displaying public
# movie information.

# movie post request
# public, anyone logged in or out can see any movie.
# does not require token.


@app.post('/api/movie-search')
def movie_search():
    data = request.json
    choice = data.get("search")
    movie_list = run_query("SELECT title FROM movie")
    resp = []
    for movie in movie_list:
        # performing a fuzzy search. taking my input parameter and comparing
        # it to each movie title. The scorer compares how close the result is
        # to the entered search. I chose token ratio because it returns a search
        # with a word AT ANY POINT in the string, in the other ratio options
        # it has to match the position in the string and therefore was not returning
        # ideal search results (ex batman would just return batman, not batman forever)
        result=process.extract(choice, movie, scorer=fuzz.token_ratio)
        # Looping through the results and appending the response
        # with each item in the search result that scored a match of "80" or above. 
        for item in result:
            # the second item in the tuple represents match score
            if item[1] >= 80:
                movie_id=run_query("SELECT id FROM movie WHERE title=?",[result[0][0]])
                resp.append(result+movie_id)
                
    return jsonify(resp)
    
    #TODO ERROR CODE - I PUT AN ERROR CODE IN IF ELSE 
    # BY THE RESPONSE BUT IT WRECKED MY SEARCH RESULT. 

# post, patch, delete not allowed here as that is for 
# ADMINS only and will be on movie_edit endpoint.
