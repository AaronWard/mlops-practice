import azure.functions as func
import fastapi
import os
app = fastapi.FastAPI()

@app.get("/sample")
async def index():
    return {
        "info": "Pyramids of Giza are older than the Eiffel tower",
    }

@app.get("/privacy_policy")
async def privacy_policy():
    # Read privacy_policy.txt file
    # with open('privacy_policy.txt', 'r') as file:
    #     privacy_policy_content = file.read()

    return {
        "info": os.getcwd()
    }