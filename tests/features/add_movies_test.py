from unittest.mock import patch
import pytest


def test_add_many_movies_success(client):
    # Arrange
    payload = [
        {
            "title": "Inception",
            "plot": "A thief who steals corporate secrets...",
            "release_date": "2010",
            "genre": ["Sci-Fi", "Thriller"],
            "director": "Christopher Nolan",
            "rating": 4.8,
            "poster": "https://m.media-amazon.com/images/I/abc.jpg"
        },
        {
            "title": "The Dark Knight",
            "plot": "Batman raises the stakes in his war on crime...",
            "release_date": "2008",
            "genre": ["Action", "Crime"],
            "director": "Christopher Nolan",
            "rating": 4.9,
            "poster": "https://m.media-amazon.com/images/I/def.jpg"
        }
    ]

    # Act
    response = client.post("/api/movies/insert-many", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert "Movies created with IDs" in data["message"]

def test_redirect_many_to_single_movie(client):
    # Arrange
    payload = [
        {
            "title": "Inception",
            "plot": "A thief who steals corporate secrets...",
            "release_date": "2010",
            "genre": ["Sci-Fi", "Thriller"],
            "director": "Christopher Nolan",
            "rating": 4.8,
            "poster": "https://m.media-amazon.com/images/I/abc.jpg"
        }
    ]

    # Act
    response = client.post("/api/movies/insert-many", json=payload)

    # Assert
    assert response.status_code == 307
    assert response.headers["Location"].endswith("/api/movies/")

@pytest.mark.parametrize("rating", [-1.0, 6.0, 0, 0.0, 5.1])
def test_add_many_movies_invalid_rating(client, rating):
    payload = [
        {
            "title": "Inception",
            "plot": "A thief who steals corporate secrets...",
            "release_date": "2010",
            "genre": ["Sci-Fi", "Thriller"],
            "director": "Christopher Nolan",
            "rating": rating,
            "poster": "https://m.media-amazon.com/images/I/abc.jpg"
        },
        {
            "title": "The Dark Knight",
            "plot": "Batman raises the stakes in his war on crime...",
            "release_date": "2008",
            "genre": ["Action", "Crime"],
            "director": "Christopher Nolan",
            "rating": rating,
            "poster": "https://m.media-amazon.com/images/I/def.jpg"
        }
    ]

    # Act
    response = client.post("/api/movies/insert-many", json=payload)

    # Assert
    if 0 <= rating <= 5 and isinstance(rating, (int, float)):
        assert response.status_code == 201
    else:
        assert response.status_code == 422
        assert "Rating must be between 0 and 5" in response.get_data(as_text=True)

def test_add_many_movies_empty_list(client):
    # Act
    response = client.post("/api/movies/insert-many", json=[])

    # Assert
    assert response.status_code == 422
    assert "No movies provided" in response.get_data(as_text=True)

def test_add_many_movies_internal_error(client):
    # Arrange
    payload = [
        {
            "title": "Inception",
            "plot": "A thief who steals corporate secrets...",
            "release_date": "2010",
            "genre": ["Sci-Fi", "Thriller"],
            "director": "Christopher Nolan",
            "rating": 4.8,
            "poster": "https://m.media-amazon.com/images/I/abc.jpg"
        },
        {
            "title": "The Dark Knight",
            "plot": "Batman raises the stakes in his war on crime...",
            "release_date": "2008",
            "genre": ["Action", "Crime"],
            "director": "Christopher Nolan",
            "rating": 4.9,
            "poster": "https://m.media-amazon.com/images/I/def.jpg"
        }
    ]

    with patch('app.domain.services.movie_services.MovieService.add_many_movies') as mock_add_many:
        mock_add_many.side_effect = Exception("Database error")

        response = client.post("/api/movies/insert-many", json=payload)
        assert response.status_code == 500
        assert "Internal server error" in response.get_data(as_text=True)