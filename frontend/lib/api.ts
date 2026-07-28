export type BackendPingResponse = {
  message: string;
  backend: string;
};

export type Document = {
  id: string;
  user_id: string;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
};

const apiBasePath = "/api/backend/api";

export class ApiError extends Error {
  constructor(message: string, public readonly status: number) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${apiBasePath}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new ApiError(payload?.detail ?? "The request could not be completed.", response.status);
  }

  return (await response.json()) as T;
}

export function listDocuments(token: string): Promise<Document[]> {
  return request<Document[]>("/documents", { headers: { Authorization: `Bearer ${token}` } });
}

export function createDocument(token: string, title: string, content: string): Promise<Document> {
  return request<Document>("/documents", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ title, content }),
  });
}

export async function fetchBackendPing(baseUrl: string): Promise<BackendPingResponse | null> {
  try {
    const response = await fetch(`${baseUrl}/api/ping`, { cache: "no-store" });

    if (!response.ok) {
      return null;
    }

    return (await response.json()) as BackendPingResponse;
  } catch {
    return null;
  }
}
