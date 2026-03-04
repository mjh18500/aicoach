from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse

from .data_loader import load_persona
from .timeline import build_unified_timeline
from .axes import compute_axis_scores, compute_monthly_axis_scores
from .patterns import detect_momentum_collapse, detect_stress_preceded_collapse
from .insights import generate_monthly_summary
from .state_classifier import classify_state
from .daily_plan_generator import generate_daily_plan

app = FastAPI(title="aicoach API")

# serve static prototype pages
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    try:
        with open("app/static/ai-companion-deepdive.html") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Index page not found")

@app.get("/sage", response_class=HTMLResponse)
def sage():
    try:
        with open("app/static/sage-mockup.html") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Sage page not found")


@app.get("/analyze/{persona_id}")
def analyze(persona_id: str):
    persona = load_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    timeline = build_unified_timeline(persona)
    monthly_scores = compute_monthly_axis_scores(timeline)
    axis_scores = compute_axis_scores(timeline)
    collapses = detect_momentum_collapse(monthly_scores)
    stress_analysis = detect_stress_preceded_collapse(monthly_scores, collapses)
    latest_month = sorted(monthly_scores.keys())[-1] if monthly_scores else None
    summary = (
        generate_monthly_summary(latest_month, monthly_scores, stress_analysis)
        if latest_month
        else ""
    )
    state = classify_state(persona)
    plan = generate_daily_plan(persona)

    return JSONResponse(
        {
            "axis_scores": axis_scores,
            "monthly_scores": monthly_scores,
            "collapses": collapses,
            "stress_analysis": stress_analysis,
            "summary": summary,
            "state": state,
            "plan": plan,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
