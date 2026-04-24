from fastapi import APIRouter
from app.models.issue import IssueCreate
from app.services.issue_service import create_issue
from app.services.agent_workflow import run_agent_workflow

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "backend"
    }


@router.get("/agents")
def get_agents():
    return {
        "agents": [
            {"name": "Planner Agent", "role": "Creates an investigation plan"},
            {"name": "Retrieval Agent", "role": "Finds relevant context and memory"},
            {"name": "Analysis Agent", "role": "Identifies likely cause"},
            {"name": "Patch Agent", "role": "Suggests a repair or improvement"},
            {"name": "Review Agent", "role": "Evaluates confidence, risk, and next steps"}
        ]
    }


@router.post("/issues")
def create_new_issue(issue: IssueCreate):
    saved_issue = create_issue(issue)
    return {
        "message": "Issue created successfully",
        "issue": saved_issue
    }


@router.post("/agent-workflow")
def run_workflow(issue: IssueCreate):
    saved_issue = create_issue(issue)
    result = run_agent_workflow(saved_issue)
    return result
