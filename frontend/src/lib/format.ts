export function truncate(text: string | null, maxLength: number): string {
  if (!text) return "";
  const cleaned = text.replace(/\s+/g, " ").trim(); 
  if (cleaned.length <= maxLength) return cleaned;
  return cleaned.slice(0, maxLength).trimEnd() + "…";
}

export function formatEventDate(isoString: string): string {
  return new Date(isoString).toLocaleString("en-CA", {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}