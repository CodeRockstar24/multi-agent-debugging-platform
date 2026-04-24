"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const titles: Record<string, { eyebrow: string; title: string }> = {
  "/dashboard": {
    eyebrow: "Mission Control",
    title: "Engineering intelligence across debugging, review, and recovery"
  },
  "/new-issue": {
    eyebrow: "Issue Intake",
    title: "Autonomous multi-agent debugging platform"
  },
  "/agent-workflow": {
    eyebrow: "Workflow View",
    title: "Trace how each specialist agent reasoned and handed off"
  },
  "/patch-review": {
    eyebrow: "Patch Intelligence",
    title: "Review generated fixes before you trust them"
  },
  "/knowledge-memory": {
    eyebrow: "Knowledge Layer",
    title: "Semantic memory and issue retrieval across past runs"
  }
};

export default function Topbar() {
  const pathname = usePathname();
  const content = titles[pathname] ?? titles["/new-issue"];

  return (
    <header className="topbar">
      <div>
        <p className="small-label">{content.eyebrow}</p>
        <h2>{content.title}</h2>
      </div>
      <div className="topbar-actions">
        <Link href="/new-issue" className="ghost-button">
          New Run
        </Link>
        <Link href="/dashboard" className="primary-button topbar-button">
          Open Dashboard
        </Link>
      </div>
    </header>
  );
}
