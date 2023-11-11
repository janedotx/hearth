from fastapi.testclient import TestClient

from repository import chromaClient, default_ef, setup2


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
setup2(chromaClient, default_ef)
from main import app
client = TestClient(app)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Hello": "world"
    }
