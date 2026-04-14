from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pipeline.run_pipeline import run_pipeline

app = FastAPI(title="Traceability Constraint System API")


class AnalyzeRequest(BaseModel):
    content: str = Field(..., description="Raw input content")
    input_type: str = Field(..., description="One of: text, xml, json, html")


@app.get("/")
def root():
    return {"status": "TCS backend running"}


@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    allowed_types = {"text", "xml", "json", "html"}

    if data.input_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_input_type",
                "allowed": sorted(allowed_types),
            },
        )

    suffix_map = {
        "text": ".txt",
        "xml": ".xml",
        "json": ".json",
        "html": ".html",
    }

    tmp_path = None

    try:
        with NamedTemporaryFile(
            mode="w",
            suffix=suffix_map[data.input_type],
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write(data.content)
            tmp_path = Path(tmp.name)

        result = run_pipeline(data.content)
        return result

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "analysis_failed",
                "message": str(exc),
            },
        )
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink()