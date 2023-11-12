import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

from consts import PATH_TO_DB, COLLECTION_NAME

chromaClient = chromadb.PersistentClient(path = PATH_TO_DB, settings = Settings(allow_reset = True))
default_ef = embedding_functions.DefaultEmbeddingFunction()

# Drop any data already there and recreate the default collection with fixtures.
def seedDB(client, ef):
  client.reset()
  collection = client.create_collection(name=COLLECTION_NAME, embedding_function=ef)
  collection.add(
    documents=["aardvark", "batrachian hound", "chthonic",
      "dromedary", "estivation", "gneiss", 
      "womp womp", "womp", "zyzzyva"
    ], metadatas=[{"animal": 1}, { "animal": 1 }, { "animal": 0},
      {"animal": 1}, { "animal": 0 }, { "animal": 0 },
      { "animal": 0, "sound_effect": 1 }, { "sound_effect": 1 }, { "animal": 1 }
    ], ids = ["id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8", "id9"]
  )
