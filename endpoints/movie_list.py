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
    movie_info = run_query("SELECT * FROM movie ORDER BY title")
    movie_resp = []
    for movie in movie_info:
        movie_obj = {}
        movie_obj["id"] = movie[0]
        movie_obj["overview"] = movie[1]
        movie_obj["releaseDate"] = movie[2]
        movie_obj["tagline"] = movie[3]
        movie_obj["title"] = movie[4]
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
    name = data.get("reviewSearch")
    movie_result = run_query("SELECT * FROM movie WHERE title=?", [name])
    # movie result gives a list of the movies, as there may be multiple
    # movies with the same name (ex remakes)
    for movie in movie_result:
        movie_id=movie[0]
        # grabbing the ID from the movie so I can use it to pull the reviews
        review_result=run_query("SELECT * FROM reviews WHERE movie_id=?",[movie_id])
        print(review_result)
        review_resp=[]
        for review in review_result:
            review_obj={}
            review_obj["id"]=review[0]
            review_obj["review"]=review[1]
            review_obj["user_id"]=review[2]
            review_obj["rating"]=review[3]
            review_obj["is_approved"]=review[4]
            review_resp.append(review_obj)
    if review_resp is None:
        return jsonify("No existing reviews")
    else:
        return jsonify(review_resp)




# patch, delete not allowed here as that is for 
# ADMINS only and will be on movie_edit endpoint.
