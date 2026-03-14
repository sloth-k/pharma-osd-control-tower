function cellColor(score) {
  if (score > 85) return "bg-emerald-400/90";
  if (score >= 70) return "bg-amber-400/90";
  return "bg-rose-400/90";
}

export default function Heatmap({ data, sites }) {
  return (
    <div className="panel">
      <div className="mb-4">
        <h3 className="text-lg font-semibold">Site Benchmark Heatmap</h3>
        <p className="text-sm text-slate-500">Average Process Stability Score by product and site.</p>
      </div>
      <div className="grid gap-3">
        {data.map((row) => (
          <div key={row.product_id} className="grid grid-cols-6 gap-3">
            <div className="rounded-2xl bg-slate-100 px-4 py-3 font-medium">Product {row.product_id}</div>
            {sites.map((site) => {
              const match = row.sites.find((item) => item.site_id === site.site_id);
              return (
                <div
                  key={site.site_id}
                  className={`rounded-2xl px-4 py-3 text-center font-semibold text-white ${cellColor(match?.avg_pss || 0)}`}
                >
                  {match ? match.avg_pss.toFixed(1) : "-"}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
