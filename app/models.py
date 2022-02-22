from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

import uuid
import jwt
import datetime



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100),unique = True, nullable = False)
    address = db.Column(db.String(200), nullable = False)
    password_hash = db.Column(db.Text, nullable = False)

    contacts_of_user = db.relationship("Contact" , backref='user', lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{{self.name}} : {{self.email}}"
  

class Contact(db.Model):
    __tablename__ = "all_contacts"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(200), nullable = False)
    country = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"{{self.name}} contact is in user list with id : {{self.user_id}}"
  
