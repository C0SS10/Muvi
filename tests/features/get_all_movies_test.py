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
    response = client.get(f"{ENDPOINT}?limit=5&offset=5")

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