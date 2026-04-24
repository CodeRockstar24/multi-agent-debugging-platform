"use client";

export type WorkflowRun = {
  issue: {
    id?: number;
    issue_type: string;
    project_name: string;
    error_summary: string;
    problem_details?: string;
    code_snippet?: string;
    status?: string;
  };
  workflow: {
    planner: { summary?: string; plan?: string[]; handoff?: string };
    retrieval: {
      summary?: string;
      retrieved_context?: string[];
      memory_hits?: {
        sqlite?: Array<{ id: number; error_summary: string; issue_type?: string }>;
        pinecone?: Array<{ id: string; error_summary: string; issue_type?: string; score?: number }>;
      };
    };
    analysis: { summary?: string; analysis?: string };
    patch: { summary?: string; patch_preview?: string; based_on?: string };
    review: {
      final_summary?: string;
      confidence?: number;
      risk?: string;
      next_actions?: string[];
      workflow_trace?: Record<string, string | undefined>;
    };
  };
  autonomy?: {
    branching_used?: string;
    analysis_attempts?: Array<{ attempt: number; status: string; summary: string }>;
    memory_enabled?: boolean;
    fallbacks_enabled?: boolean;
  };
  createdAt?: string;
};

const STORAGE_KEY = "code-debugger-runs";
const MAX_RUNS = 12;

export function loadRuns(): WorkflowRun[] {
  if (typeof window === "undefined") return [];

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as WorkflowRun[]) : [];
  } catch {
    return [];
  }
}

export function saveRun(run: WorkflowRun) {
  if (typeof window === "undefined") return;

  const existing = loadRuns();
  const next = [{ ...run, createdAt: new Date().toISOString() }, ...existing].slice(0, MAX_RUNS);
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
}

export function getLatestRun(): WorkflowRun | null {
  const runs = loadRuns();
  return runs.length > 0 ? runs[0] : null;
}
