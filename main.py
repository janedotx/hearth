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
  return { "Hello": "world" }

@app.post("/document")
def add_document(document: Document):
  old = collection.count()
  collection.add(documents = [document.document], 
    metadatas = [document.metadata],
    ids = [document.id_str])
  return { 'old': old, 'new': collection.count() }

@app.get("/similarity_query")
def query_document_similarity(query: Query):
  return collection.query(
    query_texts = query.query_texts,
    n_results = query.n_results,
    where = query.where
    )
