"use client";

import { useEffect, useState } from "react";
import { getLatestRun, type WorkflowRun } from "../../lib/workflow-store";

export default function PatchReviewPage() {
  const [run, setRun] = useState<WorkflowRun | null>(null);

  useEffect(() => {
    setRun(getLatestRun());
  }, []);

  return (
    <section className="page-grid">
      <div className="content-card dark-card">
        <h1>Patch Review</h1>
        <p>Review the latest generated patch and validation guidance.</p>
      </div>

      {!run ? (
        <div className="content-card dark-card">
          <p>No patch generated yet.</p>
        </div>
      ) : (
        <>
          <div className="review-grid">
            <div className="stat-card dark-card">
              <p className="small-label">Confidence</p>
              <h3>{Math.round((run.workflow.review.confidence ?? 0) * 100)}%</h3>
            </div>
            <div className="stat-card dark-card">
              <p className="small-label">Risk</p>
              <h3>{run.workflow.review.risk}</h3>
            </div>
            <div className="stat-card dark-card">
              <p className="small-label">Issue Type</p>
              <h3>{run.issue.issue_type}</h3>
            </div>
          </div>

          <div className="content-card dark-card">
            <h2>Patch Preview</h2>
            <pre className="code-block">{run.workflow.patch.patch_preview ?? "No patch preview."}</pre>
          </div>

          <div className="content-card dark-card">
            <h2>Validation Steps</h2>
            {run.workflow.review.next_actions && (
              <ul className="clean-list">
                {run.workflow.review.next_actions.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            )}
          </div>
        </>
      )}
    </section>
  );
}
