import Link from "next/link";

import { fetchStory, type Story } from "@/lib/api";

type StoryDetailProps = {
  params: Promise<{
    storyId: string;
  }>;
};

export default async function StoryDetailPage({ params }: StoryDetailProps) {
  const { storyId } = await params;

  let story: Story | null = null;
  let loadError: string | null = null;
  try {
    const data = await fetchStory(storyId);
    story = data.story;
  } catch (error) {
    loadError = error instanceof Error ? error.message : "加载失败";
  }

  return (
    <main className="container">
      <Link href="/" className="back-link">
        ← 返回故事列表
      </Link>

      {story ? (
        <section className="detail-grid">
          <article className="detail-main">
            <h1 className="detail-title">{story.title}</h1>
            <p className="detail-summary">{story.summary}</p>

            <div className="meta">
              <span className="metric">订阅 {story.subscriber_count}</span>
              <span className="metric">讨论 {story.discussion_count}</span>
              <span className="metric">存疑 {story.doubt_count}</span>
              <span className="metric">阅读 {story.view_count}</span>
              <span className="metric">参与角色 {story.participant_role_count}</span>
            </div>
          </article>

          <aside className="detail-side">
            <h2 className="side-title">你能在这里看到什么</h2>
            <ul className="side-list">
              <li className="side-item">这个故事最核心的一句话梗概</li>
              <li className="side-item">不同角色的解读与讨论</li>
              <li className="side-item">当前热度与关注趋势</li>
              <li className="side-item">你也可以收藏并持续追踪</li>
            </ul>
          </aside>
        </section>
      ) : (
        <article className="notice" style={{ marginTop: "16px" }}>
          内容暂时不可用：{loadError ?? "未知错误"}。
        </article>
      )}
    </main>
  );
}

