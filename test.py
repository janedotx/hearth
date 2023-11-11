from fastapi.testclient import TestClient

from repository import chromaClient, default_ef, seedDB


import os
'''
allow_reset = None
if "ALLOW_RESET" in os.environ:
  allow_reset = os.environ["ALLOW_RESET"]
else:
  allow_reset = "FALSE"

os.environ["ALLOW_RESET"] = "TRUE"

os.environ["ALLOW_RESET"] = allow_reset

'''
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
  assert response_json == { "old": 9, "new": 10}

def test_post_document_invalid_path_one():
  response = client.post("/document",
    headers = { "Content-Type": "application/json" },
    json = { 
      "document": "fluorescent",
      "metadata": { "animal": "False" }
    }
    )
  assert response.status_code == 422

def test_post_document_invalid_path_two():
  response = client.post("/document",
    headers = { "Content-Type": "application/json" },
    json = { 
      "document": "fluorescent",
      "id_str": "id_fluorescent"
    }
    )
  assert response.status_code == 422

def test_post_document_invalid_path_three():
  response = client.post("/document",
    headers = { "Content-Type": "application/json" },
    json = { 
      "metadata": { "animal": "False" },
      "id_str": "id_fluorescent"
    }
    )
  assert response.status_code == 422

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
  assert len(response_json["ids"][0]) == 2
  for result in response_json["metadatas"][0]:
    assert result["sound_effect"]

def test_query_document_similarity_optional_params():
  response = client.post("/similarity_query", 
    headers = { "Content-Type": "application/json" },
    json = { 
      "query_texts": [ "animal" ]
    }
  )
  assert response.status_code == 200
  assert len(response.json()["ids"][0]) == 5