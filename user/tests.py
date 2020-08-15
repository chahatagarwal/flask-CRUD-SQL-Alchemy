import pytest
from user import app, db
import json
import base64
from flask import Flask, session
from .models import  User


class Test_API:
    client  = app.test_client()
    
    @pytest.fixture(autouse=True, scope='session')
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()
        yield db
        db.drop_all()
    
    def test_data_in_db_before_addition(self):
        user = User.query.all()
        assert len(user) == 0
        
    def test_create(self):
        url = "/create"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        payload = "{\n\t\"username\": \"test01\",\n\t\"password\": \"test\", \n\t\"useremail\":\"user@test.com\"}"
        response = self.client.post(url, data=payload, headers=headers)
        assert response.status_code == 200
        assert response.json['Message'].strip() == 'Created successfully'

    def test_data_in_db_after_addition(self):
        user = User.query.all()
        assert user[0].id == 1
        assert user[0].username == "test01"    


    def test_read(self):
        url = "/read"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        response = self.client.get(url, headers=headers)
        assert response.status_code == 200
        assert response.json['password'].startswith("sha256")
        
    def test_update(self):
        url = "/update/1"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        payload = "{\n\t\"username\": \"updated_username\"}"
        response = self.client.put(url,data=payload, headers=headers)
        assert response.status_code == 200
        assert response.json['Message'] == 'Updated successfully'
    
    def test_updated_data_in_db(self):
        user = User.query.all()
        assert user[0].id == 1
        assert user[0].username == "updated_username"    

    def test_invalid_update(self):
        url = "/update/1255"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        payload = "{\n\t\"username\": \"updated_username\"}"
        response = self.client.put(url,data=payload, headers=headers)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Check your user id'


    def test_delete(self):
        url = "/delete/1"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        # payload = "{\n\t\"username\": \"updated_username\"}"
        response = self.client.delete(url, headers=headers)
        assert response.status_code == 204
        
    def test_delete_in_db(self):
        user = User.query.all()
        assert len(user) == 0

    def test_invalid_delete(self):
        url = "/delete/1255"
        headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
        # payload = "{\n\t\"username\": \"updated_username\"}"
        response = self.client.delete(url, headers=headers)
        assert response.status_code == 400
        assert response.json['Message'].strip() == 'Check your user id'
