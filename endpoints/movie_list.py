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
    movie_info = run_query("SELECT * FROM movie")
    movie_resp = []
    for movie in movie_info:
        movie_obj = {}
        movie_obj["id"] = movie[0]
        movie_obj["genres"] = movie[1]
        movie_obj["overview"] = movie[2]
        movie_obj["releaseDate"] = movie[3]
        movie_obj["tagline"] = movie[4]
        movie_obj["title"] = movie[5]
        # response = run_query("SELECT movie.id, reviews.id, reviews.review, reviews.user_id, reviews.rating, reviews.movie_id, reviews.is_approved FROM movie_reviews.movie RIGHT JOIN reviews ON movie.id=reviews.movie_id WHERE movie.id=?",[movie[0]])
        # print(response)
        movie_resp.append(movie_obj)
    return jsonify(movie_resp)

# review post request
# public, anyone logged in or out can see any review.
# does not require token. Use along side movie Get.

@app.post('/api/movie-list')
def review_search():
    data = request.json
    movie_id = data.get("movieId")
    review_list = run_query("SELECT * FROM reviews WHERE movie_id=?", [movie_id])    
    review_resp = []
    for review in review_list:
        review_obj={}
        review_obj["id"] = review[0]
        review_obj["review"] = review[1]
        review_obj["userId"] = review[2]
        review_obj["rating"] = review[3]
        review_obj["movieId"] = review[4]
        review_obj["isApproved"] = review[5]
        review_resp.append(review_obj)
    return jsonify(review_resp)




# patch, delete not allowed here as that is for 
# ADMINS only and will be on movie_edit endpoint.
