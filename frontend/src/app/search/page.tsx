import { Suspense } from "react";
import { ArticleCard } from "@/components/article-card";
import { searchArticles } from "@/lib/api";
import { first } from "@/lib/params";

export default function SearchPage({ searchParams }: PageProps<"/search">) {
  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">意味検索</h1>
      <Suspense fallback={<p className="text-sm text-zinc-500">検索中…</p>}>
        <SearchResults searchParams={searchParams} />
      </Suspense>
    </div>
  );
}

async function SearchResults({ searchParams }: Pick<PageProps<"/search">, "searchParams">) {
  const q = first((await searchParams).q)?.trim();
  if (!q) {
    return <p className="text-sm text-zinc-500">上の検索欄にキーワードを入れてください。</p>;
  }

  const results = await searchArticles(q);

  return (
    <div className="space-y-3">
      <p className="text-sm text-zinc-500">「{q}」に意味が近い記事</p>
      {results.map((r) => (
        <ArticleCard key={r.id} article={r} distance={r.distance} />
      ))}
    </div>
  );
}
