from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse
from boomer import boomer

app = FastAPI()
app.mount("/static", StaticFiles(directory="boomer_ui/static"), name="static")
templates = Jinja2Templates(directory="boomer_ui/templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/boomerify")
async def boomerify(request: Request):
    text = request.query_params["text"]
    return boomer(text)


def main():
    import uvicorn

    uvicorn.run(
        "boomer_ui.app:app", host="127.0.0.1", port=5000, log_level="info", reload=True
    )
