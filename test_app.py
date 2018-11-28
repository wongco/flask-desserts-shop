from unittest import TestCase
from app import app
from desserts import dessert_list, Dessert
from flask import session


class FlaskTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        """reset the dessert_list after each test.
        Only an issue because we don't know about databases yet."""

        cookie = Dessert(1, "Chocolate chip cookie",
                         "C is for cookie, that's good enough for me", 200)
        sundae = Dessert(2, "Banana split",
                         "I'm going to eat all of my feelings", 600)
        donut = Dessert(3, "Glazed Donut", "Perfect with a cup of coffee", 300)
        dessert_list.desserts = [cookie, sundae, donut]
        dessert_list.next_id = 4

    def test_homepage(self):
        """Make sure homepage has correct routing information"""

        with self.client:
            response = self.client.get('/')
            # test that the status code is a 200
            self.assertEqual(response.status_code, 200)
            # test that there's a table in the response data
            self.assertIn(b'table', response.data)
            # test that the description for each endpoint is in the response data
            # e.g. 'JSON data of all desserts' should be in the response data,
            # 'Adds a new dessert to our list' should be in the response data,
            # etc.
            self.assertIn(
                b'JSON data of all desserts', response.data,
                "Don't forget to make a GET /desserts Endpoint Description")
            self.assertIn(
                b'Adds a new dessert to our list (returns data on the new dessert)',
                response.data,
                "Don't forget to make a POST /desserts Endpoint Description")
            self.assertIn(
                b'JSON data on a single dessert', response.data,
                "Don't forget to make a GET /desserts/<id> Endpoint Description"
            )
            self.assertIn(
                b'Update an existing dessert (returns data on the updated dessert)',
                response.data,
                "Don't forget to make a PATCH /desserts/<id> Endpoint Description"
            )
            self.assertIn(
                b'Removes a dessert from our list (returns data on the deleted dessert)',
                response.data,
                "Don't forget to make a DELETE /desserts/<id> Endpoint Description"
            )

    def test_get_all_desserts(self):
        """Make sure that the get request succeeds"""
        response = self.client.get('/desserts')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json, dessert_list.serialize())

    def test_add_dessert(self):
        """Make sure that the post request succeeds"""

        response = self.client.post('/desserts', json={
            "name": "Cookie",
            "description": "yummy",
            "calories": 3
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Cookie')
        self.assertEqual(response.json['description'], 'yummy')
        self.assertEqual(response.json['calories'], 3)

    def test_get_specific_dessert(self):
        """Make sure that the post request succeeds"""

        response = self.client.get('/desserts/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Chocolate chip cookie')
        self.assertEqual(response.json['description'],
                         "C is for cookie, that's good enough for me")
        self.assertEqual(response.json['calories'], 200)
        response = self.client.get('/desserts/7')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Dessert not found.', response.data)

    def test_patch_desserts(self):
        """Make sure that the patch request succeeds"""

        response = self.client.patch('/desserts/1', json={
            "name": "HotCookie",
            "description": "Delicious",
            "calories": 40
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'HotCookie')
        self.assertEqual(response.json['description'], 'Delicious')
        self.assertEqual(response.json['calories'], 40)
        response = self.client.patch('/desserts/7', json={
            "name": "HotCookie",
            "description": "Delicious",
            "calories": 40
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Dessert not found.', response.data)

    def test_delete_desserts(self):
        """Make sure that the delete request succeeds"""

        response = self.client.delete('/desserts/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Chocolate chip cookie')
        self.assertEqual(response.json['description'],
                         "C is for cookie, that's good enough for me")
        self.assertEqual(response.json['calories'], 200)
        response = self.client.delete('/desserts/1')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Dessert not found.', response.data)

    def test_get_total_calories(self):
        """Make sure that the total calories request succeeds"""

        with self.client:
            response = self.client.post('/desserts/1/eat')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(session.get('total_calories', 0), 200)
            response = self.client.post('/desserts/7/eat')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Dessert not found.', response.data)
            response = self.client.post('/desserts/2/eat')
            self.assertEqual(session.get('total_calories', 0), 800)
            response = self.client.post('/desserts/3/eat')
            self.assertEqual(session.get('total_calories', 0), 1100)
