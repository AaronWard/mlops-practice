import os
import logging
from fastapi import FastAPI, HTTPException
from typing import List
import azure.functions as func
from chromadb.api import ClientAPI as API

# Initialize FastAPI app
app = FastAPI()

# Define the path to the ChromaDB SQLite file
db_path = './ApiFunction/chromadb/chroma.sqlite3'

# Initialize the ChromaDB API client
# Make sure the SQLite file is included in your deployment package
if not os.path.isfile(db_path):
    raise Exception("Database file not found. Ensure it's included in the deployment package.")
client = API(db_path)

@app.get("/sample")
async def index():
    return {
        "info": "Pyramids of Giza are older than the Eiffel tower",
    }

@app.get("/query/{query_text}")
async def query(query_text: str):
    try:
        # Query the ChromaDB database
        results = client.query(query_texts=[query_text], n_results=10)
        # Process and return the results
        # Adapt this according to the actual structure of your results
        logging.info(results)
        return {
            "documents": results['documents']
        }
    except Exception as e:
        logging.info(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/privacy_policy")
async def privacy_policy():
    try:
        # Ensure the file path is correct relative to the root of your Azure Function app
        with open('./ApiFunction/privacy_policy.txt', 'r') as file:
            privacy_policy_content = file.read()
        return {
            "info": privacy_policy_content
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Privacy policy not found.")
