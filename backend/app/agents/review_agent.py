import json
import re

from app.services.llm_service import generate_gemini_text


JSON_BLOCK_PATTERN = re.compile(r"\{.*\}", re.DOTALL)


def _parse_review_payload(review_text: str) -> dict:
    match = JSON_BLOCK_PATTERN.search(review_text)
    if not match:
        return {
            "final_summary": review_text.strip(),
            "confidence": 0.75,
            "risk": "medium",
            "next_actions": [
                "Validate the recommendation against the real codebase",
                "Run targeted verification before rollout"
            ]
        }

    try:
        parsed = json.loads(match.group(0))
        confidence = parsed.get("confidence", 0.75)
        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.75

        return {
            "final_summary": parsed.get("summary", review_text.strip()),
            "confidence": max(0.0, min(confidence, 1.0)),
            "risk": str(parsed.get("risk", "medium")).lower(),
            "next_actions": parsed.get("next_actions", [
                "Validate the recommendation against the real codebase",
                "Run targeted verification before rollout"
            ])
        }
    except json.JSONDecodeError:
        return {
            "final_summary": review_text.strip(),
            "confidence": 0.75,
            "risk": "medium",
            "next_actions": [
                "Validate the recommendation against the real codebase",
                "Run targeted verification before rollout"
            ]
        }


def run_review_agent(
    issue: dict,
    planner_data: dict,
    retrieval_data: dict,
    analysis_data: dict,
    patch_data: dict
) -> dict:
    issue_type = issue.get("issue_type", "bug")
    project_name = issue.get("project_name", "unknown project")
    error_summary = issue.get("error_summary", "")
    analysis_text = analysis_data.get("analysis", "")
    patch_text = patch_data.get("patch_preview", "")
    retrieval_hits = retrieval_data.get("memory_hits", {})

    prompt = f"""
You are an expert software engineering review agent.

Return ONLY valid JSON with this exact shape:
{{
  "summary": "short review of whether the solution is reasonable",
  "confidence": 0.0,
  "risk": "low",
  "next_actions": ["step one", "step two"]
}}

Rules:
- confidence must be a number between 0.0 and 1.0
- risk must be one of: low, medium, high
- next_actions must contain exactly 2 concise validation steps
- do not use markdown code fences

Issue type: {issue_type}
Project name: {project_name}
Error summary: {error_summary}

Planner summary:
{planner_data.get("summary", "")}

Retrieval summary:
{retrieval_data.get("summary", "")}
SQLite hits: {len(retrieval_hits.get("sqlite", []))}
Pinecone hits: {len(retrieval_hits.get("pinecone", []))}

Analysis:
{analysis_text}

Patch suggestion:
{patch_text}
"""

    review_text = generate_gemini_text(prompt)
    parsed = _parse_review_payload(review_text)

    return {
        "agent": "Review Agent",
        "issue_type": issue_type,
        "task": "Review the proposed solution",
        "final_summary": parsed["final_summary"],
        "confidence": parsed["confidence"],
        "risk": parsed["risk"],
        "next_actions": parsed["next_actions"],
        "workflow_trace": {
          "planner": planner_data.get("summary"),
          "retrieval": retrieval_data.get("summary"),
          "analysis": analysis_data.get("summary"),
          "patch": patch_data.get("summary")
        },
        "raw_review": review_text
    }
