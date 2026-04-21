import csv
import io
import uuid
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from models.result import SessionStartRequest, TrialResult
from trial_generator import generate_all_trials

app = FastAPI(title="ProbWeightingApp API")

# CORS: 開発環境 + Render デプロイ URL
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "https://probweightingapp.onrender.com",  # Render フロントエンド
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# インメモリストレージ（本番ではDBに置き換え）
sessions: dict[str, dict[str, Any]] = {}
results: list[dict[str, Any]] = []


# ---------------------------------------------------------------------------
# POST /api/session/start
# ---------------------------------------------------------------------------
@app.post("/api/session/start")
def start_session(req: SessionStartRequest):
    if not req.student_id.strip() or not req.name.strip():
        raise HTTPException(status_code=400, detail="student_id と name は必須です")

    session_id = str(uuid.uuid4())
    trials = generate_all_trials()
    sessions[session_id] = {
        "student_id": req.student_id.strip(),
        "name": req.name.strip(),
        "trials": trials,
        "created_at": datetime.now().isoformat(),
    }
    return {"session_id": session_id, "trials": trials}


# ---------------------------------------------------------------------------
# POST /api/results
# ---------------------------------------------------------------------------
@app.post("/api/results")
def save_result(result: TrialResult):
    if result.session_id not in sessions:
        raise HTTPException(status_code=404, detail="セッションが見つかりません")

    record = result.model_dump()
    record["Timestamp"] = datetime.now().isoformat()
    results.append(record)
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# GET /api/results/{student_id}/csv
# ---------------------------------------------------------------------------
CSV_COLUMNS = [
    "StudentID", "Name", "Trial", "Block", "N",
    "p", "q", "r", "x", "x_prime",
    "y", "s", "y_prime",
    "pN", "qN", "rN", "sN",
    "choice", "ci_satisfied", "Timestamp",
]

FIELD_MAP = {
    "StudentID": "student_id",
    "Name": "name",
    "Trial": "trial",
    "Block": "block",
    "N": "N",
    "p": "p",
    "q": "q",
    "r": "r",
    "x": "x",
    "x_prime": "x_prime",
    "y": "y",
    "s": "s",
    "y_prime": "y_prime",
    "pN": "pN",
    "qN": "qN",
    "rN": "rN",
    "sN": "sN",
    "choice": "choice",
    "ci_satisfied": "ci_satisfied",
    "Timestamp": "Timestamp",
}


@app.get("/api/results/{student_id}/csv")
def download_csv(student_id: str):
    student_results = [r for r in results if r.get("student_id") == student_id]
    if not student_results:
        raise HTTPException(status_code=404, detail="該当する結果が見つかりません")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ProbWeighting_{student_id}_{timestamp}.csv"

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for r in student_results:
        row = {col: r.get(FIELD_MAP[col], "") for col in CSV_COLUMNS}
        writer.writerow(row)

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------------------------------------------------------------------------
# GET /api/results/summary
# ---------------------------------------------------------------------------
@app.get("/api/results/summary")
def get_summary():
    if not results:
        return {"total_trials": 0, "ci_rate_overall": None, "by_block": {}, "by_N": {}}

    total = len(results)
    ci_count = sum(1 for r in results if r.get("ci_satisfied"))

    by_block: dict[str, dict] = {}
    by_N: dict[str, dict] = {}

    for r in results:
        block_key = str(r["block"])
        n_key = str(r["N"])

        if block_key not in by_block:
            by_block[block_key] = {"total": 0, "ci_count": 0}
        by_block[block_key]["total"] += 1
        if r.get("ci_satisfied"):
            by_block[block_key]["ci_count"] += 1

        if n_key not in by_N:
            by_N[n_key] = {"total": 0, "ci_count": 0}
        by_N[n_key]["total"] += 1
        if r.get("ci_satisfied"):
            by_N[n_key]["ci_count"] += 1

    return {
        "total_trials": total,
        "ci_rate_overall": round(ci_count / total, 4) if total else None,
        "by_block": {
            k: {
                **v,
                "ci_rate": round(v["ci_count"] / v["total"], 4) if v["total"] else None,
            }
            for k, v in by_block.items()
        },
        "by_N": {
            k: {
                **v,
                "ci_rate": round(v["ci_count"] / v["total"], 4) if v["total"] else None,
            }
            for k, v in by_N.items()
        },
    }
