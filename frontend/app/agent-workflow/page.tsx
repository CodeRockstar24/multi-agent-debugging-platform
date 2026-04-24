"use client";

import { useEffect, useState } from "react";
import { getLatestRun, type WorkflowRun } from "../../lib/workflow-store";

export default function AgentWorkflowPage() {
  const [run, setRun] = useState<WorkflowRun | null>(null);

  useEffect(() => {
    setRun(getLatestRun());
  }, []);

  return (
    <section className="page-grid">
      <div className="content-card dark-card">
        <h1>Agent Workflow</h1>
        <p>Inspect how the latest run moved from planning to review.</p>
      </div>

      {!run ? (
        <div className="content-card dark-card">
          <p>No workflow captured yet.</p>
        </div>
      ) : (
        <div className="timeline-grid">
          <div className="timeline-card">
            <h3>Planner Agent</h3>
            <p>{run.workflow.planner.summary}</p>
          </div>
          <div className="timeline-card">
            <h3>Retrieval Agent</h3>
            <p>{run.workflow.retrieval.summary}</p>
          </div>
          <div className="timeline-card">
            <h3>Analysis Agent</h3>
            <div className="rich-text">{run.workflow.analysis.analysis}</div>
          </div>
          <div className="timeline-card">
            <h3>Patch Agent</h3>
            <pre className="code-block">{run.workflow.patch.patch_preview}</pre>
          </div>
          <div className="timeline-card">
            <h3>Review Agent</h3>
            <div className="rich-text">{run.workflow.review.final_summary}</div>
          </div>
        </div>
      )}
    </section>
  );
}
