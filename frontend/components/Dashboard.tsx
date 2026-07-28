"use client";

import { FormEvent, useEffect, useState } from "react";
import { useAuth, useUser, UserButton } from "@clerk/nextjs";

import { ApiError, createDocument, Document, listDocuments } from "../lib/api";

export default function Dashboard() {
  const { isLoaded: isUserLoaded, user } = useUser();
  const { getToken } = useAuth();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    if (!isUserLoaded) return;

    getToken()
      .then((token) => {
        if (!token) throw new ApiError("Your session has expired. Please log in again.", 401);
        return listDocuments(token);
      })
      .then(setDocuments)
      .catch((caughtError: unknown) => {
        setError(caughtError instanceof ApiError ? caughtError.message : "Unable to load your dashboard. Please try again.");
      })
      .finally(() => setIsLoading(false));
  }, [isUserLoaded, getToken]);

  async function handleCreate(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    const token = await getToken();
    if (!token) return;
    const form = event.currentTarget;
    const values = new FormData(form);
    setError(null);
    setIsCreating(true);

    try {
      const document = await createDocument(token, String(values.get("title")), String(values.get("content")));
      setDocuments((current) => [document, ...current]);
      form.reset();
    } catch (caughtError) {
      setError(caughtError instanceof ApiError ? caughtError.message : "Unable to save the document.");
    } finally {
      setIsCreating(false);
    }
  }

  if (!isUserLoaded || isLoading) return <p className="lede">Loading your dashboard…</p>;

  return (
    <>
      <section className="card">
        <p className="eyebrow">Your dashboard</p>
        <h1>Welcome{user?.firstName ? `, ${user.firstName}` : ""}</h1>
        <p className="lede">
          Your documents are private to {user?.primaryEmailAddress?.emailAddress}. Add pasted notes now; uploads and
          study generation arrive in Stage 2.
        </p>
        <UserButton afterSignOutUrl="/" />
      </section>
      <section className="card">
        <h2>Add study notes</h2>
        <form className="status-grid" onSubmit={handleCreate}>
          <label><span>Title</span><input name="title" maxLength={255} required /></label>
          <label><span>Notes</span><textarea name="content" rows={6} required /></label>
          <button type="submit" disabled={isCreating}>{isCreating ? "Saving…" : "Save document"}</button>
        </form>
      </section>
      <section className="card">
        <h2>Your documents</h2>
        {error ? <p className="error" role="alert">{error}</p> : null}
        {documents.length === 0 ? <p className="lede">No documents yet. Save a set of notes to begin.</p> : (
          <ul className="document-list">
            {documents.map((document) => <li key={document.id}><strong>{document.title}</strong><span>Saved {new Date(document.created_at).toLocaleDateString()}</span></li>)}
          </ul>
        )}
      </section>
    </>
  );
}
