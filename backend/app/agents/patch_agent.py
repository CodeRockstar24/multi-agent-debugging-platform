from app.services.llm_service import generate_gemini_text


def run_patch_agent(issue: dict, analysis_data: dict) -> dict:
    issue_type = issue.get("issue_type", "bug")
    project_name = issue.get("project_name", "unknown project")
    error_summary = issue.get("error_summary", "")
    problem_details = issue.get("problem_details", "")
    code_snippet = issue.get("code_snippet", "")
    analysis_text = analysis_data.get("analysis", "")

    prompt = f"""
You are an expert software engineering patch agent.

Your task is to suggest the best practical fix for this issue.

Issue type: {issue_type}
Project name: {project_name}
Error summary: {error_summary}
Problem details: {problem_details}
Code snippet or command:
{code_snippet}

Analysis from previous agent:
{analysis_text}

Return:
1. a short recommended fix
2. a patch preview or config/workflow improvement
3. one validation step

Keep it practical and concise.
"""

    patch_text = generate_gemini_text(prompt)

    return {
        "agent": "Patch Agent",
        "issue_type": issue_type,
        "task": "Suggest a repair or improvement",
        "patch_preview": patch_text,
        "based_on": analysis_text,
        "summary": "Patch agent prepared an LLM-powered fix suggestion."
    }
