from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query


# this endpoint displays editing options for movies
# only added by THE ADMIN THAT IS LOGGED IN.
# THIS IS ONLY FOR ADMIN USERS! NO ONE ELSE CAN SEE
# THIS ENDPOINT.

# movie get request


@app.get('/api/movie-editing')
def fetch_movie():
    token = request.headers.get("token")
    if not token:
        return jsonify ("Error, not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM user_session WHERE token=?", [token])
        user_id = token_check[0][0]
        admin_check = run_query("SELECT is_admin FROM user WHERE id=?", [user_id])
        is_admin = admin_check[0][0]
        if is_admin == 0:
            return jsonify("Error, not authorized"), 401
        else:
            movie_list = run_query("SELECT * FROM movie")
            movie_resp = []
            for movie in movie_list:
                movie_obj = {}
                movie_obj["id"] = movie[0]
                movie_obj["genre"] = movie[1]
                movie_obj["overview"] = movie[2]
                movie_obj["releaseDate"] = movie[3]
                movie_obj["tagline"] = movie[4]
                movie_obj["title"] = movie[5]
                movie_resp.append(movie_obj)
            return jsonify(movie_resp)

# movie post request
# requires is_admin boolean
# this is for submitting new movies into the 
# database.
# requires token.

@app.post('/api/movie-editing')
def post_movie():
    token = request.headers.get("token")
    if not token:
        return jsonify ("Error posting movie, user not logged in"), 401    
    else:        
        data = request.json
        review = data.get("review")
        movie = data.get("movie")
        rating = data.get("rating")
        token_check = run_query("SELECT id FROM user_session WHERE token=?", [token])
        if not token_check:
            return jsonify("Error posting review, user not logged in"), 401
        user_id = token_check[0][0]
        movie_check = run_query("SELECT id FROM movie WHERE title=?", [movie])
        if not movie_check:
            return jsonify("Error, movie not in database"), 422              
        movie_id = movie_check[0][0]  
        rating_check = run_query("SELECT id FROM rating WHERE rating=?", [rating])
        if not rating_check:
            return jsonify("Error, must enter correct rating from 1 to 5"), 422
        if not user_id:
            return jsonify("Error posting review, user does not exist")        
        if not review:
            return jsonify ("Missing required argument : review"), 422
        if not movie:
            return jsonify ("Missing required argument : movie"), 422        
        else:
            run_query("INSERT INTO reviews (review, user_id, rating, movie_id) VALUES (?,?,?,?)", [review, user_id, rating, movie_id])
            return jsonify("Review added successfully"), 201

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