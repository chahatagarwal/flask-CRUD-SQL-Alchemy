from flask import Flask, request, jsonify, make_response, session, app, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand
import json
from user import app, db
from .models import User
from flask import render_template, redirect, url_for, flash
import datetime


@app.route('/create', methods=['POST'])
def create():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(username=post_data.get('username')).first()
    if not user:
        user = User(
            username=post_data.get('username'),
            useremail=post_data.get('useremail'),
            password="sha256_" + post_data.get('password')
        )
        # insert the user
        db.session.add(user)
        db.session.commit()
        responseObject = {
            'Message': 'Created successfully'
        }
        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'Message': 'Check the fields entered',
        }
    return make_response(jsonify(responseObject)), 400


@app.route('/read', methods=['GET'])
def login():
    #read all user from db
    user = User.query.all()
    if user:
        responseObject = {
            'password': user[0].password
        }
        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'Message': 'Could not verify'
        }
        return make_response(jsonify(responseObject)), 400

@app.route('/update/<id>', methods=['PUT'])
def update(id):
    # get the data
    username = json.loads((request.data).decode())
    username = username['username']
    # check if user already exists
    stmt = User.query.get(id)
    if stmt:
      stmt.username = username
      db.session.commit()
      if stmt:
          responseObject = {
              'Message': 'Updated successfully'
          }
          return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'Message': 'Check your user id'
        }
    return make_response(jsonify(responseObject)), 400

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    # check if user already exists
    stmt = User.query.get(id)
    if stmt:
      stmt.query.delete()
      db.session.commit()
      if stmt:
          responseObject = {
            'Message': ''
        }
          return make_response(jsonify(responseObject)),204
    else:
        responseObject = {
            'Message': 'Check your user id'
        }
    return make_response(jsonify(responseObject)), 400