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

  const preview = story?.activity_preview ?? { insights: [], discussions: [] };

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

            <div className="detail-preview-grid">
              <section className="detail-panel">
                <div className="detail-panel-head">
                  <h2 className="detail-panel-title">最新解读</h2>
                  <span className="detail-panel-note">按最近更新展示</span>
                </div>

                {preview.insights.length > 0 ? (
                  <div className="detail-panel-list">
                    {preview.insights.map((insight) => (
                      <article className="detail-preview-card" key={insight.id}>
                        <h3 className="detail-preview-title">{insight.title}</h3>
                        <p className="detail-preview-summary">{insight.summary}</p>
                        <p className="detail-preview-body">{insight.content}</p>
                      </article>
                    ))}
                  </div>
                ) : (
                  <p className="detail-empty">这条故事暂时还没有解读。</p>
                )}
              </section>

              <section className="detail-panel">
                <div className="detail-panel-head">
                  <h2 className="detail-panel-title">最新讨论</h2>
                  <span className="detail-panel-note">按最近更新展示</span>
                </div>

                {preview.discussions.length > 0 ? (
                  <div className="detail-panel-list">
                    {preview.discussions.map((discussion) => (
                      <article className="detail-preview-card detail-discussion-card" key={discussion.id}>
                        <p className="detail-preview-body">{discussion.content}</p>
                      </article>
                    ))}
                  </div>
                ) : (
                  <p className="detail-empty">这条故事暂时还没有讨论。</p>
                )}
              </section>
            </div>
          </article>

          <aside className="detail-side">
            <div className="detail-continue">
              <h2 className="side-title">继续浏览</h2>
              <p className="detail-continue-text">
                如果这个故事还没看够，可以回到故事流，继续挑一个故事看看不同的理解。
              </p>
              <Link href="/" className="detail-continue-link">
                继续看其他故事
              </Link>
            </div>

            <div className="detail-sidebar-block">
              <h2 className="side-title">你能在这里看到什么</h2>
              <ul className="side-list">
                <li className="side-item">这个故事最核心的一句话梗概</li>
                <li className="side-item">不同角色的解读与讨论</li>
                <li className="side-item">当前热度与关注趋势</li>
                <li className="side-item">你也可以收藏并持续追踪</li>
              </ul>
            </div>
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
