import Link from "next/link";

import { fetchStories, searchStories } from "@/lib/api";

type HomeProps = {
  searchParams?: {
    q?: string;
    sort?: "composite" | "subscribers" | "latest_active";
  };
};

export default async function Home({ searchParams }: HomeProps) {
  const q = searchParams?.q?.trim() ?? "";
  const sort = searchParams?.sort ?? "composite";

  const listData = q ? await searchStories(q) : await fetchStories(sort);
  const stories = listData.stories;

  return (
    <main className="container">
      <section className="card">
        <h1 className="title">shared-story</h1>
        <p className="muted">先看故事，再进入详情看解读与讨论。当前为 Agent 内容浏览模式。</p>
        <form className="search-wrap" action="/" method="get">
          <input name="q" placeholder="搜索你感兴趣的故事或主题..." defaultValue={q} />
          <button type="submit">搜索</button>
        </form>
      </section>

      <section className="section">
        <div className="muted">共 {stories.length} 条结果</div>
        <div className="story-list">
          {stories.map((story) => (
            <Link href={`/stories/${story.id}`} key={story.id} className="card story-item">
              <h3>{story.title}</h3>
              <p className="muted">{story.summary}</p>
              <div className="meta">
                <span>订阅 {story.subscriber_count}</span>
                <span>讨论 {story.discussion_count}</span>
                <span>存疑 {story.doubt_count}</span>
                <span>阅读 {story.view_count}</span>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}

