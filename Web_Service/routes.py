
from ast import Return
import datetime
from datetime import timedelta

from email import message
from functools import wraps
import json
from logging import exception
from os import access
from unittest import result
from urllib import response
import requests

from uuid import uuid4

import jwt
from flask import Blueprint, jsonify, make_response, request
from jwt import exceptions
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash


import models
from models import database
from scraper_funcs import create_search_string


home_bp = Blueprint('homepage', __name__, url_prefix='/home')
search_bp = Blueprint('search', __name__, url_prefix='/search')
authorise_bp = Blueprint('registration', __name__, url_prefix='/authorisation')
saved_bp = Blueprint('saved', __name__, url_prefix='/saved')


def requires_token(fun):
    """A decorater function that prevents unauthorised users from accessing protected functionallity.

    Args:
        fun (function): A fucntion that requires authorisation for access

    Returns:
        user: Returns a User object that corresponds request authorisation token.
    """
    @wraps(fun)
    def decorated(*args, **kwargs):
        token = None

        if 'autherisation-token' in request.headers:
            token = request.headers['autherisation-token']
        if not token:
            return make_response(jsonify("Token required"), 403)
        try:
            pub_id = jwt.decode(token, '$SECRET_KEY', algorithms="HS256")
            user = models.User.query.filter_by(
                pub_id=pub_id['public_id']).first()
        except:
            return make_response(jsonify({"message": "Invalid token, please login"}), 403)

        return fun(user, *args, **kwargs)

    return decorated


@home_bp.route('/', methods=['GET'])
def homepage():
    """Returns data to the homepage of all queries held by a authenticated user.

    Returns:
        JSON: Json data of all query objects associated with a user object. 
    """
    # token = request.json["token"]
    token = None

    if 'autherisation-token' in request.headers:
        token = request.headers['autherisation-token']

    if token:
        try:
            pub_id = jwt.decode(token, '$SECRET_KEY', algorithms="HS256")
            user = models.User.query.filter_by(
                pub_id=pub_id["public_id"]).first()
            if user:
                # if len(user.searches) == 0:
                #     return make_response(jsonify({'message' : 'No saved queries'}), 200)
                # else:
                queries = user.searches
                return make_response(jsonify({'queries': [query.to_dict() for query in queries]}), 200)
            if not user:
                return make_response(jsonify([{'message': 'Invalid token'}]))
        except exceptions.ExpiredSignatureError:
            return make_response(jsonify([{'message': 'Token expired, login to see saved searches data'}]), 403)
    else:
        return make_response(jsonify([{'queries': 0}]), 200)


@authorise_bp.route('/register', methods=['POST'])
def register():
    """
    Route to allow an anonymous user to create a user account. 
    Checks if user user already exist with details

    Returns:
        JSON: Json containing message that user was created.
    """
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    confirmed_password = request.json['confirmed-password']

    does_exist = models.User.query.filter_by(email=email).first()

    if does_exist:
        return make_response(jsonify([{'message': 'User already exist with this email, please sign in.'}]), 409)

    if password == confirmed_password:
        hash = generate_password_hash(password)
        new_user = models.User(pub_id=str(
            uuid4()), username=username, email=email, password=hash)

        database.session.add(new_user)
        database.session.commit()
        database.session.close()
        return make_response(jsonify([{'message': 'New user created'}]), 201)
    else:
        return make_response(jsonify([{'message': 'Passwords do not match, please try again'}]), 403)


@authorise_bp.route('/login', methods=['POST'])
def login():
    """
    Route to login and generate an time limited authorisation token.

    Returns:
        JSON: JSON carrying a JSON Web Token.
    """
    authorised = request.authorization

    if not authorised or not authorised.username or not authorised.password:
        return make_response(jsonify({'message': "Login details are not recongnised, would you like to sign up?"}), 401)

    existing_user = models.User.query.filter_by(
        username=authorised.username).first()

    if existing_user and check_password_hash(existing_user.password, authorised.password):
        json_token = jwt.encode({"public_id": existing_user.pub_id, "exp": datetime.datetime.utcnow(
        ) + timedelta(minutes=20)}, '$SECRET_KEY', algorithm="HS256")
        return make_response(jsonify({'token': json_token}), 201)
        # jwt.decode(json_token, '$SECRET_KEY', algorithms="HS256")
        # return make_response(jsonify({ json_token.decode("UTF-8")}), 202)
    else:
        return make_response(jsonify({'message': "Login details are not recongnised, try again or would you like to sign up?"}), 401)


