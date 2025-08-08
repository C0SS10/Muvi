ENDPOINT = "/api/movies"

def test_get_movie_by_id_success(client):
    # Arrange
    valid_id = "68962b3e1d1afae2e2e30606"

    # Act
    response = client.get(f"{ENDPOINT}/{valid_id}")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert "title" in data
    assert "director" in data
    assert "rating" in data
    assert data["id"] == valid_id


def test_get_movie_by_id_not_found(client):
    non_existent_id = "64b8f3e2f1a4d2c9e8b7a1c4"

    response = client.get(f"{ENDPOINT}/{non_existent_id}")

    assert response.status_code == 404
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Movie not found"