from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import uvicorn
from make_report import generate_report

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
async def search(query: str = Form(...)):
    news_report = generate_report(query)
    return news_report

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)