@search_bp.route('/', methods=['POST'])
def db_input():
    """
    Route to create a search query.
    Recieves JSON data and then adds a row to the Query table.

    Returns:
        JSON: JSON data containing message query ID, search topic,
        and sentiment value 
    """
    try:
        search_topic = request.json["topic"]
        blocked_words = request.json["blocked-words"]
        search_string = create_search_string(search_topic, blocked_words)
    except KeyError:
        return make_response(jsonify({'message' : 'No Json given'}), 500)
    token = None
    if 'autherisation-token' in request.headers:
        token = request.headers['autherisation-token']

    if token:
        try:
            pub_id = jwt.decode(token, '$SECRET_KEY', algorithms="HS256")
            user = models.User.query.filter_by(
                pub_id=pub_id["public_id"]).first()
            old_query = models.Query.query.filter_by(
                topic=search_string).first()

            if old_query and user:
                database.session.add(old_query)
                old_query.searchers.append(user)
                database.session.commit()

                return make_response(jsonify([{'message': 'Request acknowledged', 'query_id': old_query.id, 'topic': old_query.topic, 'sentiment': old_query.seven_d_sentiment}]), 202)
            elif user:
                query = models.Query(querys=search_string)
                database.session.add(query)
                query.searchers.append(user)
                database.session.commit()
                return make_response(jsonify([{'message': 'Request Recieved', 'query_id': query.id, 'topic': query.topic, 'sentiment': query.seven_d_sentiment}]), 201)
            elif not user:
                return make_response(jsonify([{'message': 'Unrecognised token'}]), 403)
            # try:
            #     query = models.Query(querys=search_string)
            #     database.session.add(query)
            #     query.searchers.append(user)
            #     database.session.commit()

            #     return make_response(jsonify({'message' : 'Request Recieved', 'query_id' : query.id, 'query' : query.topic}), 201)
            # except exc.IntegrityError:
            #     return make_response(jsonify({'message' : 'Request Recieved', 'query_id' : query.id, 'query' : query.topic}), 202)
        except exceptions.ExpiredSignatureError or exceptions.InvalidSignatureError:
            try:
                query = models.Query(querys=search_string)
                database.session.add(query)
                database.session.commit()

                return make_response(jsonify([{'message': 'Token expired, sign in to see reults'}]), 201)
            except exc.IntegrityError:
                return make_response(jsonify([{'message': 'Token expired, sign into to see reult'}]), 202)

        except:
            return make_response(jsonify([{'message': 'Internal server error'}]), 500)
    else:
        old_query = models.Query.query.filter_by(topic=search_string).first()
        try:
            if old_query:
                # reponse = requests.post('http://localhost:7071/api/HttpTrigger1', json={"search-string" : search_string}, headers = {'Content-Type': 'application/json'})
                return make_response(jsonify([{'message': 'Request acknowledged', 'query_id': old_query.id, 'topic': old_query.topic, 'sentiment': old_query.seven_d_sentiment}]), 202)
            else:
                query = models.Query(querys=search_string)
                database.session.add(query)
                database.session.commit()
                # response = requests.post('http://localhost:7071/api/HttpTrigger1', json={"search-string" : search_string}, headers = {'Content-Type': 'application/json'})
                return make_response(jsonify([{'message': 'Request Recieved', 'query_id': query.id, 'topic': query.topic, 'sentiment': query.seven_d_sentiment}]), 201)
    
        except:
            return make_response(jsonify([{'message': 'Internal server error'}]), 500)
            # except exc.IntegrityError:
            #     # old_query = models.Query.query.filter_by(topic=search_string).first()
            #     return make_response(jsonify({'message' : 'Request acknowledged', 'query_id' : old_query.id, 'topic' : old_query.topic}))

