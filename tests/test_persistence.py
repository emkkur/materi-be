from pathlib import Path
from app.services import DocumentService
from app.models import DocumentCreate
import json

DATA_FILE = Path("data.json")


def test_persistence():
    # Setup: Ensure clear state
    if DATA_FILE.exists():
        DATA_FILE.unlink()

    print("Step 1: Create service and add document")
    service1 = DocumentService()
    doc_create = DocumentCreate(title="Persistent Doc", content="Should be saved")
    doc1 = service1.create_document(doc_create)

    print("Step 2: Verify data.json created and has content")
    assert DATA_FILE.exists()
    with open(DATA_FILE) as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["id"] == str(doc1.id)
        assert data[0]["title"] == "Persistent Doc"
        print("✅ File persistence verified")

    print("Step 3: Create new service instance (simulating restart)")
    service2 = DocumentService()
    doc2 = service2.get_document(doc1.id)

    assert doc2 is not None
    assert doc2.title == "Persistent Doc"
    assert doc2.id == doc1.id
    print("✅ Data loading verified")

    # Cleanup
    if DATA_FILE.exists():
        DATA_FILE.unlink()
    print("Test passed!")


if __name__ == "__main__":
    test_persistence()
