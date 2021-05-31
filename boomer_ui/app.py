from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse
from boomer import boomer, algorithm_infos
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="boomer_ui/static"), name="static")
templates = Jinja2Templates(directory="boomer_ui/templates")


@app.get("/")
async def root(request: Request):
    infos = algorithm_infos()

    return templates.TemplateResponse(
        "index.html", {"request": request, "algo_infos": infos}
    )


@app.get("/boomerify")
async def boomerify(request: Request):
    text = request.query_params["text"]
    cfg = json.loads(request.query_params["cfg"])

    valid_names = {a.name for a in algorithm_infos()}
    boomer_cfg = {}

    for algo_name, algo_perc in cfg.items():
        if algo_name not in valid_names:
            raise RuntimeError(f"invalid algo name: {algo_name}")

        algo_perc = int(algo_perc)

        if algo_perc < 0 or algo_perc > 100:
            raise RuntimeError("invalid algo percentage value")

        algo_weights = [algo_perc, 100 - algo_perc]
        boomer_cfg[algo_name] = algo_weights

    return boomer(text, algo_cfgs=boomer_cfg)


def main():
    import uvicorn

    uvicorn.run(
        "boomer_ui.app:app", host="127.0.0.1", port=5000, log_level="info", reload=True
    )
