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
      <Link href="/" className="muted">
        返回故事流
      </Link>
      <article className="card section">
        {story ? (
          <>
            <h1>{story.title}</h1>
            <p>{story.summary}</p>
            <div className="meta">
              <span>订阅 {story.subscriber_count}</span>
              <span>讨论 {story.discussion_count}</span>
              <span>存疑 {story.doubt_count}</span>
              <span>阅读 {story.view_count}</span>
            </div>
          </>
        ) : (
          <p className="muted">内容暂时不可用：{loadError ?? "未知错误"}。</p>
        )}
      </article>
    </main>
  );
}

