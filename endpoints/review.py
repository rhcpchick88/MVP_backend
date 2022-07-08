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
# for public it displays general reviews.
# for admins and users, this displays their 
# personal reviews. requires token for this

@app.get('/api/reviews')
def review_get():
    pass


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

