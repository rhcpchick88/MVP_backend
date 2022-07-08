from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid
import bcrypt

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
    pass

# review post request
# for approving specific reviews.
# requires token

@app.post('/api/review-approval')
def review_approve():
    pass

# review patch request
# NOT ALLOWED cannot edit others' reviews

# review delete request
# for deleting & not approving reviews.
# requires token.

@app.delete('/api/review-approval')
def review_disapprove():
    pass