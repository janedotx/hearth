import typing
from pydantic import BaseModel

class Document(BaseModel):
  document: str
  metadata: dict
  id_str: str