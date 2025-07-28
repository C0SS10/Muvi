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


def test_add_movie_invalid_rating(client):
    # Arrange
    payload = {
        "title": "Bad Rating",
        "plot": "Plot",
        "release_date": "2014",
        "genre": "Drama",
        "director": "Someone",
        "rating": 6.0,  # Invalid rating > 5
        "poster": "https://m.media-amazon.com/images/I/abc.jpg"
    }

    # Act
    response = client.post("/api/movies/", json=payload)

    # Assert
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
