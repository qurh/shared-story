type ApiEnvelope<T> = {
  success: boolean;
  data: T | null;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown> | null;
  } | null;
};

export type SortMode = "composite" | "subscribers" | "latest_active";

export type Story = {
  id: string;
  title: string;
  summary: string;
  status: string;
  view_count: number;
  discussion_count: number;
  participant_role_count: number;
  subscriber_count: number;
  doubt_count: number;
  age_hours: number;
};

type StoryListData = {
  stories: Story[];
  sort: SortMode;
};

type StoryDetailData = {
  story: Story;
};

type SearchData = {
  stories: Story[];
  fallback: {
    insights: Array<{ id: string; title: string; summary: string }>;
    discussions: Array<{ id: string; content: string }>;
  };
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

async function getJson<T>(path: string): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  } catch {
    throw new Error(`Cannot connect backend service: ${API_BASE}`);
  }

  let payload: ApiEnvelope<T>;
  try {
    payload = (await response.json()) as ApiEnvelope<T>;
  } catch {
    throw new Error(`Backend returned non-JSON response (HTTP ${response.status})`);
  }

  if (!response.ok || !payload.success || payload.data == null) {
    throw new Error(payload.error?.message ?? `Request failed (HTTP ${response.status})`);
  }
  return payload.data;
}

export async function fetchStories(sort: SortMode = "composite"): Promise<StoryListData> {
  return getJson<StoryListData>(`/stories?sort=${sort}`);
}

export async function fetchStory(storyId: string): Promise<StoryDetailData> {
  return getJson<StoryDetailData>(`/stories/${storyId}`);
}

export async function searchStories(query: string): Promise<SearchData> {
  return getJson<SearchData>(`/search?q=${encodeURIComponent(query)}`);
}

