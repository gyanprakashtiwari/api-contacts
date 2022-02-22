from flask import Flask, jsonify, make_response, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager



app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)

JWTManager(app)






from app import views , models