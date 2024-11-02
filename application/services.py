from adapters.movie_api_adapter import MovieAPIAdapter
from datetime import datetime
from settings import config
import redis
import sys

# Cargar configuración de desarrollo
development_config = config['development']()

# Inicializar cliente de Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class MovieService:
    def __init__(self, api_key=None, headers=None, account_id=None):
        """
        Inicializa MovieService con parámetros de autenticación para API externa.

        Args:
            api_key (str): Clave de API.
            headers (dict): Encabezados de solicitud HTTP.
            account_id (str): ID de cuenta.
        """
        self.movie_api = MovieAPIAdapter(
            api_key or development_config.THEMOVIEDB_API_KEY,
            headers or development_config.headers,
            account_id or development_config.ACCOUNT_ID,
            redis_client
        )

    def get_popular_movies(self):
        """
        Obtener las películas populares desde la API externa o la caché.
        
        Returns:
            dict: Resultados de películas populares o mensaje de error.
        """
        try:
            return self.movie_api.get_popular_movies()['results']
        except Exception as e:
            print(f"Error al obtener películas populares: {e}", file=sys.stderr)
            return {'message': 'Error al obtener películas populares'}, 500

    def get_favorite_movies(self):
        """
        Obtener las películas favoritas del usuario.

        Returns:
            dict: Lista de películas favoritas o mensaje de error.
        """
        try:
            return self.movie_api.get_favorite_movies()
        except Exception as e:
            print(f"Error al obtener películas favoritas: {e}", file=sys.stderr)
            return {'message': 'Error al obtener películas favoritas'}, 500

    def add_favorite_movie(self, media_id):
        """
        Agregar una película a la lista de favoritas.

        Args:
            media_id (int): ID de la película.

        Returns:
            dict: Respuesta de la operación o mensaje de error.
        """
        try:
            response = self.movie_api.add_favorite_movie(media_id)
            if response is None:
                return {'message': 'No se pudo agregar la película favorita'}, 500
            return {'status_code': response.status_code, 'response': response.json()}
        except Exception as e:
            print(f"Error al agregar película favorita: {e}", file=sys.stderr)
            return {'message': 'Error al agregar película favorita'}, 500

    def delete_favorite_movie(self, media_id):
        """
        Eliminar una película de la lista de favoritas.

        Args:
            media_id (int): ID de la película.

        Returns:
            dict: Respuesta de la operación o mensaje de error.
        """
        try:
            response = self.movie_api.delete_favorite_movie(media_id)
            if response is None:
                return {'message': 'No se pudo eliminar la película favorita'}, 500
            return {'status_code': response.status_code, 'response': response.json()}
        except Exception as e:
            print(f"Error al eliminar película favorita: {e}", file=sys.stderr)
            return {'message': 'Error al eliminar película favorita'}, 500

    def rate_movie(self, movie_id, rating):
        """
        Calificar una película si la calificación está en el rango permitido.

        Args:
            movie_id (int): ID de la película.
            rating (int): Calificación (1 a 5).

        Returns:
            dict: Respuesta de la operación, error o mensaje de calificación inválida.
        """
        if 1 <= rating <= 5:
            try:
                response = self.movie_api.rate_movie(movie_id, rating)
                if response is None:
                    return {'message': 'No se pudo calificar la película'}, 500
                return {'status_code': response.status_code, 'response': response.json()}
            except Exception as e:
                print(f"Error al calificar película: {e}", file=sys.stderr)
                return {'message': 'Error al calificar película'}, 500
        return {'message': 'La calificación debe estar entre 1 y 5'}, 400

    def get_rated_movies(self):
        """
        Obtener las películas calificadas por el usuario.

        Returns:
            dict: Lista de películas calificadas o mensaje de error.
        """
        try:
            return self.movie_api.get_rated_movies()
        except Exception as e:
            print(f"Error al obtener películas calificadas: {e}", file=sys.stderr)
            return {'message': 'Error al obtener películas calificadas'}, 500

    def get_favorite_movies_by_release_date(self):
        """
        Obtener películas favoritas ordenadas por fecha de lanzamiento.

        Returns:
            list: Películas favoritas ordenadas o mensaje de error.
        """
        try:
            favorite_movies = self.movie_api.get_favorite_movies()
            sorted_movies = sorted(
                favorite_movies['results'],
                key=lambda x: datetime.strptime(x['release_date'], "%Y-%m-%d"),
                reverse=True
            )
            return sorted_movies
        except Exception as e:
            print(f"Error al obtener películas favoritas por fecha de lanzamiento: {e}", file=sys.stderr)
            return {'message': 'Error al obtener películas favoritas por fecha de lanzamiento'}, 500

    def get_rated_movies_from_favorites(self):
        """
        Obtener películas calificadas que también son favoritas.

        Returns:
            list: Películas calificadas en favoritas o mensaje de error.
        """
        try:
            rated_movies = self.movie_api.get_rated_movies()['results']
            favorite_movies_ids = {movie['id'] for movie in self.movie_api.get_favorite_movies()['results']}
            return [movie for movie in rated_movies if movie['id'] in favorite_movies_ids]
        except Exception as e:
            print(f"Error al obtener películas calificadas desde favoritos: {e}", file=sys.stderr)
            return {'message': 'Error al obtener películas calificadas desde favoritos'}, 500

    def delete_all_favorite_movies(self):
        """
        Eliminar todas las películas favoritas del usuario.

        Returns:
            dict: Estado de la operación o mensaje de error.
        """
        try:
            favorite_movies = self.movie_api.get_favorite_movies()['results']
            for movie in favorite_movies:
                self.movie_api.delete_favorite_movie(movie['id'])
            return {'status': 'success', 'message': 'Todas las películas favoritas han sido eliminadas'}
        except Exception as e:
            print(f"Error al eliminar todas las películas favoritas: {e}", file=sys.stderr)
            return {'message': 'Error al eliminar todas las películas favoritas'}, 500
