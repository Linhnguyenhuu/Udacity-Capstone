import unittest
import json
from api import app
from src.database.models import db

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            # create all tables
            self.db.create_all()

        # Get available authentication tokens
        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        assistant_role = self.auth["roles"]["Casting Assistant"]["jwt_token"]
        director_role = self.auth["roles"]["Casting Director"]["jwt_token"]
        producer_role = self.auth["roles"]["Executive Producer"]["jwt_token"]
        self.auth_headers = {
            "Casting Assistant": f'Bearer {assistant_role}',
            "Casting Director": f'Bearer {director_role}',
            "Executive Producer": f'Bearer {producer_role}'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass
    

    """
    Write at least one test for each test for successful operation and for expected errors.
    And at least two tests of RBAC for each role.
    """
    # get all movies successfully
    def test_get_movies(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/movies', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["movies"])
        
    # get movie by id successfully
    def test_get_movie_by_id(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/movies/1', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    # get movie by id failed
    def test_get_movie_by_id_failed_404(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/movies/1000', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    # create a new movie successfully
    def test_create_movies(self):
        auth_header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        
        movie = {
            "title": "Pinocchio",
            "release_date": "1940-01-01 00:00:00"
        }
        res = self.client().post(f'/movies',
                                json=movie, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    # create a new movie failed 403
    def test_create_movies_fail_403(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        
        movie = {
            "title": "Pinocchio",
            "release_date": "1940-01-01 00:00:00"
        }
        res = self.client().post(f'/movies',
                                json=movie, headers=auth_header)
        
        self.assertEqual(res.status_code, 403)
        
    # create a new movie failed 422
    def test_create_movies_fail_422(self):
        auth_header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        
        movie = {
            "title": ""
        }
        res = self.client().post(f'/movies',
                                json=movie, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "request cannot be processed")
        
    # search movie successfully
    def test_search_movies(self):
        searTerm = {
            "searchTerm": "Pinocchio",
        }
        res = self.client().post(f'/movies/search', json=searTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    # search movie failed 404
    def test_search_movies_fail_404(self):
        searTerm = {
            "searchTerm": "test",
        }
        res = self.client().post(f'/movies/search', json=searTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    # update a movie successfully
    def test_update_movie(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        
        movie = {
            "title": "Victory Through Air Power",
            "release_date": "1943-01-01 00:00:00"
        }
        res = self.client().patch(f'/movies/1',
                                json=movie, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 1)
        
    # update a movie failed 403
    def test_update_movie_failed_403(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        
        movie = {
            "title": "Victory Through Air Power",
            "release_date": "1943-01-01 00:00:00"
        }
        res = self.client().patch(f'/movies/1',
                                json=movie, headers=auth_header)
        self.assertEqual(res.status_code, 403)
        
    # update a movie failed 404
    def test_update_movie_fail_404(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        
        movie = {
            "title": "Victory Through Air Power",
            "release_date": "1943-01-01 00:00:00"
        }
        res = self.client().patch(f'/movies/1000',
                                json=movie, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    # delete a movie successfully
    def test_delete_movie(self):
        auth_header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        
        res = self.client().delete(f'/movies/1', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 1)
        
    # delete a movie failed 404
    def test_delete_movie_fail_404(self):
        auth_header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        
        res = self.client().delete(f'/movies/1000', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    # delete a movie failed 401
    def test_delete_movie_fail_401(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        
        res = self.client().delete(f'/movies/2', headers=auth_header)
        self.assertEqual(res.status_code, 403)

    # get all actors successfully
    def test_get_actors(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/actors', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["actors"])
        
    # get actor by id successfully
    def test_get_actor_by_id(self):
        auth_header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().get('/actors/1', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    # get actor by id failed
    def test_get_actor_by_id_failed_404(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/actors/1000', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    # create a new actor successfully
    def test_create_actors(self):
        auth_header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        
        actor = {
            "name": "Lil Nas X",
            "age": "30",
            "gender": "male"
        }
        res = self.client().post(f'/actors',
                                json=actor, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    # create a new actor failed 422
    def test_create_actors_fail_422(self):
        auth_header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        
        actor = {
            "name": ""
        }
        res = self.client().post(f'/actors',
                                json=actor, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "request cannot be processed")
        
    # create a new actor failed 403
    def test_create_actors_fail_403(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        
        actor = {
            "name": "Lil Nas X",
            "age": "30",
            "gender": "male"
        }
        res = self.client().post(f'/actors',
                                json=actor, headers=auth_header)
        self.assertEqual(res.status_code, 403)
        
    # search actor successfully
    def test_search_actors(self):
        searTerm = {
            "searchTerm": "Oprah Winfrey",
        }
        res = self.client().post(f'/actors/search', json=searTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    # search actor failed
    def test_search_actors_fail_404(self):
        searTerm = {
            "searchTerm": "test",
        }
        res = self.client().post(f'/actors/search', json=searTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    # update a actor successfully
    def test_update_actor(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        
        actor = {
            "name": "Oprah Winfrey",
            "age": "60",
            "gender": "female"
        }
        res = self.client().patch(f'/actors/1',
                                json=actor, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 1)
        
    # update a actor failed
    def test_update_actor_fail_404(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        
        actor = {
            "name": "Oprah Winfrey",
            "age": "60",
            "gender": "female"
        }
        res = self.client().patch(f'/actors/1000',
                                json=actor, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    # update a actor failed 403
    def test_update_actor_fail_403(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        
        actor = {
            "name": "Oprah Winfrey",
            "age": "60",
            "gender": "female"
        }
        res = self.client().patch(f'/actors/1',
                                json=actor, headers=auth_header)
        self.assertEqual(res.status_code, 403)
        
    # delete a actor successfully
    def test_delete_actor(self):
        auth_header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        
        res = self.client().delete(f'/actors/3', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 3)
        
    # delete a actor failed 404
    def test_delete_actor_fail_404(self):
        auth_header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        
        res = self.client().delete(f'/actors/1000', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # delete a actor failed 403
    def test_delete_actor_fail_403(self):
        auth_header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        
        res = self.client().delete(f'/actors/1', headers=auth_header)
        self.assertEqual(res.status_code, 403)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()