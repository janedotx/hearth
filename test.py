import os
from fastapi.testclient import TestClient

from repository import chromaClient, default_ef, seedDB

# Clear DB before tests and reseed with known fixtures. 
seedDB(chromaClient, default_ef)

from main import app
client = TestClient(app)

def test_get_root():
  response = client.get("/")
  assert response.status_code == 200

def test_post_document_happy_path():
  response = client.post("/document",
    headers = { "Content-Type": "application/json" },
    json = { 
      "document": "fluorescent",
      "id_str": "id_fluorescent",
      "metadata": { "animal": "False" }
    }
    )
  assert response.status_code == 200
  response_json =  response.json()
  # Number of docs in collection went up
  assert response_json == { "old_count": 9, "new_count": 10}

# Fail if required param not supplied
def test_post_document_invalid_path_one():
  response = client.post("/document",
    headers = { "Content-Type": "application/json" },
    json = { 
      "document": "fluorescent",
      "metadata": { "animal": "False" }
    }
    )
  assert response.status_code == 422

# Fail if required param not supplied
def test_post_document_invalid_path_two():
  response = client.post("/document",
    headers = { "Content-Type": "application/json" },
    json = { 
      "document": "fluorescent",
      "id_str": "id_fluorescent"
    }
    )
  assert response.status_code == 422

# Fail if required param not supplied
def test_post_document_invalid_path_three():
  response = client.post("/document",
    headers = { "Content-Type": "application/json" },
    json = { 
      "metadata": { "animal": "False" },
      "id_str": "id_fluorescent"
    }
    )
  assert response.status_code == 422

# Happy path
def test_query_document_similarity():
  response = client.post("/similarity_query", 
    headers = { "Content-Type": "application/json" },
    json = { 
      "query_texts": [ "womp" ],
      "n_results": 2,
      "where": { "sound_effect": 1 }
    }
  )
  response_json = response.json()
  # Verify we get back only as many results as were requested
  assert len(response_json["ids"][0]) == 2

  # Verify only metadata matching the where clause is returned
  for result in response_json["metadatas"][0]:
    assert result["sound_effect"]

# Validate that the optional parameters can be left out
def test_query_document_similarity_optional_params():
  response = client.post("/similarity_query", 
    headers = { "Content-Type": "application/json" },
    json = { 
      "query_texts": [ "animal" ]
    }
  )
  assert response.status_code == 200
  # Check the response length is 5 since the default 
  # n_results is 5
  assert len(response.json()["ids"][0]) == 5