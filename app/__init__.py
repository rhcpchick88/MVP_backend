from flask import Flask

app = Flask(__name__)

from endpoints import admin_session
from endpoints import admin
from endpoints import movie
from endpoints import review
from endpoints import user_session
from endpoints import user