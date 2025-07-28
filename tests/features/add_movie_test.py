from unittest.mock import patch
import pytest


def test_add_movie_success(client):
    # Arrange
    payload = {
        "title": "Interstellar",
        "plot": "A team of explorers travel through a wormhole in space...",
        "release_date": "2014",
        "genre": ["Sci-Fi", "Adventure"],
        "director": ["Christopher Nolan"],
        "rating": 4.9,
        "poster": "https://m.media-amazon.com/images/I/abc.jpg"
    }

    # Act
    response = client.post("/api/movies/", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert "Movie created" in data["message"]


def test_add_movie_invalid_release_date(client):
    # Arrange
    payload = {
        "title": "Invalid Date",
        "plot": "Some plot",
        "release_date": "07-11-2014",  # Wrong format
        "genre": ["Drama"],
        "director": "Some Director",
        "rating": 4.0,
        "poster": "https://m.media-amazon.com/images/I/abc.jpg"
    }

    # Act
    response = client.post("/api/movies/", json=payload)

    # Assert
    assert response.status_code == 422
    assert "Release date must be in the format" in response.get_data(as_text=True)


@pytest.mark.parametrize("rating", [-1.0, 5.1, 1238, 85.5, 0.0, 0])
def test_add_movie_invalid_rating_values(client, rating):
    payload = {
        "title": "Invalid Rating",
        "plot": "Plot",
        "release_date": "2020",
        "genre": ["Drama"],
        "director": ["Someone"],
        "rating": rating,
        "poster": "https://m.media-amazon.com/images/I/abc.jpg"
    }

    # Act
    response = client.post("/api/movies/", json=payload)

    # Assert
    if 0 <= rating <= 5 and isinstance(rating, (int, float)):
        assert response.status_code == 201
    else:
        assert response.status_code == 422
        assert "Rating must be between 0 and 5" in response.get_data(as_text=True)


def test_add_movie_invalid_poster_url(client):
    # Arrange
    payload = {
        "title": "Bad Poster",
        "plot": "Plot",
        "release_date": "2014",
        "genre": "Thriller",
        "director": "Someone",
        "rating": 4.5,
        "poster": "https://example.com/poster.jpg"  # Not allowed domain
    }

    # Act
    response = client.post("/api/movies/", json=payload)

    # Assert
    assert response.status_code == 422
    assert "Poster URL must be from m.media-amazon.com" in response.get_data(as_text=True)


def test_add_movie_duplicate_genres_and_directors(client):
    # Arrange
    payload = {
        "title": "Duplicated Fields",
        "plot": "Plot",
        "release_date": "2020",
        "genre": ["Drama", "Drama", "Action"],
        "director": ["Nolan", "Nolan"],
        "rating": 3.5,
        "poster": "https://m.media-amazon.com/images/I/abc.jpg"
    }

    # Act
    response = client.post("/api/movies/", json=payload)

    # Assert
    assert response.status_code == 201
    message = response.get_json()["message"]
    assert "Movie created" in message

def test_add_movie_missing_fields(client):
    # Arrange
    payload = {
        "title": "Incomplete",
        "plot": "No release date or director",
        "rating": 3.0
    }

    # Act
    response = client.post("/api/movies/", json=payload)

    # Assert
    assert response.status_code == 422
    assert "Field required" in response.get_data(as_text=True)

def test_add_movie_internal_error(client):
    payload ={
        "title": "Internal Error",
        "plot": "This will cause an error",
        "release_date": "2020",
        "genre": ["Drama"],
        "director": ["Someone"],
        "rating": 4.0,
        "poster": "https://m.media-amazon.com/images/I/abc.jpg"
    }

    with patch('app.domain.services.movie_services.MovieService.add_movie') as mock_add:
        mock_add.side_effect = Exception("Database error")

        response = client.post("/api/movies/", json=payload)
        assert response.status_code == 500
        assert "Internal server error" in response.get_data(as_text=True)

""" 
TODO: WHEN IMPLEMENT FUNCTIONALITY GET BY TITLE, ADD TESTS FOR DUPLICATE MOVIES
def test_add_movie_duplicate_movies(client):
    payload = [{
        "title": "Duplicate Title",
        "plot": "Test",
        "release_date": "2020",
        "genre": ["Drama"],
        "director": ["Someone"],
        "rating": 4.0,
        "poster": "https://m.media-amazon.com/images/I/abc.jpg"
    }, {
        "title": "Duplicate Title",
        "plot": "Test",
        "release_date": "2020",
        "genre": ["Drama"],
        "director": ["Someone"],
        "rating": 4.0,
        "poster": "https://m.media-amazon.com/images/I/abc.jpg"
    }]

    client.post("/api/movies/", json=payload)
    response = client.post("/api/movies/", json=payload)
    assert response.status_code == 409
    assert "already exists" in response.get_data(as_text=True)
 """