# @search_bp.route('/<int:query_id>', methods=['POST'])
# def check_for_results(query_id):
#     query = models.Query.query.filter_by(topic=query_id).first()
#     if query:
#         return make_response(jsonify([{'sentiment' : query.seven_d_sentiment}]), 200)


@search_bp.route('/<int:query_id>', methods=['GET'])
def get_query(query_id):
    """
    Route to return query results associated with a given query ID.

    Args:
        query_id (int): Query object ID.

    Returns:
        JSON: All results of a search, the search topic, and seven day sentiment value.
    """
    if request.method == 'GET':
        query = models.Query.query.filter_by(id=query_id).first()
        if query:
            results = query.query_results
            if len(results) >= 1: #you changed this from > 1 to >= 1
                return make_response(jsonify({'result': [result.to_dict() for result in results], 'topic': query.topic, 'sentiment': query.seven_d_sentiment}), 200)
            else:
                return make_response(jsonify({'result': 0}), 200)
            # return make_response(jsonify([{'sentiment' : query.seven_d_sentiment}]), 200)
        else:
            return make_response(jsonify({'result': 'None', 'sentiment': 'None'}), 200)

    # search_topic = request.json["topic"]
    # blocked_words = request.json["blocked-words"]
    # search_string = create_search_string(search_topic, blocked_words)
    # token = None

    # if 'autherisation-token' in request.headers:
    #     token = request.headers['autherisation-token']

    # if token:
    #     try:
    #         pub_id = jwt.decode(token, '$SECRET_KEY', algorithms="HS256")
    #         user = models.User.query.filter_by(pub_id=pub_id["public_id"]).first()
    #     except exceptions.ExpiredSignatureError or exceptions.InvalidSignatureError:
    #         return make_response(jsonify({'message' : 'Token expired, login to update query'}), 403)

    #     old_query = models.Query.query.filter_by(id=query_id).first()

    #     if request.method == 'PUT':
    #         try:
    #             update_query = models.Query.query.filter_by(topic=search_string).first()

    #             if old_query:
    #                 user.searches.remove(old_query)
    #                 old_query.searchers.remove(user)
    #                 database.session.commit()

    #             if update_query:
    #                 update_query.searchers.append(user)
    #                 database.session.commit()
    #                 return make_response(jsonify({'message' : 'Query updated 1'}), 201)
    #             else:
    #                 new_query = models.Query(querys=search_string)
    #                 new_query.searchers.append(user)
    #                 database.session.commit()
    #                 return make_response(jsonify({'message': 'Query updated 2'}), 201)
    #         except TypeError:
    #             return make_response(jsonify([{'message':'No JSON data given'}]), 500)
    #         except KeyError:
    #             return make_response(jsonify([{'message':'Incomplete JSON fields'}]), 500)
    #         except:
    #             return make_response(jsonify("Internal server error."), 500)

    #     if request.method == 'DELETE':
    #         if old_query:
    #             try:
    #                 old_query.searchers.remove(user)
    #                 return make_response(jsonify({'message': 'Query updated'}), 202)
    #             except:
    #                 return make_response(jsonify("Internal server error."), 500)
    #         else:
    #             return make_response(jsonify("Internal server error."), 500)
    # else:
    #     return make_response(jsonify({'message' : 'Please sign in to update queries.'}), 403)


@search_bp.route('/delete/<int:query_id>', methods=['DELETE'])
@requires_token
def delete_query(user, query_id):
    """
    Route to carryout the deletion of an association between a query and user.

    Args:
        user (User): User object returned from database
        query_id (int): Query object ID

    Returns:
        JSON: JSON data containing a string confirming query has been deleted.
    """
    query = models.Query.query.filter_by(id=query_id).first()
    if query:
        try:
            query.searchers.remove(user)
            database.session.commit()
            return make_response(jsonify([{'message': 'Query removed'}]), 200)
        except:
            return make_response(jsonify([{'message': 'Internal server error'}]), 500)
    else:
        return make_response(jsonify([{'message': 'Query does not exist with ID'}]), 404)


