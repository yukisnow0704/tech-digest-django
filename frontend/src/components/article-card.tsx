import Link from "next/link";
import type { Article } from "@/lib/api";

const dateFormat = new Intl.DateTimeFormat("ja-JP", {
  dateStyle: "medium",
  timeStyle: "short",
  timeZone: "Asia/Tokyo",
});

type Props = {
  article: Article;
  distance?: number;
};

export function ArticleCard({ article, distance }: Props) {
  return (
    <article className="rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
      <div className="flex flex-wrap items-center gap-2 text-xs text-zinc-500">
        <span className="rounded bg-zinc-100 px-2 py-0.5 dark:bg-zinc-800">{article.source}</span>
        {article.category && (
          <Link
            href={`/?category=${article.category}`}
            className="rounded bg-blue-50 px-2 py-0.5 text-blue-700 dark:bg-blue-950 dark:text-blue-300"
          >
            {article.category}
          </Link>
        )}
        <time dateTime={article.published_at}>
          {dateFormat.format(new Date(article.published_at))}
        </time>
        {distance !== undefined && <span>distance {distance.toFixed(3)}</span>}
      </div>
      <h2 className="mt-2 font-semibold">
        <Link href={`/articles/${article.id}`} className="hover:underline">
          {article.title}
        </Link>
      </h2>
      {article.summary && (
        <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">{article.summary}</p>
      )}
    </article>
  );
}
