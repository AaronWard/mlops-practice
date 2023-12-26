# Import necessary libraries
import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from typing import List
import azure.functions as func

try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3
sys.modules['sqlite3'] = sqlite3

from chromadb.api import ClientAPI as API
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from chromadb.api.types import QueryResult

# Initialize FastAPI app
app = FastAPI()

# Define vars for ChromaDB SQLite 
collection_name = "autogen-docs-qa"
embedding_model = "all-MiniLM-L6-v2"
db_path = "./ApiFunction/chromadb/"

try:
    client = chromadb.PersistentClient(path=db_path)
except Exception as e:
    raise Exception(f"Chroma client couldn't be instantiated: {e}")

collection_names = client.list_collections()
embedding_function = SentenceTransformerEmbeddingFunction(embedding_model)

print(db_path)
print(collection_names)
print(embedding_model)

# Define the query function
def query_vector_db(query_texts: List[str], n_results: int = 10, search_string: str = "") -> QueryResult:
    query_embeddings = embedding_function(query_texts)
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
    return {"info": "Sample "}

@app.get("/query/{query_text}")
async def query(query_text: str):
    print(query_text)
    try:
        results = query_vector_db([query_text])
        return {"documents": results['documents']}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/privacy_policy")
async def privacy_policy():
    try:
        # Use a more secure method to join paths
        privacy_policy_path = Path(__file__).parent / 'privacy_policy.txt'
        with privacy_policy_path.open('r') as file:
            privacy_policy_content = file.read()
        return {"info": privacy_policy_content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Privacy policy not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)