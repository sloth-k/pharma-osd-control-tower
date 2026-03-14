const severityClass = {
  HIGH: "metric-pill-red",
  MEDIUM: "metric-pill-amber",
  LOW: "metric-pill-green",
};

export default function AlertTable({ alerts }) {
  return (
    <div className="panel">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold">Top Alerts</h3>
          <p className="text-sm text-slate-500">Review-by-exception view across sites, products, and batches.</p>
        </div>
      </div>
      <div className="overflow-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="text-slate-500">
            <tr>
              <th className="pb-3">Severity</th>
              <th className="pb-3">Metric</th>
              <th className="pb-3">Batch</th>
              <th className="pb-3">Message</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((alert) => (
              <tr key={alert.alert_id} className="border-t border-slate-200">
                <td className="py-3">
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${severityClass[alert.severity] || severityClass.MEDIUM}`}>
                    {alert.severity}
                  </span>
                </td>
                <td className="py-3 font-medium">{alert.metric_name}</td>
                <td className="py-3">#{alert.batch_id}</td>
                <td className="py-3 text-slate-600">{alert.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
