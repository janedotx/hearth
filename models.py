from typing import List
from pydantic import BaseModel

class Document(BaseModel):
  document: str
  metadata: dict
  id_str: str

class Query(BaseModel):
  query_texts: List[str]
  n_results: int
  where: dict
