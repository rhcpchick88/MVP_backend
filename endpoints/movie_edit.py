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
                movie_obj["overview"] = movie[1]
                movie_obj["releaseDate"] = movie[2]
                movie_obj["tagline"] = movie[3]
                movie_obj["title"] = movie[4]
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
        return jsonify ("Error, not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM user_session WHERE token=?", [token])
        user_id = token_check[0][0]
        admin_check = run_query("SELECT is_admin FROM user WHERE id=?", [user_id])
        is_admin = admin_check[0][0]
        if is_admin == 0:
            return jsonify("Error, not authorized"), 401  
        data = request.json
        overview = data.get("overview")
        release_date = data.get("releaseDate")
        tagline = data.get("tagline")
        title = data.get("title")
        title_check = run_query("SELECT id FROM movie WHERE title=?", [title])
        if title_check:
            return jsonify("Error, movie already exists")
        token_check = run_query("SELECT id FROM user_session WHERE token=?", [token])
        if not token_check:
            return jsonify("Error posting movie, user not logged in"), 401
        user_id = token_check[0][0]
        if not user_id:
            return jsonify("Error posting movie, user does not exist")        
        if not title:
            return jsonify ("Missing required argument : Title"), 422    
        else:
            run_query("INSERT INTO movie (overview, release_date, tagline, title, user_id) VALUES (?,?,?,?,?)", [overview, release_date, tagline, title, user_id])
            return jsonify("Movie added successfully"), 201

# movie patch request
# CANNOT edit other admin's uploaded movies.
# ONLY CAN EDIT OWN UPLOADED MOVIE.
# requires is_admin boolean
# requires token.

@app.patch('/api/movie-editing')
def edit_movie():
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
        data = request.json
        overview = data.get("overview")
        release_date = data.get("releaseDate")
        tagline = data.get("tagline")
        # changing title allows for fixing mistakes in entry        
        title = data.get("title")
        title_check = run_query("SELECT id FROM movie WHERE title=?", [title])
        if not title_check:
            return jsonify("Error, movie not in database")
        id_check = run_query("SELECT id FROM movie WHERE user_id=?", [user_id])
        if not id_check:
            return jsonify("Error, movie not uploaded by user"), 422
        else:
            movie_id = run_query("SELECT id FROM movie WHERE user_id=? AND title=?", [user_id, title])
            if overview:
                run_query("UPDATE movie SET overview =? WHERE id=?", [overview, movie_id])
                return jsonify("Overview updated successfully"), 201
            else:
                pass            
            if release_date:
                run_query("UPDATE movie SET release_date =? WHERE id=?", [release_date, movie_id])
                return jsonify("Release date updated successfully"), 201  
            else:
                pass          
            if tagline:
                run_query("UPDATE movie SET tagline=? WHERE id=?", [tagline, movie_id])
                return jsonify("Tagline updated successfully"), 201 
            else:
                pass           
            if title:
                run_query("UPDATE movie SET title=? WHERE id=?", [title, movie_id])
                return jsonify("Title updated successfully"), 201
            else:
                return jsonify("Error updating movie"), 500

# movie delete request
# IS NOT ALLOWED due to confusing new and old movies
# and others uploading titles etc.
# the patch request should be enough for fixing mistakes