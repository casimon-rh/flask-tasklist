"""Main test"""

import unittest
import json
from app import create_app, BD_


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Borabora for vacation'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            BD_.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps login a test user"""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/bucketlists/',
                                 headers=dict(Authorization="Bearer "+access_token), data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/bucketlists/',
                                 headers=dict(Authorization="Bearer "+access_token), data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/bucketlists/', headers=dict(Authorization="Bearer "+access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        _rv = self.client().post('/bucketlists/',
                                 headers=dict(
                                     Authorization="Bearer "+access_token),
                                 data=self.bucketlist)
        self.assertEqual(_rv.status_code, 201)
        result_in_json = json.loads(
            _rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer "+access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def test_bucketlist_can_be_edited(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        """Test API can edit an existing bucketlist. (PUT request)"""
        _rv = self.client().post(
            '/bucketlists/',
            headers=dict(Authorization="Bearer "+access_token),
            data={'name': 'Eat, poop and love'})
        self.assertEqual(_rv.status_code, 201)
        # get the json with the bucketlist
        results = json.loads(_rv.data.decode())

        _rv = self.client().put(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer "+access_token),
            data={
                "name": "Dont just eat, but also poop and love :-)"
            })
        self.assertEqual(_rv.status_code, 200)
        results = self.client().get('/bucketlists/{}'.format(results['id']),
                                    headers=dict(Authorization="Bearer "+access_token))
        self.assertIn('Dont just eat', str(results.data))

    def test_bucketlist_deletion(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        """Test API can delete an existing bucketlist. (DELETE request)."""
        _rv = self.client().post(
            '/bucketlists/',
            headers=dict(Authorization="Bearer "+access_token),
            data={'name': 'Eat, poop and love'})
        self.assertEqual(_rv.status_code, 201)
        results = json.loads(_rv.data.decode())
        res = self.client().delete(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer "+access_token))
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer "+access_token))
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            BD_.session.remove()
            BD_.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
