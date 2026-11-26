import Link from "next/link";
import { Suspense } from "react";
import { ArticleCard } from "@/components/article-card";
import { listArticles } from "@/lib/api";
import { CATEGORIES } from "@/lib/categories";
import { first } from "@/lib/params";

export default function HomePage({ searchParams }: PageProps<"/">) {
  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">新着記事</h1>
      <Suspense fallback={<p className="text-sm text-zinc-500">読み込み中…</p>}>
        <ArticleList searchParams={searchParams} />
      </Suspense>
    </div>
  );
}

function listHref(category: string | undefined, page: number) {
  const query = new URLSearchParams();
  if (category) query.set("category", category);
  if (page > 1) query.set("page", String(page));
  const qs = query.toString();
  return qs ? `/?${qs}` : "/";
}

async function ArticleList({ searchParams }: Pick<PageProps<"/">, "searchParams">) {
  const params = await searchParams;
  const category = first(params.category);
  const page = Number(first(params.page) ?? "1");

  const data = await listArticles({ category, page: String(page) });

  return (
    <>
      <nav className="flex flex-wrap gap-3 text-sm">
        <Link href="/" className={category ? "text-zinc-500" : "font-bold"}>
          すべて
        </Link>
        {CATEGORIES.map((c) => (
          <Link
            key={c}
            href={listHref(c, 1)}
            className={c === category ? "font-bold" : "text-zinc-500"}
          >
            {c}
          </Link>
        ))}
      </nav>

      <p className="text-sm text-zinc-500">{data.count} 件</p>

      <div className="space-y-3">
        {data.results.map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>

      <div className="flex justify-between text-sm">
        {data.previous ? <Link href={listHref(category, page - 1)}>← 前へ</Link> : <span />}
        {data.next ? <Link href={listHref(category, page + 1)}>次へ →</Link> : <span />}
      </div>
    </>
  );
}
