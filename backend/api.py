import sys
from flask import (
    Flask, 
    request, 
    abort, 
    jsonify
)
from flask_cors import CORS
from src.database.models import setup_db, Movie, Actor
from src.auth.auth import AuthError, requires_auth

movies_PER_PAGE = 10

# pagination
def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * movies_PER_PAGE
    end = start + movies_PER_PAGE
        
    movies = [movie.format() for movie in selection]
    current_movies = movies[start:end]
        
    return current_movies


#----------------------------------------------------------------------------#
# Init app.
#----------------------------------------------------------------------------#


# Create and configure the app
app = Flask(__name__)
setup_db(app)

# Set up CORS. Allow '*' for origins. 
CORS(app) 

# Use the after_request decorator to set Access-Control-Allow
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add("Access-Control-Allow-Origin", "*")
        
    return response

"""
Home page
"""
@app.route("/")
def index():
    return jsonify({
        "message": "Welcome to capstone project"
    })

"""
CRUD for Movie
"""

# Create an endpoint to handle GET requests for movies
@app.route("/movies")
@requires_auth('get:movies')
def get_movies(payload):
    try:
        # get all movies
        selection = Movie.query.order_by(Movie.id).all()
    
        # paging 10 movies per page
        current_movies = paginate(request, selection)
    
        # not found error
        if not current_movies:
            abort(404)
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
        'success': True,
        'movies': current_movies
    })
    
    
# Create an endpoint to GET movie using movie id
@app.route("/movies/<int:id>")
@requires_auth('get:movie')
def get_movie_by_id(payload, id):      
    try:
        # get movie by id
        movie = Movie.query.filter_by(id=id).one_or_none()
        
        # not found error
        if not movie:
            abort(404)
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
            'success': True,
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date,
        })

# Create an endpoint to POST a new movie
@app.route("/movies", methods=['POST'])
@requires_auth('post:movies')
def create_new_movie(payload):
    # get the input value
    req = request.get_json()
    title = req.get('title')
    release_date = req.get('release_date')
    
    # validate input
    if (title is (None or "")) or (release_date is (None or "")):
        abort(422)  
    try:
        # insert new movie
        movie = Movie(
            title=title,
            release_date=release_date
        )
        movie.insert()
    except AuthError as auth_error:
        raise auth_error
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
            'success': True,
            'created': movie.id
        }), 201

# Create a POST endpoint to get movies based on a search term.
@app.route('/movies/search', methods=['POST'])
def search_movies():
    try:
        # get user's input
        body = request.get_json()
        search_input = body.get('searchTerm')
        
        # get all movies have phrase that user searching
        selection = Movie.query.filter(Movie.title.ilike(f'%{search_input}%')).all()
        if len(selection) != 0:
            search_movies = paginate(request, selection)
        else:
            abort(404)
            
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
                "success": True,
                "movies": search_movies
            })
    
    
@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, id):
    req = request.get_json()
    try:
        # get movie by id
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        # if movie with <id> is not found, return 404 error
        if movie is None:
            abort(404)
        
        # get user's input
        req_title = req.get('title')
        req_release_date = req.get('release_date')
        
        # validate input
        if (req_title, req_release_date) is (None or ""):
            abort(422)
        # update a movie
        movie.title=req_title,
        movie.release_date=req_release_date
        movie.update()
    
    except AuthError as auth_error:
        raise auth_error
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
            "success": True, 
            "updated": movie.id
        }), 200


# Create an endpoint to DELETE movie using a movie ID.
@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, id):
    try:
        # get movie by id
        movie = Movie.query.filter_by(id=id).one_or_none()
        
        # Current movie does not exist
        if movie is None:
            abort(404)
        
        # delete current movie
        movie.delete()
    except AuthError as auth_error:
        raise auth_error
    except Exception as e:
        print(sys.exc_info())
        raise e
        
    return jsonify({
            'success': True,
            'deleted': id
        }), 200


"""
CRUD for Actor
"""

# Create an endpoint to handle GET requests for actors
@app.route("/actors")
@requires_auth('get:actors')
def get_actors(payload):
    try:
        # get all actors
        selection = Actor.query.order_by(Actor.id).all()
    
        # paging 10 actors per page
        current_actors = paginate(request, selection)
    
        # not found error
        if not current_actors:
            abort(404)
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
        'success': True,
        'actors': current_actors
    })
    
    
