from flask import Blueprint, jsonify
from application.services import MovieService
from settings import config
from auth.auth import token_required, permission_required

# Cargar configuración de desarrollo
development_config = config['development']()

# Crear blueprint para las rutas de películas
movies_blueprint = Blueprint('movies', __name__)

# Inicializar servicio de películas con API Key y otros parámetros
movie_service = MovieService(
    api_key=development_config.THEMOVIEDB_API_KEY,
    headers=development_config.headers,
    account_id=development_config.ACCOUNT_ID
)

@movies_blueprint.route('/populars', methods=['GET'])
def get_popular_movies():
    """
    Obtener películas populares.
    
    Returns:
        JSON: Lista de películas populares.
    """
    return jsonify(movie_service.get_popular_movies())

@movies_blueprint.route('/get_favorite_movies', methods=['GET'], endpoint='get_favorite_movies')
@token_required
def get_favorite_movies(user):
    """
    Obtener películas favoritas del usuario autenticado.
    
    Args:
        user: Usuario autenticado.
    
    Returns:
        JSON: Lista de películas favoritas.
    """
    return jsonify(movie_service.get_favorite_movies())

@movies_blueprint.route('/add_favorite/<int:media_id>', methods=['POST'], endpoint='add_favorite')
@token_required
def add_favorite_movie(user, media_id):
    """
    Agregar una película a favoritos.
    
    Args:
        user: Usuario autenticado.
        media_id (int): ID de la película a agregar.
    
    Returns:
        JSON: Respuesta de la operación.
    """
    return jsonify(movie_service.add_favorite_movie(media_id))

@movies_blueprint.route('/delete_favorite/<int:media_id>', methods=['DELETE'], endpoint='delete_favorite')
@token_required
def delete_favorite_movie(user, media_id):
    """
    Eliminar una película de favoritos.
    
    Args:
        user: Usuario autenticado.
        media_id (int): ID de la película a eliminar.
    
    Returns:
        JSON: Respuesta de la operación.
    """
    return jsonify(movie_service.delete_favorite_movie(media_id))

@movies_blueprint.route('/rate_movie/<int:movie_id>/<int:rating>', methods=['POST'], endpoint='rate_movie')
@token_required
def rate_movie(user, movie_id, rating):
    """
    Calificar una película.
    
    Args:
        user: Usuario autenticado.
        movie_id (int): ID de la película.
        rating (int): Calificación otorgada.
    
    Returns:
        JSON: Respuesta de la operación.
    """
    return jsonify(movie_service.rate_movie(movie_id, rating))

@movies_blueprint.route('/get_rated_movies', methods=['GET'], endpoint='get_rated_movies')
@token_required
def get_rated_movies(user):
    """
    Obtener películas calificadas del usuario.
    
    Args:
        user: Usuario autenticado.
    
    Returns:
        JSON: Lista de películas calificadas.
    """
    return jsonify(movie_service.get_rated_movies())

@movies_blueprint.route('/get_favorite_movies_by_release_date', methods=['GET'], endpoint='get_favorite_movies_by_release_date')
@token_required
def get_favorite_movies_by_release_date(user):
    """
    Obtener películas favoritas ordenadas por fecha de lanzamiento.
    
    Args:
        user: Usuario autenticado.
    
    Returns:
        JSON: Lista de películas favoritas ordenada.
    """
    return jsonify(movie_service.get_favorite_movies_by_release_date())

@movies_blueprint.route('/rated_movies_from_favorites', methods=['GET'], endpoint='rated_movies_from_favorites')
@token_required
def rated_movies_from_favorites(user):
    """
    Obtener películas calificadas y en favoritos.
    
    Args:
        user: Usuario autenticado.
    
    Returns:
        JSON: Lista de películas calificadas en favoritos.
    """
    return jsonify(movie_service.get_rated_movies_from_favorites())

@movies_blueprint.route('/delete_favorite_movies', methods=['DELETE'])
@token_required
@permission_required('ADMIN')
def delete_favorite_movies(user):
    """
    Eliminar todas las películas de favoritos (requiere permisos de admin).
    
    Args:
        user: Usuario autenticado con permisos de admin.
    
    Returns:
        JSON: Respuesta de la operación.
    """
    return jsonify(movie_service.delete_all_favorite_movies())
