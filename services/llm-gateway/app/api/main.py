"""
API v0.1 - HTTP доступ к судье
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
from pathlib import Path

# Добавляем пути для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.judge import judge

app = FastAPI(
    title="AURORA Cognitive Control Plane",
    description="Sphinx + Enigma  смысловой брандмауэр и законы",
    version="0.1.0"
)

class QueryRequest(BaseModel):
    prompt: str
    context: Optional[Dict[str, Any]] = None
    simulate: bool = False

class QueryResponse(BaseModel):
    prompt: str
    final_decision: str
    final_reason: str
    risk_score: float
    sphinx_report: Dict
    enigma_verdict: Dict

@app.get("/")
def root():
    return {
        "service": "AURORA Cognitive Control Plane",
        "modules": ["sphinx", "enigma", "judge"],
        "status": "active"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/v1/judge", response_model=QueryResponse)
def judge_request(request: QueryRequest):
    """
    Вынести суждение о запросе:
    - Sphinx анализирует смысл
    - Enigma применяет законы
    - Возвращается решение
    """
    try:
        result = judge.judge(request.prompt, request.context)
        return QueryResponse(
            prompt=result["prompt"],
            final_decision=result["final_decision"],
            final_reason=result["final_reason"],
            risk_score=result["risk_score"],
            sphinx_report=result["sphinx"],
            enigma_verdict=result["enigma"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/stats")
def get_stats():
    """Статистика работы судьи"""
    return judge.get_stats()

@app.get("/v1/laws")
def get_laws():
    """Список законов Enigma"""
    return {"laws": judge.enigma.laws}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
