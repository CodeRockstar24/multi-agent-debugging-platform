from app.db.database import get_connection
from app.models.issue import IssueCreate
from app.services.pinecone_service import upsert_issue_memory


def create_issue(issue: IssueCreate):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO issues (issue_type, project_name, error_summary, problem_details, code_snippet)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            issue.issue_type,
            issue.project_name,
            issue.error_summary,
            issue.problem_details,
            issue.code_snippet,
        ),
    )

    issue_id = cursor.lastrowid
    connection.commit()

    cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,))
    saved_issue = cursor.fetchone()
    connection.close()

    saved_issue_dict = dict(saved_issue)
    upsert_issue_memory(saved_issue_dict)

    return saved_issue_dict


def get_similar_issues(issue_type: str, project_name: str, limit: int = 3):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, issue_type, project_name, error_summary, problem_details, status
        FROM issues
        WHERE issue_type = ? OR project_name = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (issue_type, project_name, limit),
    )

    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]
