from flask import Flask

app = Flask(__name__)

from endpoints import search
from endpoints import movie_edit
from endpoints import review_edit
from endpoints import movie
from endpoints import review
from endpoints import user_session
from endpoints import user