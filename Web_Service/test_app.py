import json
import unittest
from base64 import b64encode

import dateparser

import models
from app import create_app, database


class TestWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_config = {
            'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
            'TESTING': True,
            'SECRET_KEY': '$SECRET_KEY'
        }
        cls.app = create_app(test_config)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self) -> None:
        database.create_all()
        database.session.commit()

    def tearDown(self) -> None:
        database.drop_all()
        database.session.commit()

    def test_register(self):
        # Test registeration denied if passwords do not match.
        json_data_01 = {"username": "john", "email": "john.email@student.com",
                        "password": "password", "confirmed-password": "wrongpassword"}
        post = self.client.post('/authorisation/register', json=json_data_01)
        self.assertEqual(post.status_code, 403)

        # Test registration confirms if passwords do match.
        json_data_02 = {"username": "john", "email": "john.email@student.com",
                        "password": "password", "confirmed-password": "password"}
        post02 = self.client.post('/authorisation/register', json=json_data_02)
        self.assertEqual(post02.status_code, 201)

        # Test registration fails when user already exists with details.
        json_data_02 = {"username": "john", "email": "john.email@student.com",
                        "password": "password", "confirmed-password": "password"}
        post02 = self.client.post('/authorisation/register', json=json_data_02)
        self.assertEqual(post02.status_code, 409)

    def test_login(self):
        # Test login with no authorisation details.
        post_no_auth = self.client.post('/authorisation/login')
        self.assertEqual(post_no_auth.status_code, 401)

        # Test login with unrecognised user details.
        post_with_auth = self.client.post('/authorisation/login', headers={
                                          'Authorization': 'Basic ' + b64encode(b"john:password").decode('utf-8')})
        self.assertEqual(post_with_auth.status_code, 401)

        # Create user
        json_data_01 = {"username": "john", "email": "john.email@student.com",
                        "password": "password", "confirmed-password": "password"}
        post = self.client.post('/authorisation/register', json=json_data_01)
        self.assertEqual(post.status_code, 201)

        # Test for successful login with registered user.
        new_post = self.client.post('/authorisation/login', headers={
                                    'Authorization': 'Basic ' + b64encode(b"john:password").decode('utf-8')})
        self.assertEqual(new_post.status_code, 201)

    def test_post_query(self):

        # Post anonymous query.
        json_data_01 = {"topic": "truss", "blocked-words": ['leadership']}
        post01 = self.client.post('/search/', json=json_data_01)
        self.assertEqual(post01.status_code, 201)
        self.assertEqual(post01.json, [
                         {'message': 'Request Recieved', 'query_id': 1, 'topic': 'truss -leadership', 'sentiment': None}])
        post02 = self.client.post('/search/', json=json_data_01)
        self.assertEqual(post02.status_code, 202)
        self.assertEqual(post02.json, [{'message': 'Request acknowledged',
                         'query_id': 1, 'topic': 'truss -leadership', 'sentiment': None}])

        # Test to see if similar input create different query.
        json_data_02 = {"topic": "rabbit", "blocked-words": []}
        post03 = self.client.post('/search/', json=json_data_02)
        self.assertEqual(post03.status_code, 201)
        self.assertEqual(post03.json, [
                         {'message': 'Request Recieved', 'query_id': 2, 'topic': 'rabbit', 'sentiment': None}])

        # Create user
        user_data = {"username": "john", "email": "john.email@student.com",
                     "password": "password", "confirmed-password": "password"}
        reg_post = self.client.post('/authorisation/register', json=user_data)
        self.assertEqual(reg_post.status_code, 201)

        # Test for successful login with registered user.
        auth_post = self.client.post('/authorisation/login', headers={
                                     'Authorization': 'Basic ' + b64encode(b"john:password").decode('utf-8')})
        self.assertEqual(auth_post.status_code, 201)

        token = auth_post.json['token']
        json_data_03 = {"topic": "sunak", "blocked-words": []}
        post04 = self.client.post(
            '/search/', json=json_data_03, headers={'autherisation-token': token})
        self.assertEqual(post04.json, [
                         {'message': 'Request Recieved', 'query_id': 3, 'topic': 'sunak', 'sentiment': None}])
        post05 = self.client.post(
            '/search/', json=json_data_03, headers={'autherisation-token': token})
        self.assertEqual(post05.json, [
                         {'message': 'Request acknowledged', 'query_id': 3, 'topic': 'sunak', 'sentiment': None}])

    def test_get_results(self):
        # Create a query.
        json_data_01 = {"topic": "shinty", "blocked-words": ['leadership']}
        post01 = self.client.post('/search/', json=json_data_01)
        self.assertEqual(post01.status_code, 201)

        # Query exists with no results.
        query_id = post01.json[0]['query_id']
        get01 = self.client.get(f'/search/{query_id}')
        self.assertEqual(get01.status_code, 200)
        self.assertEqual(get01.json['result'], 0)

        # Create result and associate it with the query.
        result = models.QueryResult(
            publisher="Shinty boys",
            headline="total maddness in the world of Shinty",
            description="Domhnall will not return. A legend lost. Latha uabhasachd airson a' gheama.",
            url="https://www.thecamanboys.co.uk",
            publish_date=dateparser.parse("10/07/2022"),
            sentiment=-0.127457)

        query = models.Query.query.filter_by(id=query_id).first()

        database.session.add(result)
        result.searched_querys.append(query)
        database.session.commit()

        # Query exist with results
        get02 = self.client.get(f'/search/{query_id}')
        self.assertEqual(get01.status_code, 200)
        found_publisher = get02.json['result'][0]['publisher']
        self.assertEqual(found_publisher, 'Shinty boys')

    def test_delete_query(self):
        # Create user
        user_data = {"username": "john", "email": "john.email@student.com",
                     "password": "password", "confirmed-password": "password"}
        reg_post = self.client.post('/authorisation/register', json=user_data)
        self.assertEqual(reg_post.status_code, 201)

        # Login.
        log_post = self.client.post('/authorisation/login', headers={
            'Authorization': 'Basic ' + b64encode(b"john:password").decode('utf-8')})
        self.assertEqual(log_post.status_code, 201)

        # Delete a query without a token.
        post01 = self.client.delete('/search/delete/1')
        self.assertEqual(post01.status_code, 403)

        # Create a query.
        token = log_post.json['token']
        json_data_01 = {"topic": "shinty", "blocked-words": ['leadership']}
        post02 = self.client.post(
            '/search/', json=json_data_01, headers={'autherisation-token': token})
        self.assertEqual(post02.status_code, 201)

        # Delete a query with a token.
        post02 = self.client.delete(
            '/search/delete/1', headers={'autherisation-token': token})
        self.assertEqual(post02.status_code, 200)

        # Delete query that does not exist.
        post03 = self.client.delete(
            '/search/delete/2', headers={'autherisation-token': token})
        self.assertEqual(post03.status_code, 404)

        # User trys to delete a query not associated with them
        token = log_post.json['token']
        json_data_01 = {"topic": "iomain", "blocked-words": ['leadership']}
        post04 = self.client.post('/search/', json=json_data_01)
        self.assertEqual(post04.status_code, 201)

        post05 = self.client.delete(
            '/search/delete/2', headers={'autherisation-token': token})
        self.assertEqual(post05.status_code, 500)

    def test_homepage(self):
        # Anonymous user access the application, has no saved queries
        get01 = self.client.get('/home/')
        self.assertEqual(get01.json[0]['queries'], 0)

        # Create user
        user_data = {"username": "john", "email": "john.email@student.com",
                     "password": "password", "confirmed-password": "password"}
        reg_post = self.client.post('/authorisation/register', json=user_data)
        self.assertEqual(reg_post.status_code, 201)

        # Login.
        log_post = self.client.post('/authorisation/login', headers={
            'Authorization': 'Basic ' + b64encode(b"john:password").decode('utf-8')})
        self.assertEqual(log_post.status_code, 201)

        # Create a query.
        token = log_post.json['token']
        json_data_01 = {"topic": "shinty", "blocked-words": ['leadership']}
        post02 = self.client.post(
            '/search/', json=json_data_01, headers={'autherisation-token': token})
        self.assertEqual(post02.status_code, 201)

        # Check the query has been added to the users queries
        get02 = self.client.get(
            '/home/', headers={'autherisation-token': token})
        self.assertEqual(get02.status_code, 200)
        self.assertEqual(get02.json['queries'][0], {
                         '7 day sentiment': None, 'id': 1, 'topic': 'shinty -leadership'})
        # print(get02.json['queries'][0])

        # Delete query associated with the user
        delete01 = self.client.delete(
            '/search/delete/1', headers={'autherisation-token': token})
        self.assertEqual(delete01.status_code, 200)

        # Check to ensure the query is no longer associated with user.
        get03 = self.client.get(
            '/home/', headers={'autherisation-token': token})
        self.assertEqual(get03.status_code, 200)
        self.assertEqual(len(get03.json['queries']), 0)

    def test_save_queries(self):
        # Create user
        user_data = {"username": "john", "email": "john.email@student.com",
                     "password": "password", "confirmed-password": "password"}
        reg_post = self.client.post('/authorisation/register', json=user_data)
        self.assertEqual(reg_post.status_code, 201)

        # Login.
        log_post = self.client.post('/authorisation/login', headers={
            'Authorization': 'Basic ' + b64encode(b"john:password").decode('utf-8')})
        self.assertEqual(log_post.status_code, 201)

        # Save an article without a token.
        post01 = self.client.post('/saved/1')
        self.assertEqual(post01.status_code, 403)

        # Create a query.
        token = log_post.json['token']
        json_data_01 = {"topic": "shinty", "blocked-words": ['leadership']}
        post02 = self.client.post(
            '/search/', json=json_data_01, headers={'autherisation-token': token})
        self.assertEqual(post02.status_code, 201)

        query_id = post02.json[0]['query_id']

        # Create result and associate it with the query.
        result = models.QueryResult(
            publisher="Shinty boys",
            headline="total maddness in the world of Shinty",
            description="Domhnall will not return. A legend lost. Latha uabhasachd airson a' gheama.",
            url="https://www.thecamanboys.co.uk",
            publish_date=dateparser.parse("10/07/2022"),
            sentiment=-0.127457)

        query = models.Query.query.filter_by(id=query_id).first()

        database.session.add(result)
        result.searched_querys.append(query)
        database.session.commit()

        # Save an article with a token.
        post03 = self.client.post(
            '/saved/1', headers={'autherisation-token': token})
        self.assertEqual(post03.status_code, 201)

        # Save an article that does not exist.
        post04 = self.client.post(
            '/saved/5', headers={'autherisation-token': token})
        self.assertEqual(post04.status_code, 200)

        # Get all saved articles
        get01 = self.client.get(
            '/saved/get_saved_articles', headers={'autherisation-token': token})
        len_of_saved = len(get01.json[0]['saved'])
        self.assertEqual(get01.status_code, 200)
        self.assertEqual(len_of_saved, 1)

    def test_delete_saved_article(self):
        # Create user
        user_data = {"username": "john", "email": "john.email@student.com",
                     "password": "password", "confirmed-password": "password"}
        reg_post = self.client.post('/authorisation/register', json=user_data)
        self.assertEqual(reg_post.status_code, 201)

        # Login.
        log_post = self.client.post('/authorisation/login', headers={
            'Authorization': 'Basic ' + b64encode(b"john:password").decode('utf-8')})
        self.assertEqual(log_post.status_code, 201)

        # Delete saved article without a token.
        post01 = self.client.delete('/saved/delete/1')
        self.assertEqual(post01.status_code, 403)

        # Create a query.
        token = log_post.json['token']
        json_data_01 = {"topic": "shinty", "blocked-words": ['leadership']}
        post02 = self.client.post(
            '/search/', json=json_data_01, headers={'autherisation-token': token})
        self.assertEqual(post02.status_code, 201)

        query_id = post02.json[0]['query_id']

        # Create result and associate it with the query.
        result = models.QueryResult(
            publisher="Shinty boys",
            headline="total maddness in the world of Shinty",
            description="Domhnall will not return. A legend lost. Latha uabhasachd airson a' gheama.",
            url="https://www.thecamanboys.co.uk",
            publish_date=dateparser.parse("10/07/2022"),
            sentiment=-0.127457)

        query = models.Query.query.filter_by(id=query_id).first()

        database.session.add(result)
        result.searched_querys.append(query)
        database.session.commit()

        # Save an article with a token.
        post03 = self.client.post(
            '/saved/1', headers={'autherisation-token': token})
        self.assertEqual(post03.status_code, 201)

        # Delete an article with a token.
        post04 = self.client.delete(
            '/saved/delete/1', headers={'autherisation-token': token})
        self.assertEqual(post04.status_code, 200)
        self.assertEqual(post04.json[0]['message'], 'Result removed')

        # Delete an article  not associated with user.
        post05 = self.client.delete(
            '/saved/delete/1', headers={'autherisation-token': token})
        self.assertEqual(post05.status_code, 500)
        self.assertEqual(post05.json[0]['message'], 'Internal server error')

        # Delete an article that does not exist.
        post06 = self.client.delete(
            '/saved/delete/0', headers={'autherisation-token': token})
        self.assertEqual(post06.status_code, 404)
        self.assertEqual(post06.json[0]['message'],
                         'Query result does not exist')

        # Get all saved articles
        get01 = self.client.get(
            '/saved/get_saved_articles', headers={'autherisation-token': token})
        len_of_saved = len(get01.json[0]['saved'])
        self.assertEqual(get01.status_code, 200)
        self.assertEqual(len_of_saved, 0)

    def test_get_saved_articles(self):
        # Create user
        user_data = {"username": "john", "email": "john.email@student.com",
                     "password": "password", "confirmed-password": "password"}
        reg_post = self.client.post('/authorisation/register', json=user_data)
        self.assertEqual(reg_post.status_code, 201)

        # Login.
        log_post = self.client.post('/authorisation/login', headers={
                                    'Authorization': 'Basic ' + b64encode(b"john:password").decode('utf-8')})
        self.assertEqual(log_post.status_code, 201)

        # Delete saved article without a token.
        post01 = self.client.delete('/saved/delete/1')
        self.assertEqual(post01.status_code, 403)

        # Create a query.
        token = log_post.json['token']
        json_data_01 = {"topic": "shinty", "blocked-words": ['leadership']}
        post02 = self.client.post(
            '/search/', json=json_data_01, headers={'autherisation-token': token})
        self.assertEqual(post02.status_code, 201)

        query_id = post02.json[0]['query_id']

        # Create result and associate it with the query.
        result = models.QueryResult(
            publisher="Shinty boys",
            headline="total maddness in the world of Shinty",
            description="Domhnall will not return. A legend lost. Latha uabhasachd airson a' gheama.",
            url="https://www.thecamanboys.co.uk",
            publish_date=dateparser.parse("10/07/2022"),
            sentiment=-0.127457)

        query = models.Query.query.filter_by(id=query_id).first()

        database.session.add(result)
        result.searched_querys.append(query)
        database.session.commit()

        # Save an article with a token.
        post03 = self.client.post(
            '/saved/1', headers={'autherisation-token': token})
        self.assertEqual(post03.status_code, 201)

        # Get all saved articles
        get01 = self.client.get(
            '/saved/get_saved_articles', headers={'autherisation-token': token})
        self.assertEqual(get01.status_code, 200)
        found_publisher = get01.json[0]['saved'][0]['publisher']
        len_of_saved = len(get01.json[0]['saved'])
        self.assertEqual(found_publisher, 'Shinty boys')
        self.assertEqual(len_of_saved, 1)


if __name__ == "__main__":
    unittest.main()
