# Import necessary libraries
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from typing import List
import azure.functions as func

from chromadb.api import ClientAPI as API

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from chromadb.api.types import QueryResult

# Initialize FastAPI app
app = FastAPI()

print(os.getcwd())

# Define the path to the ChromaDB SQLite file
# db_path = str(Path(os.getcwd(), "./ApiFunction/chromadb/chroma.sqlite3").expanduser())
db_path = "./ApiFunction/chromadb/"
print(db_path)

client = chromadb.PersistentClient(path=db_path)
collection_names = client.list_collections()
print(collection_names)


# Define the query function
def query_vector_db(query_texts: List[str], n_results: int = 10, search_string: str = "") -> QueryResult:
    collection_name = "autogen-discord"  
    embedding_model = "all-MiniLM-L6-v2" 

    # Initialize embedding function
    embedding_function = SentenceTransformerEmbeddingFunction(embedding_model)
    query_embeddings = embedding_function(query_texts)

    # Fetch collection
    collection = client.get_collection(collection_name)

    # Query collection
    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=n_results,
        where_document={"$contains": search_string} if search_string else None,
    )
    return results

# Define FastAPI endpoints
@app.get("/sample")
async def index():
    return {"info": "Sample response"}

@app.get("/query/{query_text}")
async def query(query_text: str):
    try:
        # Query the ChromaDB database
        results = query_vector_db([query_text])
        return {"documents": results['documents']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/privacy_policy")
async def privacy_policy():
    try:
        with open('./ApiFunction/privacy_policy.txt', 'r') as file:
            privacy_policy_content = file.read()
        return {"info": privacy_policy_content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Privacy policy not found.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)