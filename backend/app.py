
from flask import Flask, request, jsonify
from database import users_collection, recipes_collection
from bson.objectid import ObjectId
import bcrypt
import os
import jwt
from datetime import datetime, timezone, timedelta
from flask_cors import CORS

JWT_SECRET = os.getenv("JWT_SECRET")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3006"}}) # Allow specific origin

#user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    #check that the fields aren't empty
    if not username or not password:
        return jsonify({'message': 'Missing one of the required fields.'}), 400

    #check that the username is unique
    if users_collection.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 400
    
    #hash the password with bcrypt
    hashed_password = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')

    user_data = { 'username':username,
                 'password': hashed_password,
                 'createdAt': datetime.now(timezone.utc)
    }
    #insert user into the database
    users_collection.insert_one(user_data)
    return jsonify({"status":"success"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username= data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username or password cannot be empty'}), 400
    
    user = users_collection.find_one({'username':  username})

    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):

        # token information: user ID converted to str, issued at, and expiration time
        payload = {
            'sub': str(user['_id']),
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
            }
        
        user_token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        response = jsonify({
            'message': 'Login successful',
            'userId': str(user['_id']),
            'userToken': user_token
        })
        response.statuscode = 200
        return response
    else:
        return jsonify({'message': 'Username or password are invalid'}), 401   
    
@app.route('/recipe', methods=['POST'])
def new_recipe():
    try:
        token = request.headers['Authorization']
        user_id= retrive_id(token)
    except Exception:
        return jsonify({'message':'Invalid JWT token'}), 401
    body_data = request.get_json()
    print(body_data)
    #format body data (user entries) to insert in database
    recipe_data = {
        'userId': user_id,
        'name': body_data.get('name'),
        'description': body_data.get('description'),
        'ingredients': body_data.get('ingredients'),
        'instructions': body_data.get('instructions'),
        'cookTime': body_data.get('cookTime'),
        'servings': body_data.get('servings'),
        'createdAt': datetime.now(timezone.utc)
    }
    
    #insert in database and return result id
    result = recipes_collection.insert_one(recipe_data)
    return jsonify({'message':'Recipe added successfully', 'recipeId': str(result.inserted_id)}), 201

@app.route('/recipe', methods=['GET'])
def get_recipe_list():
    try:
        token = request.headers['Authorization']
        user_id = retrive_id(token)
    except Exception:
        return jsonify({'message':'Invalid JWT token'}), 401
    
    recipe_list = list(recipes_collection.find({'userId': user_id}))

    for recipe in recipe_list:
        recipe['_id'] = str(recipe['_id'])
        recipe['userId'] = str(recipe['userId'])
    
    return jsonify({'recipes': recipe_list}), 200

@app.route('/recipe/<recipe_id>', methods=['GET'])
def get_single_recipe(recipe_id):
    try:
        token = request.headers['Authorization']
        user_id = retrive_id(token)
    except Exception:
        return jsonify({'message':'Invalid JWT token'}), 401

    try:
        recipe_id_obj = ObjectId(recipe_id)
    except Exception:
        return jsonify({'message':'Invalid recipe ID format'}), 400
    
    recipe = recipes_collection.find_one({'_id':recipe_id_obj,'userId': user_id})
    if recipe:
        recipe['_id'] = str(recipe['_id'])
        recipe['userId'] = str(recipe['userId'])
        return jsonify(recipe), 200
    else:
        return jsonify({'message': 'Recipe not found'}), 404
    
@app.route('/recipe/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    try:
        token = request.headers['Authorization']
        user_id = retrive_id(token)
    except Exception:
        return jsonify({'message':'Invalid JWT token'}), 401

    body_data = request.get_json()
    # iterate through the data recieved from the front end and update only the values that are allowed to be updated to a new recipe object
    updated_recipe = {k: v for (k, v) in body_data.items() if k not in ['_id', 'userId', 'createdAt']}
    
    # update the document, ensure the recipe matches the user updating.
    result = recipes_collection.update_one({'_id':ObjectId(recipe_id), 'userId': ObjectId(user_id)}, {'$set': updated_recipe})

    # check if the result found 1 recipe in database, otherwise return not found. Matched count will never be more than 1 (unique ID).
    if result.matched_count == 1:
        return jsonify({'message':'Recipe updated successully'}), 200
    else:
        return jsonify({'message':'Recipe not found'}), 404
    
@app.route('/recipe/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    token = request.headers['Authorization']
    try:
        user_id = retrive_id(token)
    except Exception:
        return jsonify({'message':'Invalid JWT token'}), 401

    result = recipes_collection.delete_one({'_id': ObjectId(recipe_id), 'userId': ObjectId(user_id)})
    
    if result.deleted_count == 1:
        return jsonify({'message': 'Recipe delete successfully'}), 200
    
    else:
        return jsonify({'message': 'Recipe not found'}), 404
    
def retrive_id(token):
    #decode token, error handling
    try:
        user_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = ObjectId(user_token['sub'])
        if not users_collection.find_one({'_id': user_id}):
            raise Exception("Invalid JWT token")
    except Exception:
        raise Exception("Invalid JWT token")
    return user_id