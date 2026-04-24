def run_planner_agent(issue: dict) -> dict:
    issue_type = issue.get("issue_type", "bug")
    project_name = issue.get("project_name", "unknown project")
    error_summary = issue.get("error_summary", "unknown issue")

    plans_by_type = {
        "bug": {
            "plan": [
                "Inspect the failing code path",
                "Identify the incorrect logic or edge case",
                "Hand off findings to patch generation"
            ],
            "handoff": "analysis_to_patch"
        },
        "code_review": {
            "plan": [
                "Inspect maintainability and readability issues",
                "Identify risky or unclear code patterns",
                "Hand off improvement targets to patch generation"
            ],
            "handoff": "analysis_to_patch"
        },
        "test_failure": {
            "plan": [
                "Inspect failing assertion and fixture context",
                "Determine whether implementation or test is wrong",
                "Hand off validated cause to patch generation"
            ],
            "handoff": "analysis_to_patch"
        },
        "api_error": {
            "plan": [
                "Inspect route, schema, and validation flow",
                "Identify contract mismatch or runtime failure",
                "Hand off API fix strategy to patch generation"
            ],
            "handoff": "analysis_to_patch"
        },
        "ci_cd_issue": {
            "plan": [
                "Inspect pipeline stage and failure point",
                "Check dependencies, auth, and environment config",
                "Hand off remediation plan to patch generation"
            ],
            "handoff": "analysis_to_patch"
        },
        "performance_issue": {
            "plan": [
                "Inspect likely bottlenecks",
                "Check hot paths, repeated work, and I/O",
                "Hand off optimization targets to patch generation"
            ],
            "handoff": "analysis_to_patch"
        },
        "deployment_issue": {
            "plan": [
                "Inspect runtime configuration and startup behavior",
                "Check env vars, networking, and service assumptions",
                "Hand off deployment remediation steps to patch generation"
            ],
            "handoff": "analysis_to_patch"
        }
    }

    selected = plans_by_type.get(issue_type, plans_by_type["bug"])

    return {
        "agent": "Planner Agent",
        "issue_type": issue_type,
        "project_name": project_name,
        "task": "Create an investigation plan",
        "plan": selected["plan"],
        "handoff": selected["handoff"],
        "summary": f"Planner agent created a branched plan for {issue_type}: {error_summary}"
    }
