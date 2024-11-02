import requests
from settings import config
import redis
import json
import time
import sys
from requests.exceptions import RequestException

development_config = config['development']()

def retry_with_backoff(max_retries=3, backoff_factor=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except RequestException as e:
                    retries += 1
                    wait_time = backoff_factor ** retries
                    print(f"Intento {retries} fallido. Reintentando en {wait_time} segundos...", file=sys.stderr)
                    time.sleep(wait_time)
            print("Todos los intentos fallaron. Obteniendo respuesta de caché si está disponible...", file=sys.stderr)
            return None
        return wrapper
    return decorator

class MovieAPIAdapter:
    def __init__(self, api_key, headers, account_id, redis_client=None):
        self.api_key = api_key
        self.headers = headers
        self.account_id = account_id
        self.base_url = f"https://api.themoviedb.org/3/account/{account_id}"
        self.redis_client = redis_client
        self.cache_duration = int(getattr(development_config, "CACHE_DURATION", 30))

    def _cache_response(self, key, duration, response):
        if self.redis_client:
            try:
                self.redis_client.setex(key, duration, json.dumps(response))
            except:
                if redis.exceptions.ConnectionError:
                    print("Redis no está disponible, continuando sin caché.")
                else:
                    print(f"Error al guardar en caché: {redis.exceptions.RedisError}", file=sys.stderr)

    def _get_cached_response(self, key):
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(key)
                if cached_data:
                    return json.loads(cached_data)
            except:
                if redis.exceptions.ConnectionError:
                    print("Redis no está disponible, continuando sin caché.")
                else:
                    print(f"Error al guardar en caché: {redis.exceptions.RedisError}", file=sys.stderr)
        return None

    @retry_with_backoff(max_retries=3, backoff_factor=2)
    def get_popular_movies(self):
        cache_key = "popular_movies"
        cached_response = self._get_cached_response(cache_key)

        if cached_response:
            return cached_response

        try:
            response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={self.api_key}")
            response.raise_for_status()
            response_json = response.json()
            self._cache_response(cache_key, self.cache_duration, response_json)
            return response_json
        except RequestException as e:
            print(f"Error al obtener películas populares: {e}", file=sys.stderr)
            return None

    @retry_with_backoff(max_retries=3, backoff_factor=2)
    def get_favorite_movies(self):
        cache_key = f"favorite_movies_{self.account_id}"
        cached_response = self._get_cached_response(cache_key)

        if cached_response:
            return cached_response

        try:
            response = requests.get(f"{self.base_url}/favorite/movies", headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            self._cache_response(cache_key, self.cache_duration, response_json)
            return response_json
        except RequestException as e:
            print(f"Error al obtener películas favoritas: {e}", file=sys.stderr)
            return None

    @retry_with_backoff(max_retries=3, backoff_factor=2)
    def add_favorite_movie(self, media_id):
        payload = {"media_type": "movie", "media_id": media_id, "favorite": True}
        try:
            response = requests.post(f"{self.base_url}/favorite", headers=self.headers, json=payload)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500:
                print("Error al agregar película favorita", file=sys.stderr)
            else:
                print(f"Error al agregar película favorita: {e}", file=sys.stderr)
            return None

    @retry_with_backoff(max_retries=3, backoff_factor=2)
    def delete_favorite_movie(self, media_id):
        payload = {"media_type": "movie", "media_id": media_id, "favorite": False}
        try:
            response = requests.post(f"{self.base_url}/favorite", headers=self.headers, json=payload)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500:
                print("Error al eliminar película favorita:", file=sys.stderr)
            else:
                print(f"Error al eliminar película favorita: {e}", file=sys.stderr)
            return None

    @retry_with_backoff(max_retries=3, backoff_factor=2)
    def rate_movie(self, movie_id, rating):
        payload = {"value": rating}
        try:
            response = requests.post(f"https://api.themoviedb.org/3/movie/{movie_id}/rating", headers=self.headers, json=payload)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500:
                print("Error al calificar película", file=sys.stderr)
            else:
                print(f"Error al calificar película: {e}", file=sys.stderr)
            return None

    @retry_with_backoff(max_retries=3, backoff_factor=2)
    def get_rated_movies(self):
        cache_key = f"rated_movies_{self.account_id}"
        cached_response = self._get_cached_response(cache_key)

        if cached_response:
            return cached_response

        try:
            response = requests.get(f"{self.base_url}/rated/movies", headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            self._cache_response(cache_key, self.cache_duration, response_json)
            return response_json
        except RequestException as e:
            print(f"Error al obtener películas calificadas: {e}", file=sys.stderr)
            return None
