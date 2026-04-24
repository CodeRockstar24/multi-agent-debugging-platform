import "./globals.css";
import type { ReactNode } from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

export const metadata = {
  title: "Code Debugger AI",
  description: "Multi-agent AI assistant for software debugging and code review"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <Sidebar />
          <div className="main-shell">
            <Topbar />
            <main className="page-content">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
