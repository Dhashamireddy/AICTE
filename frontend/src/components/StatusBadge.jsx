import { CheckCircle2, AlertCircle, Loader2 } from "lucide-react";

// state: "loading" | "ok" | "error"
export default function StatusBadge({ state, message }) {
  const icons = {
    loading: <Loader2 size={16} className="spin" />,
    ok: <CheckCircle2 size={16} />,
    error: <AlertCircle size={16} />,
  };
  return (
    <span className={`badge badge-${state}`} role="status">
      {icons[state]} {message}
    </span>
  );
}
