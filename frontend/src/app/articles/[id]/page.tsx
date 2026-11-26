import { notFound } from "next/navigation";
import { Suspense } from "react";
import { ArticleCard } from "@/components/article-card";
import { ApiError, getArticle, getSimilarArticles } from "@/lib/api";

export default function ArticlePage({ params }: PageProps<"/articles/[id]">) {
  return (
    <Suspense fallback={<p className="text-sm text-zinc-500">読み込み中…</p>}>
      <ArticleDetail params={params} />
    </Suspense>
  );
}

async function ArticleDetail({ params }: Pick<PageProps<"/articles/[id]">, "params">) {
  const { id } = await params;

  const [article, similar] = await Promise.all([getArticle(id), getSimilarArticles(id)]).catch(
    (error: unknown) => {
      if (error instanceof ApiError && error.status === 404) notFound();
      throw error;
    },
  );

  return (
    <div className="space-y-8">
      <section className="space-y-3">
        <ArticleCard article={article} />
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block text-sm text-blue-700 hover:underline dark:text-blue-300"
        >
          元の記事を読む →
        </a>
      </section>

      <section className="space-y-3">
        <h2 className="font-bold">似てる記事</h2>
        {similar.length === 0 ? (
          <p className="text-sm text-zinc-500">この記事はまだベクトルがありません。</p>
        ) : (
          similar.map((s) => <ArticleCard key={s.id} article={s} distance={s.distance} />)
        )}
      </section>
    </div>
  );
}
