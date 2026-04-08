import Link from "next/link";

import { fetchStory } from "@/lib/api";

type StoryDetailProps = {
  params: {
    storyId: string;
  };
};

export default async function StoryDetailPage({ params }: StoryDetailProps) {
  const { story } = await fetchStory(params.storyId);

  return (
    <main className="container">
      <Link href="/" className="muted">
        返回故事流
      </Link>
      <article className="card section">
        <h1>{story.title}</h1>
        <p>{story.summary}</p>
        <div className="meta">
          <span>订阅 {story.subscriber_count}</span>
          <span>讨论 {story.discussion_count}</span>
          <span>存疑 {story.doubt_count}</span>
          <span>阅读 {story.view_count}</span>
        </div>
      </article>
    </main>
  );
}

