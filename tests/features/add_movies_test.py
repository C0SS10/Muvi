from unittest.mock import patch
import pytest

# Constantes comunes
ENDPOINT_INSERT_MANY = "/api/movies/insert-many"
ENDPOINT_SINGLE = "/api/movies"
POSTER_URL_1 = "https://m.media-amazon.com/images/I/abc.jpg"
POSTER_URL_2 = "https://m.media-amazon.com/images/I/def.jpg"
TITLE_1 = "Inception"
TITLE_2 = "The Dark Knight"
DIRECTOR = "Christopher Nolan"

MOVIE_1 = {
    "title": TITLE_1,
    "plot": "A thief who steals corporate secrets...",
    "release_date": "2010",
    "genre": ["Sci-Fi", "Thriller"],
    "director": DIRECTOR,
    "rating": 4.8,
    "poster": POSTER_URL_1
}

MOVIE_2 = {
    "title": TITLE_2,
    "plot": "Batman raises the stakes in his war on crime...",
    "release_date": "2008",
    "genre": ["Action", "Crime"],
    "director": DIRECTOR,
    "rating": 4.9,
    "poster": POSTER_URL_2
}

def test_add_many_movies_success(client):
    # Arrange
    payload = [MOVIE_1, MOVIE_2]

    # Act
    response = client.post(ENDPOINT_INSERT_MANY, json=payload)

    # Assert
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert "Movies created with IDs" in data["message"]

def test_redirect_many_to_single_movie(client):
    # Arrange
    payload = [MOVIE_1]

    # Act
    response = client.post(ENDPOINT_INSERT_MANY, json=payload)

    # Assert
    assert response.status_code == 307
    assert response.headers["Location"].endswith(ENDPOINT_SINGLE)

@pytest.mark.parametrize("rating", [-1.0, 6.0, 5.1])
def test_add_many_movies_invalid_rating(client, rating):
    movie_1_invalid = {**MOVIE_1, "rating": rating}
    movie_2_invalid = {**MOVIE_2, "rating": rating}
    payload = [movie_1_invalid, movie_2_invalid]

    # Act
    response = client.post(ENDPOINT_INSERT_MANY, json=payload)

    # Assert
    if 0 <= rating <= 5 and isinstance(rating, (int, float)):
        assert response.status_code == 201
    else:
        assert response.status_code == 422
        assert "Rating must be between 0 and 5" in response.get_data(as_text=True)

def test_add_many_movies_empty_list(client):
    # Act
    response = client.post(ENDPOINT_INSERT_MANY, json=[])

    # Assert
    assert response.status_code == 422
    assert "No movies provided" in response.get_data(as_text=True)

def test_add_many_movies_internal_error(client):
    # Arrange
    payload = [MOVIE_1, MOVIE_2]

    with patch('app.domain.services.movie_services.MovieService.add_many_movies') as mock_add_many:
        mock_add_many.side_effect = Exception("Database error")

        response = client.post(ENDPOINT_INSERT_MANY, json=payload)

        # Assert
        assert response.status_code == 500
        assert "Internal server error" in response.get_data(as_text=True)
