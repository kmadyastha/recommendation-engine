"use client";

import { useEffect, useState } from "react";
import { getHealth } from "@/lib/api";
import type { HealthResponse } from "@/lib/types";

interface StatusModalProps {
  open: boolean;
  onClose: () => void;
}

export function StatusModal({ open, onClose }: StatusModalProps) {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!open) return;

    setLoading(true);
    setError(null);
    getHealth()
      .then(setHealth)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [open]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
      onClick={onClose}
      role="presentation"
    >
      <div
        className="glass-panel w-full max-w-md rounded-xl p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-labelledby="status-title"
      >
        <div className="mb-4 flex items-center justify-between">
          <h2 id="status-title" className="text-title-md font-semibold text-on-surface">
            API Status
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="text-on-surface-variant transition-colors hover:text-primary"
            aria-label="Close"
          >
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        {loading && (
          <p className="text-body-sm text-on-surface-variant">Checking backend…</p>
        )}

        {error && (
          <p className="text-body-sm text-error">Unable to reach API: {error}</p>
        )}

        {health && (
          <dl className="space-y-3 text-body-sm">
            <StatusRow label="Status" value={health.status} ok={health.ready} />
            <StatusRow
              label="Restaurants loaded"
              value={health.restaurant_count.toLocaleString()}
              ok={health.data_loaded}
            />
            <StatusRow
              label="Cities"
              value={health.city_count.toLocaleString()}
              ok={health.city_count > 0}
            />
            <StatusRow
              label="LLM configured"
              value={health.llm_configured ? "Yes" : "No"}
              ok={health.llm_configured}
            />
            <StatusRow label="Data path" value={health.data_path} />
            {health.data_error && (
              <StatusRow label="Data error" value={health.data_error} ok={false} />
            )}
          </dl>
        )}
      </div>
    </div>
  );
}

function StatusRow({
  label,
  value,
  ok,
}: {
  label: string;
  value: string;
  ok?: boolean;
}) {
  return (
    <div className="flex items-start justify-between gap-4 border-b border-outline-variant/20 pb-2">
      <dt className="text-on-surface-variant">{label}</dt>
      <dd
        className={`text-right font-medium ${
          ok === undefined ? "text-on-surface" : ok ? "text-secondary" : "text-error"
        }`}
      >
        {value}
      </dd>
    </div>
  );
}
