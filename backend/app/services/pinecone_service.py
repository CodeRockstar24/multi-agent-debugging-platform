from pinecone import Pinecone
from app.core.config import settings
from app.services.llm_service import generate_embedding


def get_pinecone_index():
    if not settings.pinecone_api_key:
        return None

    pc = Pinecone(api_key=settings.pinecone_api_key)
    existing = [index["name"] for index in pc.list_indexes()]

    if settings.pinecone_index_name not in existing:
        return None

    return pc.Index(settings.pinecone_index_name)


def upsert_issue_memory(issue: dict):
    index = get_pinecone_index()
    if index is None:
        return {"status": "skipped", "reason": "Pinecone not configured or index missing"}

    text = "\n".join(
        [
            f"Issue type: {issue.get('issue_type', '')}",
            f"Project: {issue.get('project_name', '')}",
            f"Summary: {issue.get('error_summary', '')}",
            f"Details: {issue.get('problem_details', '')}",
            f"Snippet: {issue.get('code_snippet', '')}",
        ]
    ).strip()

    vector = generate_embedding(text)
    if not vector:
        return {"status": "failed", "reason": "Embedding generation failed"}

    issue_id = str(issue.get("id", issue.get("project_name", "unknown")))
    index.upsert(
        vectors=[
            {
                "id": issue_id,
                "values": vector,
                "metadata": {
                    "issue_type": issue.get("issue_type", "bug"),
                    "project_name": issue.get("project_name", ""),
                    "error_summary": issue.get("error_summary", ""),
                    "problem_details": issue.get("problem_details", ""),
                },
            }
        ]
    )

    return {"status": "ok", "id": issue_id}


def query_issue_memory(issue: dict, top_k: int = 3):
    index = get_pinecone_index()
    if index is None:
        return []

    text = "\n".join(
        [
            f"Issue type: {issue.get('issue_type', '')}",
            f"Project: {issue.get('project_name', '')}",
            f"Summary: {issue.get('error_summary', '')}",
            f"Details: {issue.get('problem_details', '')}",
            f"Snippet: {issue.get('code_snippet', '')}",
        ]
    ).strip()

    vector = generate_embedding(text)
    if not vector:
        return []

    response = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
    )

    matches = []
    for match in response.get("matches", []):
        metadata = match.get("metadata", {})
        matches.append(
            {
                "id": match.get("id"),
                "score": match.get("score"),
                "issue_type": metadata.get("issue_type"),
                "project_name": metadata.get("project_name"),
                "error_summary": metadata.get("error_summary"),
                "problem_details": metadata.get("problem_details"),
            }
        )

    return matches
