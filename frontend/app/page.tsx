import { fetchBackendPing } from "../lib/api";
import Link from "next/link";

type ProcessLike = {
  env?: Record<string, string | undefined>;
};

declare global {
  namespace JSX {
    interface IntrinsicElements {
      [elementName: string]: unknown;
    }
  }
}

function getBackendBaseUrl(): string {
  const runtime = globalThis as typeof globalThis & { process?: ProcessLike };

  return runtime.process?.env?.BACKEND_BASE_URL ?? "http://backend:8000";
}

export default async function HomePage() {
  const backendBaseUrl = getBackendBaseUrl();
  const ping = await fetchBackendPing(backendBaseUrl);

  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">Stage 0 scaffold</p>
        <h1>Learning Assistant</h1>
        <p className="lede">
          A retrieval-grounded study tool scaffold with a live backend ping path.
        </p>
      </section>

      <section className="card">
        <h2>Backend status</h2>
        {ping ? (
          <dl className="status-grid" role="status">
            <div>
              <dt>Message</dt>
              <dd>{ping.message}</dd>
            </div>
            <div>
              <dt>Service</dt>
              <dd>{ping.backend}</dd>
            </div>
          </dl>
        ) : (
          <p className="error" role="alert">
            Unable to reach the backend ping endpoint.
          </p>
        )}
      </section>

      <section className="card">
        <h2>Stage 1 entry points</h2>
        <p className="lede">Start with auth, then move into the user dashboard and document management flow.</p>
        <div className="status-grid">
          <Link href="/login">Login</Link>
          <Link href="/signup">Sign up</Link>
          <Link href="/dashboard">Dashboard</Link>
        </div>
      </section>
    </main>
  );
}
