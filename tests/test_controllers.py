import pytest
from unittest.mock import MagicMock
from flask import Flask
from controllers.controllers import movies_blueprint

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(movies_blueprint)
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_movie_service(monkeypatch):
    mock_service = MagicMock()
    monkeypatch.setattr("controllers.controllers.movie_service", mock_service)
    return mock_service

def test_get_popular_movies(client, mock_movie_service):
    mock_movie_service.get_popular_movies.return_value = [{'title': 'Movie1'}, {'title': 'Movie2'}]
    
    response = client.get('/populars')
    assert response.status_code == 200
    assert response.json == [{'title': 'Movie1'}, {'title': 'Movie2'}]
    mock_movie_service.get_popular_movies.assert_called_once()

def test_get_favorite_movies(client, mock_movie_service):
    mock_movie_service.get_favorite_movies.return_value = [{'title': 'FavMovie1'}]
    
    response = client.get('/get_favorite_movies')
    assert response.status_code == 200
    assert response.json == [{'title': 'FavMovie1'}]
    mock_movie_service.get_favorite_movies.assert_called_once()

def test_add_favorite_movie(client, mock_movie_service):
    mock_movie_service.add_favorite_movie.return_value = {'status_code': 201, 'response': {"success": True}}
    
    response = client.post('/add_favorite/1')
    assert response.status_code == 200
    assert response.json == {'status_code': 201, 'response': {"success": True}}
    mock_movie_service.add_favorite_movie.assert_called_once_with(1)

def test_delete_favorite_movie(client, mock_movie_service):
    mock_movie_service.delete_favorite_movie.return_value = {'status_code': 204, 'response': {"success": True}}
    
    response = client.delete('/delete_favorite/1')
    assert response.status_code == 200
    assert response.json == {'status_code': 204, 'response': {"success": True}}
    mock_movie_service.delete_favorite_movie.assert_called_once_with(1)

def test_rate_movie(client, mock_movie_service):
    mock_movie_service.rate_movie.return_value = {'status_code': 200, 'response': {"success": True}}
    
    response = client.post('/rate_movie/1/5')
    assert response.status_code == 200
    assert response.json == {'status_code': 200, 'response': {"success": True}}
    mock_movie_service.rate_movie.assert_called_once_with(1, 5)

def test_get_rated_movies(client, mock_movie_service):
    mock_movie_service.get_rated_movies.return_value = [{'title': 'RatedMovie1'}]
    
    response = client.get('/get_rated_movies')
    assert response.status_code == 200
    assert response.json == [{'title': 'RatedMovie1'}]
    mock_movie_service.get_rated_movies.assert_called_once()

def test_get_favorite_movies_by_release_date(client, mock_movie_service):
    mock_movie_service.get_favorite_movies_by_release_date.return_value = [
        {'title': 'Movie1', 'release_date': '2023-10-10'}
    ]
    
    response = client.get('/get_favorite_movies_by_release_date')
    assert response.status_code == 200
    assert response.json == [{'title': 'Movie1', 'release_date': '2023-10-10'}]
    mock_movie_service.get_favorite_movies_by_release_date.assert_called_once()

def test_rated_movies_from_favorites(client, mock_movie_service):
    mock_movie_service.get_rated_movies_from_favorites.return_value = [{'title': 'RatedFavMovie1'}]
    
    response = client.get('/rated_movies_from_favorites')
    assert response.status_code == 200
    assert response.json == [{'title': 'RatedFavMovie1'}]
    mock_movie_service.get_rated_movies_from_favorites.assert_called_once()

