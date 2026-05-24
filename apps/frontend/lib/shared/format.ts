export function money(value: unknown, currency = "USD") {
  const numeric = Number(value ?? 0);
  if (!Number.isFinite(numeric)) return `- ${currency}`;
  return `${numeric.toFixed(2)} ${currency}`;
}

export function percent(value: unknown) {
  const numeric = Number(value ?? 0);
  if (!Number.isFinite(numeric)) return "-";
  return `${numeric.toFixed(1)}%`;
}

export function dateTime(value: unknown) {
  if (!value) return "-";
  const date = new Date(String(value));
  if (Number.isNaN(date.getTime())) return "-";
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
}

export function countdown(expiresAt: unknown) {
  if (!expiresAt) return "-";
  const ms = new Date(String(expiresAt)).getTime() - Date.now();
  if (!Number.isFinite(ms) || ms <= 0) return "expired";
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  return minutes > 0 ? `${minutes}m ${seconds % 60}s` : `${seconds}s`;
}

export function truncate(value: unknown, length = 10) {
  const text = String(value ?? "");
  if (text.length <= length) return text || "-";
  return `${text.slice(0, length)}...`;
}

