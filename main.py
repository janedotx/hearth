from typing import Union
from fastapi import FastAPI
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

from consts import PATH_TO_DB, COLLECTION_NAME
from models import Document, Query

chromaClient = chromadb.PersistentClient(path=PATH_TO_DB, settings = Settings(allow_reset = True))
default_ef = embedding_functions.DefaultEmbeddingFunction()
collection = chromaClient.get_collection(name=COLLECTION_NAME, embedding_function=default_ef)

# uvicorn main:app --host 0.0.0.0 --port 80


app = FastAPI()

@app.get("/")
def read_root():
  return "To add a new document, POST to /document. To do a similarity query, GET /similarity_query"

@app.post("/document")
def add_document(document: Document):
  old = collection.count()
  collection.add(documents = [document.document], 
    metadatas = [document.metadata],
    ids = [document.id_str])
  return { 'old': old, 'new': collection.count() }

@app.post("/similarity_query")
def query_document_similarity(query: Query):
  result = collection.query(
    query_texts = query.query_texts,
    n_results = query.n_results if query.n_results else 5,
    where = query.where if query.where else {}
    )
  print('in app method')
  print(result)
  return result
