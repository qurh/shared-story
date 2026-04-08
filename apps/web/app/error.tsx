"use client";

import { useEffect } from "react";

type ErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <main className="container">
      <section className="notice notice-error" role="alert">
        <h1 className="error-title">内容暂时无法显示</h1>
        <p className="error-text">别担心，刷新一下通常就能继续浏览。</p>
        <button className="error-action" type="button" onClick={reset}>
          再试一次
        </button>
      </section>
    </main>
  );
}
