import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from redis import Redis

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
q = Queue(connection=Redis(host=os.getenv("REDIS_HOST"),
                           port=os.getenv("REDIS_PORT")))
