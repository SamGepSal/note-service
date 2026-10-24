import pytest
from fastapi.testclient import TestClient
from app_final import app, notes

client = TestClient(app)
@pytest.fixture(autouse=True)
def reset_notes():
    original_notes = notes.copy()
    notes.clear()

    yield

    notes.clear()
    notes.extend(original_notes)

def test_health(): 
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_note():
    response = client.post(
        "/notes",
        json={"title": "Учёба",
              "text": "тестовая заметка"
              },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Учёба",
        "text": "тестовая заметка",
    }

    list_response = client.get("/notes")
    assert list_response.status_code == 200
    assert list_response.json() == [response.json()]

def test_get_note():
    created = client.post(
        "/notes", 
        json={"title": "Покупки", "text": "Купить хлеб"},
    )
    assert created.status_code == 201
    note_id = created.json()["id"]

    response = client.get(f"/notes/{note_id}")

    assert response.status_code == 200
    assert response.json() == created.json()

def test_note_not_found():
    response = client.get("/notes/111")

    assert response.status_code == 404
    assert response.json() == {"detail": "Заметка не найдена"}

def test_invalid_note_id():
    response = client.get("/notes/qwe")

    assert response.status_code == 422