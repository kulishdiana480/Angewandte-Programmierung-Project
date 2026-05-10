import requests

BASE_URL = "http://127.0.0.1:8000"


def test_create_note_rejects_short_title():
    """Test that title shorter than 3 chars is rejected"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "ab",
        "content": "Some content",
        "category": "general",
        "tags": []
    })
    assert response.status_code == 422


def test_create_note_rejects_empty_title():
    """Test that empty title is rejected"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "",
        "content": "Some content",
        "category": "general",
        "tags": []
    })
    assert response.status_code == 422


def test_create_note_rejects_unknown_category():
    """Test that unknown category is rejected"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Test Note",
        "content": "Some content",
        "category": "banana",
        "tags": []
    })
    assert response.status_code == 422


def test_create_note_normalizes_category():
    """Test that category is normalized to lowercase"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Test Note",
        "content": "Some content",
        "category": "WORK",
        "tags": ["work"]
    })
    assert response.status_code == 201
    assert response.json()["category"] == "work"


def test_create_note_normalizes_tags():
    """Test that tags are normalized to lowercase and deduplicated"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Test Note",
        "content": "Some content",
        "category": "personal",
        "tags": ["URGENT", "urgent", "  meeting  "]
    })
    assert response.status_code == 201
    tags = response.json()["tags"]
    assert "urgent" in tags
    assert "meeting" in tags
    assert tags.count("urgent") == 1


def test_create_note_forbids_extra_fields():
    """Test that extra fields are rejected"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Test Note",
        "content": "Some content",
        "category": "general",
        "tags": [],
        "tagz": ["typo"]
    })
    assert response.status_code == 422


def test_work_note_requires_work_tag():
    """Test that work notes must include work tag"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Work Note",
        "content": "Some content",
        "category": "work",
        "tags": ["meeting"]
    })
    assert response.status_code == 422


def test_work_note_with_work_tag_succeeds():
    """Test that work note with work tag is accepted"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Work Note",
        "content": "Some content",
        "category": "work",
        "tags": ["work", "meeting"]
    })
    assert response.status_code == 201


def test_patch_with_empty_body_succeeds():
    """Test that PATCH with empty body succeeds"""
    # First create a note
    create_response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Note to patch",
        "content": "Original content",
        "category": "personal",
        "tags": []
    })
    note_id = create_response.json()["id"]

    # Patch with empty body
    response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={})
    assert response.status_code == 200


def test_patch_with_invalid_title_fails():
    """Test that PATCH with invalid title fails"""
    # First create a note
    create_response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Note to patch",
        "content": "Original content",
        "category": "personal",
        "tags": []
    })
    note_id = create_response.json()["id"]

    # Patch with invalid title
    response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={
        "title": ""
    })
    assert response.status_code == 422


def test_create_note_rejects_empty_tag():
    """Test that empty tags are rejected"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Test Note",
        "content": "Some content",
        "category": "general",
        "tags": [""]
    })
    assert response.status_code == 422


def test_create_note_rejects_too_short_tag():
    """Test that tags shorter than 2 chars are rejected"""
    response = requests.post(f"{BASE_URL}/notes", json={
        "title": "Test Note",
        "content": "Some content",
        "category": "general",
        "tags": ["a"]
    })
    assert response.status_code == 422


if __name__ == "__main__":
    test_create_note_rejects_short_title()
    test_create_note_rejects_empty_title()
    test_create_note_rejects_unknown_category()
    test_create_note_normalizes_category()
    test_create_note_normalizes_tags()
    test_create_note_forbids_extra_fields()
    test_work_note_requires_work_tag()
    test_work_note_with_work_tag_succeeds()
    test_patch_with_empty_body_succeeds()
    test_patch_with_invalid_title_fails()
    test_create_note_rejects_empty_tag()
    test_create_note_rejects_too_short_tag()
    print("All validation tests passed!")