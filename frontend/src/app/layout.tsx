import type { Metadata } from "next";
import Form from "next/form";
import Link from "next/link";
import "./globals.css";
 
export const metadata: Metadata = {
  title: "tech-digest",
  description: "Zenn / Qiita の新着記事を AI で要約",
};
 
export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="ja">
      <body className="bg-white text-zinc-900 antialiased dark:bg-zinc-950 dark:text-zinc-100">
        <header className="border-b border-zinc-200 dark:border-zinc-800">
          <div className="mx-auto flex max-w-3xl items-center gap-4 px-4 py-3">
            <Link href="/" className="font-bold">
              tech-digest
            </Link>
            <Form action="/search" className="ml-auto flex gap-2">
              <input
                name="q"
                placeholder="意味で検索"
                className="w-48 rounded border border-zinc-300 px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
              />
              <button
                type="submit"
                className="rounded bg-zinc-900 px-3 py-1 text-sm text-white dark:bg-zinc-100 dark:text-zinc-900"
              >
                検索
              </button>
            </Form>
          </div>
        </header>
        <main className="mx-auto max-w-3xl px-4 py-6">{children}</main>
      </body>
    </html>
  );
}
