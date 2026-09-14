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

export interface EventFilters {
  category?: string;
  isFree?: boolean;
  search?: string;
}

export async function fetchEvents(filters: EventFilters = {}): Promise<Event[]> {
  const params = new URLSearchParams();
  if (filters.category) params.set("category", filters.category);
  if (filters.isFree !== undefined) params.set("is_free", String(filters.isFree));
  if (filters.search) params.set("search", filters.search);

  const res = await fetch(`${API_BASE_URL}/events?${params.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to fetch events: ${res.status}`);
  return res.json();
}
