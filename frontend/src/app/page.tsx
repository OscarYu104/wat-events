import { fetchEvents } from "@/lib/api";

export default async function Home() {
  const events = await fetchEvents();

  return (
    <main>
      <h1>UW Events</h1>
      {events.length === 0 ? (
        <p>No upcoming events.</p>
      ) : (
        <ul>
          {events.map((event) => (
            <li key={event.id}>
              <strong>{event.title}</strong>
              <br />
              {new Date(event.start_time).toLocaleString()}
              {event.location_name && ` — ${event.location_name}`}
              {event.is_free ? " — Free" : event.cost_amount ? ` — $${event.cost_amount}` : ""}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
