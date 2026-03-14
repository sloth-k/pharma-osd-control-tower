export default function GaugeCard({ label, value, unit = "" }) {
  const circumference = 2 * Math.PI * 54;
  const normalized = Math.max(0, Math.min(value, 100));
  const dash = (normalized / 100) * circumference;
  const tone = normalized > 85 ? "#14b8a6" : normalized >= 70 ? "#f59e0b" : "#ef4444";

  return (
    <div className="panel flex flex-col items-center text-center">
      <svg width="150" height="100" viewBox="0 0 150 100" className="overflow-visible">
        <path d="M20 80 A55 55 0 0 1 130 80" fill="none" stroke="#e2e8f0" strokeWidth="12" strokeLinecap="round" />
        <path
          d="M20 80 A55 55 0 0 1 130 80"
          fill="none"
          stroke={tone}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={`${dash} ${circumference}`}
        />
      </svg>
      <p className="text-3xl font-semibold">{value.toFixed(1)}{unit}</p>
      <p className="mt-1 text-sm text-slate-500">{label}</p>
    </div>
  );
}
