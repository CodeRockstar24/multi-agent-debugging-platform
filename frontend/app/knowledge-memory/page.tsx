"use client";

import { useEffect, useState } from "react";
import { getLatestRun, loadRuns, type WorkflowRun } from "../../lib/workflow-store";

export default function KnowledgeMemoryPage() {
  const [latest, setLatest] = useState<WorkflowRun | null>(null);
  const [runs, setRuns] = useState<WorkflowRun[]>([]);

  useEffect(() => {
    setLatest(getLatestRun());
    setRuns(loadRuns());
  }, []);

  const sqliteHits = latest?.workflow.retrieval.memory_hits?.sqlite ?? [];
  const pineconeHits = latest?.workflow.retrieval.memory_hits?.pinecone ?? [];

  return (
    <section className="page-grid">
      <div className="content-card dark-card">
        <h1>Knowledge Memory</h1>
        <p>Inspect structured and semantic memory from recent issue runs.</p>
      </div>

      <div className="content-grid-2">
        <div className="content-card dark-card">
          <h2>SQLite Memory Hits</h2>
          {sqliteHits.length > 0 ? (
            <ul className="clean-list">
              {sqliteHits.map((item) => (
                <li key={item.id}>#{item.id} - {item.error_summary}</li>
              ))}
            </ul>
          ) : (
            <p>No SQLite memory hits yet.</p>
          )}
        </div>

        <div className="content-card dark-card">
          <h2>Pinecone Semantic Matches</h2>
          {pineconeHits.length > 0 ? (
            <ul className="clean-list">
              {pineconeHits.map((item) => (
                <li key={item.id}>
                  {item.error_summary} ({item.issue_type}) score: {item.score?.toFixed?.(3) ?? item.score}
                </li>
              ))}
            </ul>
          ) : (
            <p>No Pinecone matches yet.</p>
          )}
        </div>
      </div>

      <div className="content-card dark-card">
        <h2>Recent Stored Runs</h2>
        {runs.length > 0 ? (
          <div className="table-like">
            {runs.map((run, index) => (
              <article className="table-row" key={`${run.issue.error_summary}-${index}`}>
                <div>
                  <p className="small-label">{run.issue.issue_type}</p>
                  <h3>{run.issue.error_summary}</h3>
                  <p>{run.issue.project_name}</p>
                </div>
                <div>
                  <p className="small-label">SQLite Hits</p>
                  <h3>{run.workflow.retrieval.memory_hits?.sqlite?.length ?? 0}</h3>
                </div>
                <div>
                  <p className="small-label">Pinecone Hits</p>
                  <h3>{run.workflow.retrieval.memory_hits?.pinecone?.length ?? 0}</h3>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <p>No stored runs yet.</p>
        )}
      </div>
    </section>
  );
}
