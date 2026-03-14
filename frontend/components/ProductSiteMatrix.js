import StatusLight from "./StatusLight";

function scoreClass(score) {
  if (score > 85) return "text-emerald-600";
  if (score >= 70) return "text-amber-600";
  return "text-rose-600";
}

export default function ProductSiteMatrix({ rows, products, sites }) {
  const lookup = new Map(rows.map((row) => [`${row.product_id}-${row.site_id}`, row]));

  return (
    <div className="panel overflow-auto">
      <div className="mb-4">
        <h3 className="text-lg font-semibold">Product x Site Stability Matrix</h3>
        <p className="text-sm text-slate-500">Latest Process Stability Score snapshot by product and network site.</p>
      </div>
      <table className="min-w-full border-separate border-spacing-y-2 text-sm">
        <thead>
          <tr className="text-slate-500">
            <th className="px-2 py-2 text-left">Product</th>
            {sites.map((site) => (
              <th key={site.site_id} className="px-2 py-2 text-center">
                {site.site_name}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.product_id} className="rounded-2xl bg-slate-50">
              <td className="rounded-l-2xl px-2 py-3 font-medium">{product.product_name}</td>
              {sites.map((site) => {
                const row = lookup.get(`${product.product_id}-${site.site_id}`);
                return (
                  <td key={site.site_id} className="px-2 py-3 text-center">
                    {row ? (
                      <div className="flex items-center justify-center gap-2">
                        <StatusLight status={row.status} />
                        <span className={`font-semibold ${scoreClass(row.process_stability_score)}`}>
                          {row.process_stability_score.toFixed(1)}
                        </span>
                      </div>
                    ) : (
                      <span className="text-slate-300">-</span>
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
