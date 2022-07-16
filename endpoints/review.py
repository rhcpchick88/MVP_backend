from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid
import bcrypt

# reviews also have a "lookup table" with RATINGS. 
# RATINGS are out of 5 and the reason they are posted 
# on a "lookup" table is if the rating system
# ever changes.
# They do not have to be posted ALONG SIDE a review. 
# It is optional.

# review get request
# for admins and users, this displays their 
# personal reviews. requires token for this

@app.get('/api/reviews')
def review_get():
    token = request.headers.get("token")
    token_check = run_query("SELECT id FROM user_session WHERE token=?", [token])
    user_id = token_check[0][0]
    if not user_id:
        review_list = run_query("SELECT * FROM review")
        resp =[]
        for review in review_list:
            review_obj = {}
            review_obj["id"] = review[0]
            review_obj["review"] = review[1]
            review_obj["userId"] = review[2]
            review_obj["rating"] = review[3]
            review_obj["movieId"] = review[4]
            review_obj["isApproved"] = review[5]
            resp.append(review_obj)
        return jsonify(review_list),200
    else:
        user_review = run_query("SELECT id FROM review WHERE user_id=?", [user_id])


# review post request
# only users can see this!
# refer to the movie uploaded in the database to post
# a review.
# requires token.

@app.post('/api/reviews')
def review_post():
    pass

# review patch request
# allows user to edit their reviews and rating if
# they please.
# requires token.

@app.patch('/api/reviews')
def review_edit():
    pass

# review delete request
# allows user to delete their reviews if desired.
# requires token.

@app.delete('/api/reviews')
def review_delete():
    pass

