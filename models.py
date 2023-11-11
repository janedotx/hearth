from typing import List, Optional
from pydantic import BaseModel, Field

class Document(BaseModel):
  document: str
  metadata: dict
  id_str: str

class Query(BaseModel):
  query_texts: List[str]
  n_results: Optional[int | None] = Field(None)
  where: Optional[dict | None] = Field(None)
