from pydantic import BaseModel


class IssueCreate(BaseModel):
    issue_type: str = "bug"
    project_name: str
    error_summary: str
    problem_details: str | None = None
    code_snippet: str | None = None


class IssueResponse(BaseModel):
    id: int
    issue_type: str
    project_name: str
    error_summary: str
    problem_details: str | None = None
    code_snippet: str | None = None
    status: str
