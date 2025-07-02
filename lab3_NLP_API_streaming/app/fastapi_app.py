from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class TextPayload(BaseModel):
    text: str

@app.post("/analyze")
async def analyze(payload: TextPayload):
    text = payload.text
    sentiment = "positive" if "good" in text or "excited" in text else "negative"
    return {"sentiment": sentiment}
