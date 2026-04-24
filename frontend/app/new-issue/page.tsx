"use client";

import { useState } from "react";
import { saveRun, type WorkflowRun } from "../../lib/workflow-store";

const issueTypes = [
  "bug",
  "code_review",
  "test_failure",
  "api_error",
  "ci_cd_issue",
  "performance_issue",
  "deployment_issue"
];

export default function NewIssuePage() {
  const [issueType, setIssueType] = useState("bug");
  const [projectName, setProjectName] = useState("");
  const [errorSummary, setErrorSummary] = useState("");
  const [problemDetails, setProblemDetails] = useState("");
  const [codeSnippet, setCodeSnippet] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<WorkflowRun | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setResult(null);
    setErrorMessage("");

    try {
      const response = await fetch("/api/agent-workflow", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          issue_type: issueType,
          project_name: projectName,
          error_summary: errorSummary,
          problem_details: problemDetails,
          code_snippet: codeSnippet
        })
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Backend error: ${response.status} ${text}`);
      }

      const data = (await response.json()) as WorkflowRun;
      setResult(data);
      saveRun(data);
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Something went wrong while submitting the issue."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page-grid">
      <div className="content-card dark-card">
        <h1>New Issue</h1>
        <p>Submit a difficult software engineering problem and inspect the full multi-agent workflow.</p>

        <form className="issue-form" onSubmit={handleSubmit}>
          <div className="content-grid-2">
            <label>
              Issue Type
              <select value={issueType} onChange={(e) => setIssueType(e.target.value)}>
                {issueTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Project Name
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="finops-observability-platform"
              />
            </label>
          </div>

          <label>
            Error Summary
            <input
              type="text"
              value={errorSummary}
              onChange={(e) => setErrorSummary(e.target.value)}
              placeholder="Production service is failing health checks after deploy"
            />
          </label>

          <label>
            Problem Details
            <textarea
              rows={7}
              value={problemDetails}
              onChange={(e) => setProblemDetails(e.target.value)}
              placeholder="Paste incident details, logs, stack trace, rollout context, or failure description"
            />
          </label>

          <label>
            Code Snippet / Command / Config
            <textarea
              rows={10}
              value={codeSnippet}
              onChange={(e) => setCodeSnippet(e.target.value)}
              placeholder="Paste code, workflow YAML, deployment config, API request, or suspicious command"
            />
          </label>

          <button type="submit" className="primary-button" disabled={loading}>
            {loading ? "Running agents..." : "Run Agent Workflow"}
          </button>
        </form>

        {errorMessage && (
          <div className="workflow-card error-card">
            <h3>Request Error</h3>
            <p>{errorMessage}</p>
          </div>
        )}
      </div>

      {result && (
        <>
          <div className="content-card dark-card">
            <h2>Workflow Result</h2>
            <div className="meta-row">
              <span className="pill">{result.issue.issue_type}</span>
              <span className="pill">{result.issue.project_name}</span>
              <span className="pill success-pill">
                {Math.round((result.workflow.review.confidence ?? 0) * 100)}% confidence
              </span>
            </div>

            <div className="workflow-list">
              <div className="workflow-card dark-subcard">
                <h3>Planner Agent</h3>
                <p>{result.workflow.planner.summary}</p>
                {result.workflow.planner.plan && (
                  <ul className="clean-list">
                    {result.workflow.planner.plan.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                )}
              </div>

              <div className="workflow-card dark-subcard">
                <h3>Retrieval Agent</h3>
                <p>{result.workflow.retrieval.summary}</p>
                <ul className="clean-list">
                  {result.workflow.retrieval.retrieved_context?.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="workflow-card dark-subcard">
                <h3>Analysis Agent</h3>
                <div className="rich-text">{result.workflow.analysis.analysis}</div>
              </div>

              <div className="workflow-card dark-subcard">
                <h3>Patch Agent</h3>
                <p>{result.workflow.patch.summary}</p>
                <pre className="code-block">{result.workflow.patch.patch_preview}</pre>
              </div>

              <div className="workflow-card dark-subcard">
                <h3>Review Agent</h3>
                <div className="rich-text">{result.workflow.review.final_summary}</div>
                <div className="meta-row">
                  <span className="pill success-pill">
                    Confidence {Math.round((result.workflow.review.confidence ?? 0) * 100)}%
                  </span>
                  <span className="pill warning-pill">
                    Risk {result.workflow.review.risk}
                  </span>
                </div>
                {result.workflow.review.next_actions && (
                  <ul className="clean-list">
                    {result.workflow.review.next_actions.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </div>

          <div className="content-card dark-card">
            <h2>Autonomy Signals</h2>
            <p><strong>Branching Used:</strong> {result.autonomy?.branching_used}</p>
            <p><strong>Memory Enabled:</strong> {String(result.autonomy?.memory_enabled)}</p>
            <p><strong>Fallbacks Enabled:</strong> {String(result.autonomy?.fallbacks_enabled)}</p>
          </div>
        </>
      )}
    </section>
  );
}
