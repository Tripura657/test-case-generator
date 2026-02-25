from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import httpx, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Test Case Generator")

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=10)

class GenerateResponse(BaseModel):
    result: str

@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    )
    payload = {
        "contents": [{"parts": [{"text": req.prompt}]}]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload)
        if r.status_code != 200:
            raise HTTPException(status_code=500, detail="Gemini API error")

        data = r.json()
        text = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        if not text:
            raise HTTPException(status_code=500, detail="No output generated")

        return {"result": text}