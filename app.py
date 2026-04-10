from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI
from pydantic import BaseModel

from engines.semantic_tether_engine import build_traceable_output

app = FastAPI(title="Traceability Constraint System API")


class AnalyzeRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"status": "TCS backend running"}


@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    tmp_path = None

    with NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
        encoding="utf-8",
    ) as tmp:
        tmp.write(data.text)
        tmp_path = Path(tmp.name)

    try:
        result = build_traceable_output(tmp_path)
        return result
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink()
