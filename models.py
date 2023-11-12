from typing import List, Optional
from pydantic import BaseModel, Field

# Document class
class Document(BaseModel):
  document: str
  metadata: dict
  id_str: str

# Query class for similarity queries
class Query(BaseModel):
  query_texts: List[str]
  n_results: Optional[int | None] = Field(None)
  where: Optional[dict | None] = Field(None)
