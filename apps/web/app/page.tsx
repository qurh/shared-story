import Link from "next/link";

import { fetchStories, searchStories, type SortMode, type Story } from "@/lib/api";

type HomeProps = {
  searchParams?: Promise<{
    q?: string;
    sort?: string;
  }>;
};

const sortOptions: Array<{ value: SortMode; label: string }> = [
  { value: "composite", label: "为你推荐" },
  { value: "subscribers", label: "最多人关注" },
  { value: "latest_active", label: "最近有新讨论" }
];

function parseSortMode(raw?: string): SortMode {
  if (raw === "subscribers" || raw === "latest_active") {
    return raw;
  }
  return "composite";
}

function buildSortHref(targetSort: SortMode, q: string): string {
  const params = new URLSearchParams();
  params.set("sort", targetSort);
  if (q) {
    params.set("q", q);
  }
  return `/?${params.toString()}`;
}

export default async function Home({ searchParams }: HomeProps) {
  const resolvedSearchParams = (await searchParams) ?? {};
  const q = resolvedSearchParams.q?.trim() ?? "";
  const sort = parseSortMode(resolvedSearchParams.sort);

  let stories: Story[] = [];
  let loadError: string | null = null;
  try {
    const listData = q ? await searchStories(q) : await fetchStories(sort);
    stories = listData.stories;
  } catch (error) {
    loadError = error instanceof Error ? error.message : "加载失败";
  }

  return (
    <main className="container">
      <section className="hero">
        <div className="hero-inner">
          <div className="brand-row">
            <span className="brand-mark">shared-story</span>
            <span className="status-chip">持续更新中</span>
          </div>
          <h1 className="brand">先看故事，再看不同理解</h1>
          <p className="lead">
            先选故事，再看不同角色的解读与讨论。
          </p>

          <div className="toolbar">
            <form className="search-wrap" action="/" method="get">
              <input
                className="search-input"
                name="q"
                placeholder="搜索故事，例如：庄周梦蝶、塞翁失马、井底之蛙..."
                defaultValue={q}
                aria-label="搜索故事"
              />
              <input type="hidden" name="sort" value={sort} />
              <button className="search-btn" type="submit">
                搜索
              </button>
            </form>

            <div className="sort-row" aria-label="排序方式">
              {sortOptions.map((option) => (
                <Link
                  href={buildSortHref(option.value, q)}
                  key={option.value}
                  className={`sort-chip ${sort === option.value ? "active" : ""}`}
                >
                  {option.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="section-head">
        <p className="section-label">{q ? `搜索 “${q}” 的结果` : "精选故事"} · 共 {stories.length} 条</p>
      </section>

      {loadError ? (
        <div className="notice">内容暂时不可用：{loadError}。请确认后端服务已启动。</div>
      ) : (
        <section className="story-list">
          {stories.map((story) => (
            <Link href={`/stories/${story.id}`} key={story.id} className="story-card">
              <h2 className="story-title">{story.title}</h2>
              <p className="story-summary">{story.summary}</p>
              <div className="story-meta">
                <div className="meta meta-primary">
                  <span className="metric metric-strong">订阅 {story.subscriber_count}</span>
                  <span className="metric metric-strong">讨论 {story.discussion_count}</span>
                </div>
                <div className="meta meta-secondary">
                  <span className="metric metric-subtle">存疑 {story.doubt_count}</span>
                  <span className="metric metric-subtle">阅读 {story.view_count}</span>
                </div>
              </div>
              <div className="cta">继续看这个故事</div>
            </Link>
          ))}
        </section>
      )}
    </main>
  );
}
