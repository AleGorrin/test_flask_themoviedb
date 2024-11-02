import pytest
from unittest.mock import MagicMock
from application.services import MovieService

@pytest.fixture
def mock_adapter():
    # Mock para MovieAPIAdapter
    mock_adapter = MagicMock()
    return mock_adapter

@pytest.fixture
def movie_service(mock_adapter):
    # Mock de MovieAPIAdapter en MovieService
    return MovieService(api_key="dummy_key", headers={}, account_id="dummy_id")

def test_get_popular_movies(movie_service, mock_adapter):
    # Mock para get_popular_movies
    mock_adapter.get_popular_movies.return_value = {'results': [{'title': 'Movie1'}, {'title': 'Movie2'}]}
    movie_service.movie_api = mock_adapter

    popular_movies = movie_service.get_popular_movies()
    assert popular_movies == [{'title': 'Movie1'}, {'title': 'Movie2'}]
    mock_adapter.get_popular_movies.assert_called_once()

def test_get_favorite_movies(movie_service, mock_adapter):
    mock_adapter.get_favorite_movies.return_value = {'results': [{'id': 1, 'title': 'FavMovie1'}]}
    movie_service.movie_api = mock_adapter

    favorite_movies = movie_service.get_favorite_movies()
    assert favorite_movies == {'results': [{'id': 1, 'title': 'FavMovie1'}]}
    mock_adapter.get_favorite_movies.assert_called_once()

def test_add_favorite_movie(movie_service, mock_adapter):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"success": True}
    mock_adapter.add_favorite_movie.return_value = mock_response
    movie_service.movie_api = mock_adapter

    response = movie_service.add_favorite_movie(media_id=1)
    assert response == {'status_code': 201, 'response': {"success": True}}
    mock_adapter.add_favorite_movie.assert_called_once_with(1)

def test_delete_favorite_movie(movie_service, mock_adapter):
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.json.return_value = {"success": True}
    mock_adapter.delete_favorite_movie.return_value = mock_response
    movie_service.movie_api = mock_adapter

    response = movie_service.delete_favorite_movie(media_id=1)
    assert response == {'status_code': 204, 'response': {"success": True}}
    mock_adapter.delete_favorite_movie.assert_called_once_with(1)

def test_rate_movie_valid_rating(movie_service, mock_adapter):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_adapter.rate_movie.return_value = mock_response
    movie_service.movie_api = mock_adapter

    response = movie_service.rate_movie(movie_id=1, rating=4)
    assert response == {'status_code': 200, 'response': {"success": True}}
    mock_adapter.rate_movie.assert_called_once_with(1, 4)

def test_rate_movie_invalid_rating(movie_service):
    response = movie_service.rate_movie(movie_id=1, rating=6)
    assert response == ({'message': 'Rating must be between 1 and 5'}, 400)

def test_get_rated_movies(movie_service, mock_adapter):
    mock_adapter.get_rated_movies.return_value = {'results': [{'id': 1, 'title': 'RatedMovie1'}]}
    movie_service.movie_api = mock_adapter

    rated_movies = movie_service.get_rated_movies()
    assert rated_movies == {'results': [{'id': 1, 'title': 'RatedMovie1'}]}
    mock_adapter.get_rated_movies.assert_called_once()

def test_get_favorite_movies_by_release_date(movie_service, mock_adapter):
    mock_adapter.get_favorite_movies.return_value = {
        'results': [
            {'id': 1, 'title': 'Movie1', 'release_date': '2023-10-10'},
            {'id': 2, 'title': 'Movie2', 'release_date': '2021-08-15'},
        ]
    }
    movie_service.movie_api = mock_adapter

    sorted_movies = movie_service.get_favorite_movies_by_release_date()
    assert sorted_movies[0]['release_date'] == '2023-10-10'
    assert sorted_movies[1]['release_date'] == '2021-08-15'
    mock_adapter.get_favorite_movies.assert_called_once()

def test_get_rated_movies_from_favorites(movie_service, mock_adapter):
    mock_adapter.get_rated_movies.return_value = {
        'results': [{'id': 1, 'title': 'RatedFavMovie1'}, {'id': 2, 'title': 'RatedNonFavMovie'}]
    }
    mock_adapter.get_favorite_movies.return_value = {
        'results': [{'id': 1, 'title': 'RatedFavMovie1'}]
    }
    movie_service.movie_api = mock_adapter

    rated_fav_movies = movie_service.get_rated_movies_from_favorites()
    assert rated_fav_movies == [{'id': 1, 'title': 'RatedFavMovie1'}]
    mock_adapter.get_rated_movies.assert_called_once()
    mock_adapter.get_favorite_movies.assert_called_once()

def test_delete_all_favorite_movies(movie_service, mock_adapter):
    mock_adapter.get_favorite_movies.return_value = {
        'results': [{'id': 1, 'title': 'Movie1'}, {'id': 2, 'title': 'Movie2'}]
    }
    mock_adapter.delete_favorite_movie.return_value = MagicMock(status_code=204)
    movie_service.movie_api = mock_adapter

    response = movie_service.delete_all_favorite_movies()
    assert response == {'status': 'success', 'message': 'All favorite movies have been deleted'}
    mock_adapter.get_favorite_movies.assert_called_once()
    assert mock_adapter.delete_favorite_movie.call_count == 2
