from app.services.llm_service import generate_gemini_text


def run_analysis_agent(issue: dict, retrieved_data: dict) -> dict:
    issue_type = issue.get("issue_type", "bug")
    project_name = issue.get("project_name", "unknown project")
    error_summary = issue.get("error_summary", "")
    problem_details = issue.get("problem_details", "")
    code_snippet = issue.get("code_snippet", "")
    retrieved_context = retrieved_data.get("retrieved_context", [])

    prompt = f"""
You are an expert software engineering analysis agent.

Your task is to analyze a developer issue and identify the most likely root cause.

Issue type: {issue_type}
Project name: {project_name}
Error summary: {error_summary}
Problem details: {problem_details}
Code snippet or command:
{code_snippet}

Retrieved context:
{retrieved_context}

Return a short but strong engineering analysis explaining:
1. the most likely root cause
2. what area of the system is likely affected
3. what should be checked next

Keep the answer concise and practical.
"""

    analysis_text = generate_gemini_text(prompt)

    return {
        "agent": "Analysis Agent",
        "issue_type": issue_type,
        "task": "Identify the likely cause",
        "analysis": analysis_text,
        "retrieval_used": retrieved_context,
        "summary": "Analysis agent completed LLM-powered issue analysis."
    }
