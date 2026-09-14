const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Event {
  id: string;
  title: string;
  description: string | null;
  start_time: string;
  end_time: string | null;
  location_name: string | null;
  is_online: boolean;
  categories: string[];
  is_free: boolean;
  cost_amount: string | null;
}

export async function fetchEvents(): Promise<Event[]> {
  const res = await fetch(`${API_BASE_URL}/events`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to fetch events: ${res.status}`);
  return res.json();
}
