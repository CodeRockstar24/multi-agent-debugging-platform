from app.services.issue_service import get_similar_issues
from app.services.pinecone_service import query_issue_memory


def run_retrieval_agent(issue: dict) -> dict:
    issue_type = issue.get("issue_type", "bug")
    project_name = issue.get("project_name", "")
    problem_details = issue.get("problem_details", "")
    code_snippet = issue.get("code_snippet", "")

    context_by_type = {
        "bug": [
            "Check business logic, conditionals, and arithmetic operators",
            "Inspect recent function-level changes",
            "Look for missing edge-case handling"
        ],
        "code_review": [
            "Check readability, duplication, and module responsibility",
            "Look for unclear naming and long functions",
            "Inspect maintainability and testability"
        ],
        "test_failure": [
            "Compare expected output with implementation behavior",
            "Check flaky assumptions and bad fixtures",
            "Inspect edge-case test coverage"
        ],
        "api_error": [
            "Check request schema, validation, and route handling",
            "Inspect response shape and status codes",
            "Look for auth or serialization issues"
        ],
        "ci_cd_issue": [
            "Check workflow steps and dependency installation",
            "Inspect environment variables used in pipeline",
            "Review build/test command assumptions"
        ],
        "performance_issue": [
            "Check repeated work, hot paths, and heavy loops",
            "Inspect database or network bottlenecks",
            "Look for caching or batching opportunities"
        ],
        "deployment_issue": [
            "Check startup command and port binding",
            "Inspect environment variables and secrets",
            "Review service connectivity and runtime assumptions"
        ]
    }

    sqlite_hits = get_similar_issues(issue_type, project_name)
    pinecone_hits = query_issue_memory(issue)

    sqlite_context = [
        f"Past issue #{item['id']}: {item['error_summary']}"
        for item in sqlite_hits
    ]

    pinecone_context = [
        f"Semantic match {item['id']}: {item['error_summary']} (score={round(item['score'], 3) if item.get('score') is not None else 'n/a'})"
        for item in pinecone_hits
    ]

    retrieved_context = (
        context_by_type.get(issue_type, context_by_type["bug"])
        + sqlite_context
        + pinecone_context
    )

    return {
        "agent": "Retrieval Agent",
        "issue_type": issue_type,
        "task": "Gather relevant context",
        "retrieved_context": retrieved_context,
        "memory_hits": {
            "sqlite": sqlite_hits,
            "pinecone": pinecone_hits
        },
        "source_excerpt": f"{problem_details}\n{code_snippet}".strip(),
        "summary": (
            f"Retrieval agent gathered context, {len(sqlite_hits)} SQLite memory hits, "
            f"and {len(pinecone_hits)} Pinecone semantic matches for {issue_type}"
        )
    }
