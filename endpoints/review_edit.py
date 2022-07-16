from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query


# this endpoint displays REVIEWS needing approval
# ONLY ADMINS CAN SEE THIS ENDPOINT NO ONE ELSE

# for admins this displays "pending reviews"
# the boolean will show "is not approved" movies so
# admins can approve the review.
# once the review is approved the boolean will 
# show "is approved" and show in the general
# public review endpoint and disappear out of this 
# endpoint.

# review get request
# only sees unapproved movie reviews *
# requires token

@app.get('/api/review-approval')
def review_display():
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
            review_list = run_query("SELECT * FROM reviews WHERE is_approved=0")
            return jsonify(review_list)

# review post request
# NOT ALLOWED. not for posting new review information.

# review patch request
# for approving specific reviews.
# requires token

@app.patch('/api/review-approval')
def review_approve():
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
            data = request.json
            title = data.get("title")
            if not title:
                return jsonify("Error, missing required argument : movie title")
            movie_check = run_query("SELECT id FROM movie WHERE title=?", [title])
            if not movie_check:
                return jsonify("Error, movie not in database"), 422
            movie_id = movie_check[0][0]
            review_check = run_query("SELECT id FROM reviews WHERE movie_id=? AND is_approved=0", [movie_id])
            if not review_check:
                return jsonify("Error, review not in database"), 422
            review_id = review_check[0][0]
            run_query("UPDATE reviews SET is_approved=1 WHERE id=?",[review_id])
            return jsonify("Review approved")
                    
                    
                

# review delete request
# NOT ALLOWED cannot delete reviews.
# the reviews are automatically not approved
# so they won't show up anyways.