# Create an endpoint to GET actor using actor id
@app.route("/actors/<int:id>")
@requires_auth('get:actor')
def get_actor_by_id(payload, id):      
    try:
        # get actor by id
        actor = Actor.query.filter_by(id=id).one_or_none()
        
        # not found error
        if not actor:
            abort(404)
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
            'success': True,
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender
        })

# Create an endpoint to POST a new actor
@app.route("/actors", methods=['POST'])
@requires_auth('post:actors')
def create_new_actor(payload):
    # get the input value
    input = request.get_json()
    name = input.get('name')
    age = input.get('age')
    gender = input.get('gender')
    
    # validate input
    if (name is (None or "")) or (age is (None or "")) or (gender is (None or "")):
        abort(422)
    try:
        # insert new actor
        actor = Actor(
            name=name,
            age=age,
            gender=gender
        )
        actor.insert()
    except AuthError as auth_error:
        raise auth_error
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
            'success': True,
            'created': actor.id
        }), 201

# Create a POST endpoint to get actors based on a search term.
@app.route('/actors/search', methods=['POST'])
def search_actors():
    try:
        # get user's input
        body = request.get_json()
        search_input = body.get('searchTerm')
        
        # get all actors have phrase that user searching
        selection = Actor.query.filter(Actor.name.ilike(f'%{search_input}%')).all()
        if len(selection) != 0:
            search_actors = paginate(request, selection)
        else:
            abort(404)
            
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
                "success": True,
                "actors": search_actors
            })
    
    
@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, id):
    req = request.get_json()
    try:
        # get actor by id
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        # if actor with <id> is not found, return 404 error
        if actor is None:
            abort(404)
        
        # get user's input
        req_name = req.get('name')
        req_age = req.get('age')
        req_gender = req.get('gender')
        
        # validate input
        if (req_name, req_age, req_gender) is (None or ""):
            abort(422)
        # update a actor
        actor.name=req_name
        actor.age=req_age
        actor.gender=req_gender
        actor.update()
    
    except AuthError as auth_error:
        raise auth_error
    except Exception as e:
        print(sys.exc_info())
        raise e
    
    return jsonify({
            "success": True, 
            "updated": actor.id
        }), 200


# Create an endpoint to DELETE actor using a actor ID.
@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, id):
    try:
        # get actor by id
        actor = Actor.query.filter_by(id=id).one_or_none()
        
        # Current actor does not exist
        if actor is None:
            abort(404)
        
        # delete current actor
        actor.delete()
    except AuthError as auth_error:
        raise auth_error
    except Exception as e:
        print(sys.exc_info())
        raise e
        
    return jsonify({
            'success': True,
            'deleted': id
        }), 200

"""
Create error handlers for all expected errors
including 404 and 422.
"""
@app.errorhandler(404)
def not_found(error):
    return( 
        jsonify({'success': False, 'error': 404,'message': 'resource not found'}),
        404
    )

@app.errorhandler(422)
def unprocessed(error):
    return(
        jsonify({'success': False, 'error': 422,'message': 'request cannot be processed'}),
        422
    )
@app.errorhandler(400)
def bad_request(error):
    return(
        jsonify({'success': False, 'error': 400,'message': 'bad request'}),
        400
    )
@app.errorhandler(405)
def not_allowed(error):
    return(
        jsonify({'success': False, 'error': 405,'message': 'method not alllowed'}),
        405
    )

@app.errorhandler(401)
def unauthorized(error):
    return(
        jsonify({'success': False, 'error': 401,'message': 'the client must authenticate'}),
        401
    )

@app.errorhandler(408)
def request_time_out(error):
    return(
        jsonify({'success': False, 'error': 408,'message': 'request time out'}),
        408
    )

@app.errorhandler(500)
def internal_server_error(error):
    return(
        jsonify({'success': False, 'error': 500,'message': 'internal server error'}),
        500
    )

@app.errorhandler(501)
def not_implemented(error):
    return(
        jsonify({'success': False, 'error': 501,'message': 'not implement'}),
        501
    )

@app.errorhandler(503)
def service_unavailable(error):
    return(
        jsonify({'success': False, 'error': 503,'message': 'service unavailable'}),
        503
    )

@app.errorhandler(504)
def gateway_timeout(error):
    return(
        jsonify({'success': False, 'error': 504,'message': 'gateway timeout'}),
        504
    )