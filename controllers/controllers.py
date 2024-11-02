from flask import Blueprint, jsonify
from application.services import MovieService
from settings import config
from auth.auth import token_required, permission_required
development_config = config['development']()

movies_blueprint = Blueprint('movies', __name__)
movie_service = MovieService(api_key=development_config.THEMOVIEDB_API_KEY, headers=development_config.headers, account_id=development_config.ACCOUNT_ID)

@token_required
@permission_required('USER')
@movies_blueprint.route('/populars', methods=['GET'])
def get_popular_movies():
    return jsonify(movie_service.get_popular_movies())

@movies_blueprint.route('/get_favorite_movies', methods=['GET'], endpoint='add_favorite_movie')
@token_required
@permission_required('USER')
def get_favorite_movies(user):
    return jsonify(movie_service.get_favorite_movies())

@movies_blueprint.route('/add_favorite/<int:media_id>', methods=['POST'], endpoint='add_favorite_movie')
@token_required
@permission_required('USER')
def add_favorite_movie(user, media_id):
    return jsonify(movie_service.add_favorite_movie(media_id))

@movies_blueprint.route('/delete_favorite/<int:media_id>', methods=['DELETE'], endpoint='add_favorite_movie')
@token_required
@permission_required('USER')
def delete_favorite_movie(user, media_id):
    return jsonify(movie_service.delete_favorite_movie(media_id))

@movies_blueprint.route('/rate_movie/<int:movie_id>/<int:rating>', methods=['POST'], endpoint='add_favorite_movie')
@token_required
@permission_required('USER')
def rate_movie(user, movie_id, rating):
    return jsonify(movie_service.rate_movie(movie_id, rating))

@movies_blueprint.route('/get_rated_movies', methods=['GET'], endpoint='add_favorite_movie')
@token_required
@permission_required('USER')
def get_rated_movies(user):
    return jsonify(movie_service.get_rated_movies())

@movies_blueprint.route('/get_favorite_movies_by_release_date', methods=['GET'], endpoint='add_favorite_movie')
@token_required
@permission_required('USER')
def get_favorite_movies_by_release_date(user):
    return jsonify(movie_service.get_favorite_movies_by_release_date())

@movies_blueprint.route('/rated_movies_from_favorites', methods=['GET'], endpoint='add_favorite_movie')
@token_required
@permission_required('USER')
def rated_movies_from_favorites(user):
    return jsonify(movie_service.get_rated_movies_from_favorites())

@movies_blueprint.route('/delete_favorite_movies', methods=['DELETE'])
@token_required
@permission_required('ADMIN')
def delete_favorite_movies(user):
    return jsonify(movie_service.delete_all_favorite_movies())
