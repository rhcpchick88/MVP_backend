from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid
import bcrypt

# for user profile information.


# user get request
# displays user profile information. 
# requires login token.


@app.get('/api/user')
def profile_get():
    # request a token header to verify the user is authenticated
    token = request.headers.get("token")
    if not token:
        return jsonify ("Error, not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM user_session WHERE token=?", [token])
        user_id = token_check[0][0]
        user_information = run_query("SELECT * FROM user WHERE id=?", [user_id])
        profile_resp = []
        for user in user_information:
            user_obj = {}
            user_obj["email"] = user[1]
            user_obj["username"] = user[2]
            user_obj["firstName"] = user[4]
            user_obj["lastName"] = user[5]
            user_obj["aboutMe"] = user[7]
            user_obj["pictureOne"] = user[8]
            user_obj["pictureTwo"] = user[9]
            user_obj["pictureThree"] = user[10]
            user_obj["adminStatus"] = user[11]
            user_obj["favoriteMovie"] = user[12]
            user_obj["favoriteGenre"] = user[13]
            profile_resp.append(user_obj)
        return jsonify(user_information), 200


# user post request 
# create user profile 
# does not require token
#TODO unique checks.

@app.post('/api/user')
def profile_create():
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    aboutMe = data.get("aboutMe")
    pictureOne = data.get("pictureOne")
    pictureTwo = data.get("pictureTwo")
    pictureThree = data.get("pictureThree")
    favoriteMovie = data.get("favoriteMovie")
    favoriteGenre = data.get("favoriteGenre")
    email_check = run_query("SELECT id FROM user WHERE email=?",[email])
    user_id = email_check[0][0]
    if user_id:
        return jsonify("Error, user already exists")
    if not email:
        return jsonify ("Missing required argument: email"), 422
    if not username:
        return jsonify ("Missing required argument: username"), 422
    if not password:
        return jsonify ("Missing required argument: password"), 422
    if not firstName:
        return jsonify ("Missing required argument: first name"), 422
    # password salt and hash for DB encryption
    userPassword = password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(userPassword.encode(), salt)
    run_query("INSERT INTO user (email, username, password, first_name, last_name, about_me, picture_one, picture_two, picture_three, favorite_movie, genre) VALUES (?,?,?,?,?,?,?,?,?,?,?)", [email, username, hashed_password, firstName, lastName, aboutMe, pictureOne, pictureTwo, pictureThree, favoriteMovie, favoriteGenre])
    # creating a token for user as profile creation will log the user in automatically
    # hexing the UUID to remove dashes
    token = uuid.uuid4().hex
    user_check = run_query("SELECT id FROM user WHERE email=?", [email])
    user_id = user_check[0][0]
    run_query("INSERT INTO user_session (id, token) VALUES (?,?)", [user_id, token])
    return jsonify([token]), 201


# user patch request
# update user profile
# requires login token.
#TODO make update all at once

@app.patch('/api/user')
def profile_edit():
    # request a token header to verify the user is authenticated
    token = request.headers.get("token")
    if not token:
        return jsonify ("Not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM user_session WHERE token=?", [token])
        user_id = token_check[0][0]
    if not user_id:
        return jsonify ("Error updating user information, invalid login session"), 401
    else:
        data = request.json
        # cannot change the email as it is a unique identifier for the profile
        username = data.get("username")
        password = data.get("password")
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        aboutMe = data.get("aboutMe")
        pictureOne = data.get("pictureOne")
        pictureTwo = data.get("pictureTwo")
        pictureThree = data.get("pictureThree")
        favoriteMovie = data.get("favoriteMovie")
        favoriteGenre = data.get("favoriteGenre")
        # update the fields individually as all fields are not required to be updated 
        # for the patch request. Enables user to update one field at a time if they want.
        if username:
            run_query("UPDATE user SET username=? WHERE id=?", [username, user_id])
            return jsonify("Username updated successfully"), 201
        else:
            pass
        if password:
            # updated password still needs encryption like before
            userPassword = password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(userPassword.encode(), salt)
            run_query("UPDATE user SET password=? WHERE id=?", [hashed_password, user_id])
            return jsonify ("Password updated successfully"), 201
        else:
            pass
        if firstName:
            run_query("UPDATE user SET first_name=? WHERE id=?", [firstName, user_id])
            return jsonify ("First name updated successfully"), 201
        else:
            pass
        if lastName:
            run_query("UPDATE user SET last_name=? WHERE id=?", [lastName, user_id])
            return jsonify ("Last name updated successfully"), 201
        else:
            pass
        if aboutMe:
            run_query("UPDATE user SET about_me=? WHERE id=?", [aboutMe, user_id])
            return jsonify ("About me updated successfully"), 201
        else:
            pass
        if pictureOne:
            run_query("UPDATE user SET picture_one=? WHERE id=?", [pictureOne, user_id])
            return jsonify ("Picture updated successfully"), 201
        else:
            pass
        if pictureTwo:
            run_query("UPDATE user SET picture_two=? WHERE id=?", [pictureTwo, user_id])
            return jsonify ("Picture updated successfully"), 201
        else:
            pass
        if pictureThree:
            run_query("UPDATE user SET picture_three=? WHERE id=?", [pictureThree, user_id])
            return jsonify ("Picture updated successfully"), 201
        else:
            pass
        if favoriteMovie:
            run_query("UPDATE user SET favorite_movie=? WHERE id=?", [favoriteMovie, user_id])
            return jsonify ("Favorite movie updated successfully"), 201
        else:
            pass
        if favoriteGenre:
            run_query("UPDATE user SET genre=? WHERE id=?", [favoriteGenre, user_id])
            return jsonify ("Favorite genre updated successfully"), 201
        else:
            return jsonify ("Error updating user profile"), 500


# user delete request
# delete a user profile
# requires login token.

@app.delete('/api/user')
def profile_delete():
    # request a token header to verify the user is authenticated
    token = request.headers.get("token")
    if not token:
        return jsonify ("Not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM user_session WHERE token=?", [token])
        user_id = token_check[0][0]
        if not user_id:
            return jsonify("Error deleting profile"), 401
        else:
            # must delete the session token as well as the profile
            run_query("DELETE FROM user_session WHERE id=?", [user_id])
            run_query("DELETE FROM user WHERE id=?", [user_id])
            return jsonify ("Profile deleted successfully, logged out"), 204