import os
import fastapi
import azure.functions as func

app = fastapi.FastAPI()
@app.get("/sample")
async def index():
    return {
        "info": "Pyramids of Giza are older than the Eiffel tower",
    }

@app.get("/privacy_policy")
async def privacy_policy():
    # Read privacy_policy.txt file
    with open('./ApiFunction/privacy_policy.txt', 'r') as file:
        privacy_policy_content = file.read()

    return {
        "info": privacy_policy_content
    }