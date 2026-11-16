import { useEffect, useState } from "react";
import { Landmark } from "lucide-react";
import StatusBadge from "../components/StatusBadge.jsx";
import { getHealth } from "../services/api.js";

export default function Home() {
  const [status, setStatus] = useState({ state: "loading", message: "Checking backend..." });

  useEffect(() => {
    getHealth()
      .then((data) => setStatus({ state: "ok", message: `Backend ${data.status}, database ${data.database}` }))
      .catch(() => setStatus({ state: "error", message: "Backend not reachable. Is it running on port 8000?" }));
  }, []);

  return (
    <main className="container">
      <header className="hero">
        <Landmark size={40} />
        <h1>AICTE Assistive Portal</h1>
        <p>An AI-based system for simplifying the approval process for technical institutions.</p>
        <StatusBadge state={status.state} message={status.message} />
      </header>
      <footer className="disclaimer">
        Academic assistance prototype. This is not an official AICTE approval system.
      </footer>
    </main>
  );
}
