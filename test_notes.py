import requests

BASE_URL = "http://127.0.0.1:8000"


############################################
### Basic tests
############################################


def test_get_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World"}


def test_get_status():
    """Test status endpoint"""
    response = requests.get(f"{BASE_URL}/status")

    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_get_about():
    """Test about endpoint"""
    response = requests.get(f"{BASE_URL}/about")

    assert response.status_code == 200
    assert response.json()["author"] == "Kulish Diana"


############################################
### CRUD tests
############################################


def test_create_note():
    """Test creating a new note"""
    note_data = {
        "title": "Test Note",
        "content": "Test content",
        "category": "work",
        "tags": ["test", "pytest"]
    }
    response = requests.post(f"{BASE_URL}/notes", json=note_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test content"
    assert data["category"] == "work"
    assert "id" in data
    assert "created_at" in data


def test_list_notes():
    """Test listing all notes"""
    response = requests.get(f"{BASE_URL}/notes")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_note_by_id():
    """Test getting a specific note by ID"""
    # First create a note
    note_data = {
        "title": "Note for ID test",
        "content": "Content for ID test",
        "category": "personal",
        "tags": ["id-test"]
    }
    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    note_id = create_response.json()["id"]

    # Then get it by ID
    response = requests.get(f"{BASE_URL}/notes/{note_id}")

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["title"] == "Note for ID test"


def test_update_note():
    """Test updating a note with PUT"""
    # First create a note
    note_data = {
        "title": "Note to update",
        "content": "Original content",
        "category": "personal",
        "tags": ["original"]
    }
    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    note_id = create_response.json()["id"]

    # Then update it
    updated_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "category": "work",
        "tags": ["updated"]
    }
    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=updated_data)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["content"] == "Updated content"
    assert response.json()["category"] == "work"


def test_partial_update_note():
    """Test partially updating a note with PATCH"""
    # First create a note
    note_data = {
        "title": "Note to patch",
        "content": "Original content",
        "category": "personal",
        "tags": []
    }
    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    note_id = create_response.json()["id"]

    # Then patch only the title
    patch_data = {"title": "Patched Title"}
    response = requests.patch(f"{BASE_URL}/notes/{note_id}", json=patch_data)

    assert response.status_code == 200
    assert response.json()["title"] == "Patched Title"
    assert response.json()["content"] == "Original content"


def test_delete_note():
    """Test deleting a note"""
    # First create a note
    note_data = {
        "title": "Note to delete",
        "content": "This will be deleted",
        "category": "personal",
        "tags": []
    }
    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    note_id = create_response.json()["id"]

    # Then delete it
    response = requests.delete(f"{BASE_URL}/notes/{note_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = requests.get(f"{BASE_URL}/notes/{note_id}")
    assert get_response.status_code == 404


############################################
### Filter tests
############################################


def test_filter_by_category():
    """Test filtering notes by category"""
    # Create a note with specific category
    note_data = {
        "title": "Work Note",
        "content": "Work content",
        "category": "work",
        "tags": []
    }
    requests.post(f"{BASE_URL}/notes", json=note_data)

    response = requests.get(f"{BASE_URL}/notes?category=work")

    assert response.status_code == 200
    notes = response.json()
    for note in notes:
        assert note["category"] == "work"


def test_filter_by_search():
    """Test filtering notes by search term"""
    # Create a note with specific content
    note_data = {
        "title": "Unique Search Term XYZ",
        "content": "Some content",
        "category": "study",
        "tags": []
    }
    requests.post(f"{BASE_URL}/notes", json=note_data)

    response = requests.get(f"{BASE_URL}/notes?search=Unique Search Term XYZ")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_filter_by_tag():
    """Test filtering notes by tag"""
    # Create a note with specific tag
    note_data = {
        "title": "Tagged Note",
        "content": "Content",
        "category": "work",
        "tags": ["special-tag"]
    }
    requests.post(f"{BASE_URL}/notes", json=note_data)

    response = requests.get(f"{BASE_URL}/notes?tag=special-tag")

    assert response.status_code == 200
    assert len(response.json()) >= 1


############################################
### Error tests
############################################


def test_get_nonexistent_note():
    """Test getting a note that does not exist"""
    response = requests.get(f"{BASE_URL}/notes/99999")

    assert response.status_code == 404


def test_update_nonexistent_note():
    """Test updating a note that does not exist"""
    updated_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "category": "work",
        "tags": []
    }
    response = requests.put(f"{BASE_URL}/notes/99999", json=updated_data)

    assert response.status_code == 404


def test_delete_nonexistent_note():
    """Test deleting a note that does not exist"""
    response = requests.delete(f"{BASE_URL}/notes/99999")

    assert response.status_code == 404


def test_create_note_missing_field():
    """Test creating a note with missing required field"""
    invalid_data = {
        "title": "Only title"
        # missing content and category
    }
    response = requests.post(f"{BASE_URL}/notes", json=invalid_data)

    assert response.status_code == 422


############################################
### Stats and tags tests
############################################


def test_get_stats():
    """Test getting notes statistics"""
    response = requests.get(f"{BASE_URL}/notes/stats")

    assert response.status_code == 200
    data = response.json()
    assert "total_notes" in data
    assert "by_category" in data
    assert "top_tags" in data
    assert "unique_tags_count" in data


def test_list_tags():
    """Test listing all tags"""
    response = requests.get(f"{BASE_URL}/tags")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_categories():
    """Test listing all categories"""
    response = requests.get(f"{BASE_URL}/categories")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


if __name__ == "__main__":
    test_get_root()
    test_get_status()
    test_get_about()
    test_create_note()
    test_list_notes()
    test_get_note_by_id()
    test_update_note()
    test_partial_update_note()
    test_delete_note()
    test_filter_by_category()
    test_filter_by_search()
    test_filter_by_tag()
    test_get_nonexistent_note()
    test_update_nonexistent_note()
    test_delete_nonexistent_note()
    test_create_note_missing_field()
    test_get_stats()
    test_list_tags()
    test_list_categories()
    print("All tests passed!")
    