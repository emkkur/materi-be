# Materi Take Home Backend

## 1. Tech Stack

* **Backend**: FastAPI, Python 3.12
* **Persistence**: Local JSON-file storage.

## 2. Backend Setup

### Prerequisites

* **Python**: 3.12 or higher.

### Setup

```bash
cd materi-be
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
python run_server.py

```

*The server will start at `http://127.0.0.1:8000`.*

## 3. API Endpoints

The backend provides a RESTful API for document management:

* `GET /documents`: Returns a list of all document summaries.
  * **Response**: `List[DocumentResponse]`
    ```json
    [
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": "Document Title",
        "content": "...",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ]
    ```

* `POST /document`: Creates a new document.
  * **Request Body**: `DocumentCreate`
    ```json
    {
      "title": "New Document",
      "content": "Serialized Slate JSON content..."
    }
    ```
  * **Response**: `DocumentResponse` (see above structure)

* `GET /document/{id}`: Fetches the full JSON state of a specific document.
  * **Response**: `DocumentResponse`

* `PATCH /document/{id}`: Updates an existing document's title or content.
  * **Request Body**: `DocumentUpdate`
    ```json
    {
      "title": "Updated Title",
      "content": "Updated content..."
    }
    ```
  * **Response**: `DocumentResponse`

* `DELETE /document/{id}`: Removes a document from storage.
  * **Response**: `204 No Content`

## 4. Data Model

Documents are stored in `data.json` with the following schema:

* `id`: UUID string.
* `title`: The name of the document.
* `content`: A JSON-serialized string representing the Slate.js editor state.
* `created_at`: ISO 8601 creation timestamp.
* `updated_at`: ISO 8601 last-update timestamp.