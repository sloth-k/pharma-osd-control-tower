import Link from "next/link";
import { useRouter } from "next/router";

const nav = [
  { href: "/", label: "Network Control Tower" },
  { href: "/product-health", label: "Product Health" },
  { href: "/batch-monitoring", label: "Batch Monitoring" },
  { href: "/site-benchmarking", label: "Site Benchmarking" },
];

export default function Layout({ title, subtitle, children }) {
  const router = useRouter();

  return (
    <div className="min-h-screen px-4 py-6 md:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-6 flex flex-col gap-4 rounded-[32px] bg-ink px-6 py-6 text-white shadow-panel md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-cyan-200">Pharma OSD Analytics</p>
            <h1 className="mt-2 text-3xl font-semibold">{title}</h1>
            <p className="mt-2 max-w-3xl text-sm text-slate-300">{subtitle}</p>
          </div>
          <nav className="flex flex-wrap gap-2">
            {nav.map((item) => {
              const active = router.pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`rounded-full px-4 py-2 text-sm transition ${
                    active ? "bg-white text-ink" : "bg-white/10 text-white hover:bg-white/20"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </header>
        {children}
      </div>
    </div>
  );
}
