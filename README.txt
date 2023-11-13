Overview:
This project supports adding documents to a Chroma vector database and querying for document
similarity, via two HTTP endpoints implemented in FastAPI and hosted by uvicorn. The motivation
for choosing Chroma was that it came with a set of embeddings and would not require interfacing
with an external embedding provider. 

Setup and running:

1. Install pyenv.
2. Use pyenv to install Python 3.10.13, as the Chroma client will not work 
with later versions of Python.
3. Run `pip install -r requirements.txt`.
4. To start the uvicorn server, run `uvicorn main:app --host 0.0.0.0 --port`.
5. You can now interact with the Chroma database by issuing HTTP requests. 
  a. Example curl request to add a document:
    `curl -X POST http:/0.0.0.0:3000/document -H "Content-Type: application/json" -H  "Accept: application/json" -d '{ "document": "artificialasdfdd", "id_str": "id_artificialasdfdd", "metadata": { "animal": "False"  }}'`
  b. Example curl request to do a query:
    `curl -X POST http:/0.0.0.0:3000/similarity_query -H "Content-Type: application/json"
       -H  "Accept: application/json"
       -d '{ 
          "query_texts": ["unnatural"], "where": { "animal": 0 
          }}'`

To run the service in a container:
1. Run `docker build -t hearth .`
2. Run `docker run -dp 127.0.0.1:3000:3000 hearth`.
3. The service should now be accessible at localhost:3000.


For thoughts on future directions to take this project and enhancements to add, see questions.txt.