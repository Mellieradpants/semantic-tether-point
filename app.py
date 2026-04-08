from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    text: str

@app.post("/analyze")
def analyze(data: Input):
    text = data.text

    # TEMP — replace with your engine
    result = {
        "received_text": text,
        "status": "engine not connected yet"
    }

    return result
