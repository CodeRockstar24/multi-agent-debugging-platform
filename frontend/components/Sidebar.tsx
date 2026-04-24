"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/new-issue", label: "New Issue" },
  { href: "/agent-workflow", label: "Agent Workflow" },
  { href: "/patch-review", label: "Patch Review" },
  { href: "/knowledge-memory", label: "Knowledge Memory" }
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <div className="brand">
        <p className="brand-tag">AI Software Engineer</p>
        <h1>Code Debugger</h1>
        <p className="brand-copy">
          Multi-agent software debugging, patch generation, review, and memory retrieval.
        </p>
      </div>

      <nav className="nav-links">
        {links.map((link) => {
          const isActive = pathname === link.href;
          return (
            <Link key={link.href} href={link.href} className={`nav-link${isActive ? " active" : ""}`}>
              <span className="nav-link-title">{link.label}</span>
              <span className="nav-link-meta">Open</span>
            </Link>
          );
        })}
      </nav>

      <div className="sidebar-card">
        <p className="small-label">Current Focus</p>
        <h3>Autonomous Engineering Assist</h3>
        <p>Branching workflows, semantic memory, dynamic patching, and LLM-backed review.</p>
      </div>
    </aside>
  );
}