@search_bp.route('/update/<int:query_id>', methods=['PUT'])
@requires_token
def update_query(user, query_id):
    """
    Updates a stored query associated with a user. 
    This is done by removing association betwe Query and User objects
    and creating a new Query object and associating it with the User.

    Args:
        user (User): User object returned from database
        query_id (int): Query object ID

    Returns:
        JSON: JSON containing updated Query object ID
    """
    try:
        search_topic = request.json["topic"]
        blocked_words = request.json["blocked-words"]
        search_string = create_search_string(search_topic, blocked_words)
    except TypeError:
        return make_response(jsonify([{'message': 'JSON not given'}]), 500)

    old_query = models.Query.query.filter_by(id=query_id).first()
    updated_query = models.Query.query.filter_by(
        topic=search_string).first()
    try:
        if old_query:
            user.searches.remove(old_query)
            old_query.searchers.remove(user)
            database.session.commit()
        else:
            return make_response(
                jsonify([{'message': 'Query does not exist for given ID'}]), 404)

        if updated_query:
            updated_query.searchers.append(user)
            database.session.commit()
            return make_response(jsonify([{'result': updated_query.id}]), 201)
        else:
            new_query = models.Query(querys=search_string)
            new_query.searchers.append(user)
            database.session.commit()
            return make_response(jsonify([{'result': new_query.id}]), 201)
    except KeyError:
        return make_response(jsonify([{'message': 'Insufficient JSON'}]), 500)
    except:
        return make_response(jsonify([{'message': "Internal server error."}]), 500)


@saved_bp.route('/<int:queryresult_id>', methods=['POST'])
@requires_token
def save_article(user, queryresult_id):
    """
    Route to create an association between User object and 
    QueryResult object.

    Args:
        user (User): User object returned from database
        queryresult_id (_type_): QueryResult object ID

    Returns:
        JSON: JSON containing String if QueryResult object has been associated with user.
    """

    result = models.QueryResult.query.filter_by(id=queryresult_id).first()
    if result:
        user.saved_article.append(result)
        database.session.commit()

        return make_response(jsonify([{'message': 'Added'}]), 201)
    else:
        return make_response(jsonify([{'message': 'Query result does not exist with given id'}], 200))
# except exceptions.ExpiredSignatureError or exceptions.InvalidSignatureError:
#         return make_response(jsonify({'message' : 'Token expired, please sign in to save articles'}), 403)
#     else:
#         return make_response(jsonify({'message' : "Please sign in to save articles"}), 403)


@saved_bp.route('/delete/<int:queryresult_id>', methods=['DELETE'])
@requires_token
def delete_article(user, queryresult_id):
    """
    Route to delete association between User Object and QueryResult object

    Args:
        user (User): User object returned from database
        queryresult_id (int): QueryResult object ID

    Returns:
        JSON: JSON string containing confirmation assocation has been removed
    """
    query = models.QueryResult.query.filter_by(id=queryresult_id).first()
    if query:
        try:
            user.saved_article.remove(query)
            database.session.commit()
            return make_response(jsonify([{'message': 'Result removed'}]), 200)
        except:
            return make_response(jsonify([{'message': 'Internal server error'}]), 500)
    elif not query:
        return make_response(jsonify([{'message': 'Query result does not exist'}]), 404)
    else:
        return make_response(jsonify([{'message': 'Method not allowed'}]), 405)


@saved_bp.route('/get_saved_articles', methods=['GET'])
@requires_token
def get_saved_articles(user):
    """
    Route to resturn all saved QueryResult object associated with a User object.

    Args:
        user (User): User object returned from database

    Returns:
        JSON: JSON data containing list of all QueryResult objects associated with a User object.
    """
    # token = request.json["token"]
    # if len(token) > 0:
    #     try:
    #         pub_id = jwt.decode(token, '$SECRET_KEY', algorithms="HS256")
    #         user = models.User.query.filter_by(pub_id=pub_id["public_id"]).first()
    articles = user.saved_article
    return make_response(jsonify([{'saved': [article.to_dict() for article in articles]}]), 200)
    #     except exceptions.ExpiredSignatureError or exceptions.InvalidSignatureError:
    #         return make_response(jsonify({'message' : "Please sign in to see saved articles"}), 403)

    # else:
    #     return make_response(jsonify({'message' : "Please sign in to see saved articles"}), 403)
