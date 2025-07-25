def test_add_movies_success(client):
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