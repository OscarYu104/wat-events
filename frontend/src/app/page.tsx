import { fetchEvents } from "@/lib/api";
import { truncate, formatEventDate } from "@/lib/format";

interface HomeProps {
  searchParams: { category?: string; is_free?: string; search?: string };
}

const CATEGORIES = [
  "academic", "career", "social", "sports", "arts_culture",
  "volunteering", "workshop", "food", "other",
];

export default async function Home({ searchParams }: HomeProps) {
  const events = await fetchEvents({
    category: searchParams.category,
    isFree: searchParams.is_free === "true" ? true : undefined,
    search: searchParams.search,
  });

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: "2rem 1rem" }}>
      <h1>UW Events</h1>

      <form method="GET" style={{ display: "flex", gap: "0.5rem", marginBottom: "1.5rem", flexWrap: "wrap" }}>
        <input type="text" name="search" placeholder="Search events..." defaultValue={searchParams.search} />
        <select name="category" defaultValue={searchParams.category ?? ""}>
          <option value="">All categories</option>
          {CATEGORIES.map((cat) => (
            <option key={cat} value={cat}>{cat.replace("_", " ")}</option>))}
        </select>
        <label>
          <input type="checkbox" name="is_free" value="true" defaultChecked={searchParams.is_free === "true"} />
          {" "}Free only
        </label>
        <button type="submit">Filter</button>
      </form>
      
      {events.length === 0 ? (
        <p>No upcoming events match your filters.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0, display: "flex", flexDirection: "column", gap: "1rem" }}>
          {events.map((event) => (
            <li key={event.id} style={{ border: "1px solid #ddd", borderRadius: 8, padding: "1rem" }}>
              <h3 style={{ margin: "0 0 0.25rem" }}>
                {event.external_url ? (
                  <a href={event.external_url} target="_blank" rel="noopener noreferrer">{event.title}</a>
                ) : (
                  event.title
                )}
              </h3>
              <div style={{ fontSize: "0.9rem", color: "#555" }}>
                {formatEventDate(event.start_time)}
                {event.location_name && ` · ${event.location_name}`}
                {" · "}{event.is_free ? "Free" : event.cost_amount ? `$${event.cost_amount}` : "Cost varies"}
              </div>
              <div style={{ margin: "0.5rem 0" }}>
                {event.categories.map((cat) => (
                  <span
                    key={cat}
                    style={{
                      display: "inline-block", fontSize: "0.75rem", background: "#eee",
                      borderRadius: 4, padding: "0.15rem 0.5rem", marginRight: "0.25rem",
                    }}
                  >
                    {cat.replace("_", " ")}
                  </span>
                ))}
              </div>
              <p style={{ margin: 0, fontSize: "0.9rem" }}>{truncate(event.description, 200)}</p>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
