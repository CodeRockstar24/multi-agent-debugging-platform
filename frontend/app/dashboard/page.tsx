"use client";

import { useEffect, useMemo, useState } from "react";
import { loadRuns, type WorkflowRun } from "../../lib/workflow-store";

export default function DashboardPage() {
  const [runs, setRuns] = useState<WorkflowRun[]>([]);

  useEffect(() => {
    setRuns(loadRuns());
  }, []);

  const stats = useMemo(() => {
    const avgConfidence =
      runs.length > 0
        ? runs.reduce((sum, run) => sum + (run.workflow.review.confidence ?? 0), 0) / runs.length
        : 0;

    const memoryHits = runs.reduce((sum, run) => {
      const sqlite = run.workflow.retrieval.memory_hits?.sqlite?.length ?? 0;
      const pinecone = run.workflow.retrieval.memory_hits?.pinecone?.length ?? 0;
      return sum + sqlite + pinecone;
    }, 0);

    return {
      totalRuns: runs.length,
      avgConfidence,
      memoryHits
    };
  }, [runs]);

  const latest = runs[0] ?? null;

  return (
    <section className="page-grid">
      <div className="content-card dark-card">
        <h1>Dashboard</h1>
        <p>Mission control for recent workflows, memory signals, and review quality.</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card dark-card">
          <p className="small-label">Workflow Runs</p>
          <h3>{stats.totalRuns}</h3>
        </div>
        <div className="stat-card dark-card">
          <p className="small-label">Average Confidence</p>
          <h3>{stats.totalRuns ? `${Math.round(stats.avgConfidence * 100)}%` : "--"}</h3>
        </div>
        <div className="stat-card dark-card">
          <p className="small-label">Memory Hits</p>
          <h3>{stats.memoryHits}</h3>
        </div>
      </div>

      <div className="content-card dark-card">
        <h2>Latest Run</h2>
        {!latest ? (
          <p>No runs yet. Submit an issue from New Issue.</p>
        ) : (
          <>
            <p><strong>Project:</strong> {latest.issue.project_name}</p>
            <p><strong>Issue Type:</strong> {latest.issue.issue_type}</p>
            <p><strong>Summary:</strong> {latest.issue.error_summary}</p>
            <p><strong>Risk:</strong> {latest.workflow.review.risk}</p>
          </>
        )}
      </div>
    </section>
  );
}
