# api.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import io
import math

from engine.parser import load_all
from engine.nsga2 import run_nsga2
from engine.fatigue_model import compute_all_fatigue, get_fatigue_label
from ml.burnout_model import predict_burnout_30days, train_burnout_model, get_model_stats

app = FastAPI(title="NurseGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS = {
    "admin":   {"password": "admin123",   "role": "Admin"},
    "nurse1":  {"password": "nurse123",   "role": "Nurse"},
    "manager": {"password": "manager123", "role": "Manager"},
}

def safe_float(val, default=0.0):
    """Convert value to float, replacing nan/inf with default"""
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return default
        return f
    except Exception:
        return default

def safe_int(val, default=0):
    return int(safe_float(val, default))

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def login(req: LoginRequest):
    user = USERS.get(req.username)
    if user and user["password"] == req.password:
        return {"success": True, "role": user["role"], "username": req.username}
    return {"success": False, "message": "Invalid credentials"}

@app.get("/api/dataset-stats")
def dataset_stats():
    return get_model_stats()

@app.post("/api/train-model")
def train_model():
    train_burnout_model()
    return {"success": True, "message": "Model trained successfully"}

@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    return {
        "success": True,
        "rows":    len(df),
        "columns": list(df.columns),
        "preview": df.head(5).to_dict(orient="records")
    }

class GARequest(BaseModel):
    generations: int = 50
    pop_size:    int = 30

@app.post("/api/generate-schedule")
def generate_schedule(req: GARequest):
    sc, weeks, hist = load_all(
        "data/inrc2", "Sc-n030w4.txt",
        [f"WD-n030w4-{i}.txt" for i in range(4)],
        "H0-n030w4-0.txt"
    )
    best, objectives = run_nsga2(
        sc, weeks, total_days=28,
        pop_size=req.pop_size,
        generations=req.generations
    )
    fatigue     = compute_all_fatigue(best)
    avg_fatigue = safe_float(sum(fatigue.values()) / max(len(fatigue), 1), 0.0)
    avg_fatigue = round(avg_fatigue, 1)
    high_risk   = sum(1 for v in fatigue.values() if safe_float(v) >= 60)

    app.state.schedule = best
    app.state.fatigue  = fatigue

    return {
        "success":      True,
        "avg_fatigue":  avg_fatigue,
        "high_risk":    high_risk,
        "total_nurses": len(fatigue)
    }

@app.get("/api/schedule")
def get_schedule():
    if not hasattr(app.state, "schedule"):
        return {"error": "No schedule generated yet"}
    schedule = app.state.schedule
    DAYS     = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] * 4
    rows     = []
    for nid, shifts in list(schedule.items()):
        for d, shift in enumerate(shifts):
            rows.append({
                "nurse": nid,
                "day":   f"W{d//7+1}-{DAYS[d]}",
                "shift": shift
            })
    violations = []
    for nid, shifts in schedule.items():
        for i in range(len(shifts) - 1):
            if shifts[i] == "Night" and shifts[i+1] in ["Early", "Day"]:
                violations.append({
                    "nurse": nid,
                    "issue": f"Night → {shifts[i+1]}",
                    "day":   f"Day {i+1} → {i+2}"
                })
    return {"schedule": rows, "violations": violations}

@app.get("/api/fatigue")
def get_fatigue():
    if not hasattr(app.state, "fatigue"):
        return {"error": "No schedule generated yet"}
    fatigue = app.state.fatigue
    result  = []
    for nid, score in fatigue.items():
        score = safe_int(score, 0)
        label, color = get_fatigue_label(score)
        result.append({
            "nurse": nid,
            "score": score,
            "risk":  label,
            "color": color
        })
    return {
        "nurses":   result,
        "high":     sum(1 for r in result if r["risk"] == "High Risk"),
        "moderate": sum(1 for r in result if r["risk"] == "Moderate"),
        "low":      sum(1 for r in result if r["risk"] == "Low"),
    }

@app.get("/api/burnout")
def get_burnout():
    if not hasattr(app.state, "schedule"):
        return {"error": "No schedule generated yet"}
    predictions = predict_burnout_30days(app.state.schedule)
    result = []
    for nid, risk in predictions.items():
        risk = round(safe_float(risk, 50.0), 1)
        result.append({
            "nurse": nid,
            "risk":  risk,
            "level": "High" if risk > 70 else "Moderate" if risk > 40 else "Low"
        })
    result.sort(key=lambda x: x["risk"], reverse=True)
    return {"predictions": result}