import "server-only";

export type Article = {
  id: number;
  url: string;
  title: string;
  source: "zenn" | "qiita";
  published_at: string;
  summary: string;
  category: string;
};

export type SimilarArticle = Article & { distance: number };

export type Paginated<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, path: string) {
    super(`API ${path} returned ${status}`);
    this.status = status;
  }
}

const API_BASE_URL = process.env.API_BASE_URL ?? "http://localhost:8000";
const API_AUDIENCE = process.env.API_AUDIENCE;

const METADATA_IDENTITY_URL =
  "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity";

async function fetchIdToken(audience: string): Promise<string> {
  const res = await fetch(`${METADATA_IDENTITY_URL}?audience=${encodeURIComponent(audience)}`, {
    headers: { "Metadata-Flavor": "Google" },
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`ID トークンを取得できませんでした: ${res.status}`);
  }
  return res.text();
}

async function apiGet<T>(path: string): Promise<T> {
  const headers: Record<string, string> = {};
  if (API_AUDIENCE) {
    headers.Authorization = `Bearer ${await fetchIdToken(API_AUDIENCE)}`;
  }

  const res = await fetch(`${API_BASE_URL}${path}`, { headers, cache: "no-store" });
  if (!res.ok) {
    throw new ApiError(res.status, path);
  }
  return (await res.json()) as T;
}

export function listArticles(params: { category?: string; page?: string }) {
  const query = new URLSearchParams();
  if (params.category) query.set("category", params.category);
  if (params.page) query.set("page", params.page);
  return apiGet<Paginated<Article>>(`/api/articles/?${query}`);
}

export function getArticle(id: string) {
  return apiGet<Article>(`/api/articles/${encodeURIComponent(id)}/`);
}

export function getSimilarArticles(id: string) {
  return apiGet<SimilarArticle[]>(`/api/articles/${encodeURIComponent(id)}/similar/`);
}

export function searchArticles(q: string) {
  return apiGet<SimilarArticle[]>(`/api/articles/search/?${new URLSearchParams({ q })}`);
}
