import pytest
import requests
import requests_mock
from adapters.movie_api_adapter import MovieAPIAdapter

@pytest.fixture
def movie_api_adapter():
    api_key = "fake_api_key"
    headers = {"Authorization": "Bearer fake_access_token"}
    account_id = "12345"
    return MovieAPIAdapter(api_key, headers, account_id)

def test_get_popular_movies(movie_api_adapter):
    with requests_mock.Mocker() as m:
        mock_response = {"results": [{"title": "Movie 1"}, {"title": "Movie 2"}]}
        m.get(f"https://api.themoviedb.org/3/movie/popular?api_key=fake_api_key", json=mock_response)

        response = movie_api_adapter.get_popular_movies()
        assert response == mock_response
        assert "results" in response
        assert len(response["results"]) == 2

def test_get_favorite_movies(movie_api_adapter):
    with requests_mock.Mocker() as m:
        mock_response = {"results": [{"title": "Favorite Movie 1"}, {"title": "Favorite Movie 2"}]}
        m.get(f"https://api.themoviedb.org/3/account/12345/favorite/movies", json=mock_response)

        response = movie_api_adapter.get_favorite_movies()
        assert response == mock_response
        assert "results" in response
        assert len(response["results"]) == 2

def test_add_favorite_movie(movie_api_adapter):
    with requests_mock.Mocker() as m:
        media_id = 123
        m.post(f"https://api.themoviedb.org/3/account/12345/favorite", json={"status_code": 1})

        response = movie_api_adapter.add_favorite_movie(media_id)
        assert response.json()["status_code"] == 1

def test_delete_favorite_movie(movie_api_adapter):
    with requests_mock.Mocker() as m:
        media_id = 123
        m.post(f"https://api.themoviedb.org/3/account/12345/favorite", json={"status_code": 1})

        response = movie_api_adapter.delete_favorite_movie(media_id)
        assert response.json()["status_code"] == 1

def test_rate_movie(movie_api_adapter):
    with requests_mock.Mocker() as m:
        movie_id = 456
        rating = 8.5
        m.post(f"https://api.themoviedb.org/3/movie/{movie_id}/rating", json={"status_code": 1})

        response = movie_api_adapter.rate_movie(movie_id, rating)
        assert response.json()["status_code"] == 1

def test_get_rated_movies(movie_api_adapter):
    with requests_mock.Mocker() as m:
        mock_response = {"results": [{"title": "Rated Movie 1"}, {"title": "Rated Movie 2"}]}
        m.get(f"https://api.themoviedb.org/3/account/12345/rated/movies", json=mock_response)

        response = movie_api_adapter.get_rated_movies()
        assert response == mock_response
        assert "results" in response
        assert len(response["results"]) == 2
