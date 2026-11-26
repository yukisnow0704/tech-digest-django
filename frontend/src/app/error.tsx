"use client";
 
export default function ErrorPage({ retry }: { error: unknown; retry: () => void }) {
  return (
    <div className="space-y-3">
      <p>記事を読み込めませんでした。API か DB が止まっているかもしれません。</p>
      <button
        type="button"
        onClick={() => retry()}
        className="rounded border border-zinc-300 px-3 py-1 text-sm dark:border-zinc-700"
      >
        もう一度読み込む
      </button>
    </div>
  );
}
