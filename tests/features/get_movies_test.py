# Constantes comunes
ENDPOINT = "/api/movies"

def test_get_all_movies_success(client):
    # Act
    response = client.get(ENDPOINT)

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 10
    assert data[0]["title"] == "Duplicated Fields"

def test_get_all_movies_with_pagination(client):
    # Act
    response = client.get(f"{ENDPOINT}?limit=5&offset=2")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 5
    assert isinstance(data[0]["rating"], float)
    assert isinstance(data[0]["title"], str)

def test_get_all_movies_invalid_pagination(client):
    response = client.get(f"{ENDPOINT}?limit=2&offset=1000")

    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data and data["message"] == "Invalid pagination parameters"

def test_get_all_movies_invalid_query_params(client):
    response_parameters_zero = client.get("/api/movies?limit=0&offset=0")
    response_offset_negative = client.get("/api/movies?limit=2&offset=-1")

    data = response_parameters_zero.get_json()
    assert "message" in data and data["message"] == "Invalid pagination parameters"
    assert response_parameters_zero.status_code == 400

    data = response_offset_negative.get_json()
    assert "message" in data and data["message"] == "Invalid pagination parameters"
    assert response_offset_negative.status_code == 400

def test_get_movies_with_filters(client):
    # Act
    response = client.get(f"{ENDPOINT}?title=Interstellar&director=Christopher&genre=Adventure")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all("Interstellar" in movie["title"] for movie in data)

def test_get_movies_with_valid_year_filter(client):
    # Act
    response = client.get(f"{ENDPOINT}?year=2000")

    # Assert
    assert response.status_code in [200, 404]
    data = response.get_json()
    if response.status_code == 200:
        assert all("release_date" in movie for movie in data)
    else:
        assert data["message"] == "No movies found"

def test_get_movies_with_invalid_year_filter(client):
    # Act
    response = client.get(f"{ENDPOINT}?year=two-thousand")

    # Assert
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Year must be an integer"

def test_get_movies_with_invalid_rating_filter(client):
    # Act
    response = client.get(f"{ENDPOINT}?rating=four.point.five")

    # Assert
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Rating must be a float"

def test_get_movies_not_found(client):
    # Act
    response = client.get(f"{ENDPOINT}?title=ThisIsNotATitle")

    # Assert
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "No movies found"
