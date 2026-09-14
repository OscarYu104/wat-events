import { fetchEvents } from "@/lib/api";

interface HomeProps {
  searchParams: { category?: string; is_free?: string; search?: string };
}

export default async function Home({ searchParams }: HomeProps) {
  const events = await fetchEvents({
    category: searchParams.category,
    isFree: searchParams.is_free === "true" ? true : undefined,
    search: searchParams.search,
  });

  return (
    <main>
      <h1>UW Events</h1>

      <form method="GET">
        <input type="text" name="search" placeholder="Search events..." defaultValue={searchParams.search} />
        <select name="category" defaultValue={searchParams.category ?? ""}>
          <option value="">All categories</option>
          <option value="academic">Academic</option>
          <option value="career">Career</option>
          <option value="social">Social</option>
          <option value="sports">Sports</option>
          <option value="arts_culture">Arts & Culture</option>
          <option value="volunteering">Volunteering</option>
          <option value="workshop">Workshop</option>
          <option value="food">Food</option>
        </select>
        <label>
          <input type="checkbox" name="is_free" value="true" defaultChecked={searchParams.is_free === "true"} />
          Free only
        </label>
        <button type="submit">Filter</button>
      </form>
      
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
