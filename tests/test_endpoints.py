from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)


def test_create_document():
    response = client.post(
        "/document", json={"title": "Test Document", "content": "This is a test document."}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Document"
    assert "id" in data
    return data["id"]


def test_get_document(doc_id):
    response = client.get(f"/document/{doc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == doc_id
    assert data["title"] == "Test Document"


def test_list_documents(doc_id):
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(d["id"] == doc_id for d in data)


def test_update_document(doc_id):
    response = client.patch(f"/document/{doc_id}", json={"title": "Updated Title"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "This is a test document."


def test_delete_document(doc_id):
    response = client.delete(f"/document/{doc_id}")
    assert response.status_code == 204

    response = client.get(f"/document/{doc_id}")
    assert response.status_code == 404


def run_tests():
    print("Running endpoint tests...")
    # Clean up data.json before starting
    if os.path.exists("data.json"):
        os.remove("data.json")
        # Reload service to pick up empty state?
        # The service loads in __init__. TestClient(app) initializes app which initializes service.
        # But if app is already imported, service is already initialized.
        # So we might need to manually clear the service.
        from app.main import document_service

        document_service.documents = {}
        document_service._save_documents()

    try:
        doc_id = test_create_document()
        print("✅ test_create_document passed")

        test_get_document(doc_id)
        print("✅ test_get_document passed")

        test_list_documents(doc_id)
        print("✅ test_list_documents passed")

        test_update_document(doc_id)
        print("✅ test_update_document passed")

        test_delete_document(doc_id)
        print("✅ test_delete_document passed")

        print("All endpoint tests passed!")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if os.path.exists("data.json"):
            os.remove("data.json")


if __name__ == "__main__":
    run_tests()
