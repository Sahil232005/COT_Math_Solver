from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import groq

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

GROQ_API_KEY = "enter your api key " 
MODEL_NAME = "llama3-70b-8192"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })

@app.post("/solve")
async def solve_problem(problem: str = Form(...)):
    client = groq.Groq(api_key=GROQ_API_KEY)
    messages = [
        {"role": "system", "content": "Think step by step in no more than 5 words per step. End the response after a separator #### with final answer."},
        {"role": "user", "content": problem}
    ]
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=1,
            max_completion_tokens=1024
        )
        result = response.choices[0].message.content
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
