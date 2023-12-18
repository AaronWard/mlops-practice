import azure.functions as func
import fastapi
app = fastapi.FastAPI()

@app.get("/sample")
async def index():
    return {
        "info": "Newgrange is older than the Pyramids of Giza",
    }
