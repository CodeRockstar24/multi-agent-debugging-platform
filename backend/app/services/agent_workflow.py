from app.agents.planner_agent import run_planner_agent
from app.agents.retrieval_agent import run_retrieval_agent
from app.agents.analysis_agent import run_analysis_agent
from app.agents.patch_agent import run_patch_agent
from app.agents.review_agent import run_review_agent


def run_agent_workflow(issue: dict) -> dict:
    planner_result = run_planner_agent(issue)
    retrieval_result = run_retrieval_agent(issue)

    analysis_attempts = []
    analysis_result = None
    for attempt in range(2):
        analysis_result = run_analysis_agent(issue, retrieval_result)
        analysis_attempts.append(
            {
                "attempt": attempt + 1,
                "status": "completed",
                "summary": analysis_result.get("summary", "")
            }
        )
        analysis_text = analysis_result.get("analysis", "")
        if analysis_text and "failed" not in analysis_text.lower():
            break

    patch_result = run_patch_agent(issue, analysis_result or {})
    patch_text = patch_result.get("patch_preview", "")

    # Lightweight handoff fallback: if patch is weak, use analysis directly as support context
    if len(patch_text.strip()) < 40:
        patch_result["patch_preview"] = (
            "Fallback patch guidance based on analysis:\n"
            + (analysis_result.get("analysis", "No analysis available.") if analysis_result else "No analysis available.")
        )
        patch_result["summary"] = "Patch agent used fallback handoff from analysis."

    review_result = run_review_agent(
        issue,
        planner_result,
        retrieval_result,
        analysis_result or {},
        patch_result,
    )

    return {
        "issue": issue,
        "workflow": {
            "planner": planner_result,
            "retrieval": retrieval_result,
            "analysis": analysis_result,
            "patch": patch_result,
            "review": review_result,
        },
        "autonomy": {
            "branching_used": issue.get("issue_type", "bug"),
            "analysis_attempts": analysis_attempts,
            "memory_enabled": True,
            "fallbacks_enabled": True
        }
    }
