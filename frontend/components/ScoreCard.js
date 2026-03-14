export default function ScoreCard({ label, value, tone = "blue" }) {
  const toneMap = {
    blue: "from-sky-500 to-cyan-400",
    green: "from-emerald-500 to-teal-400",
    amber: "from-amber-500 to-orange-400",
    red: "from-rose-500 to-red-400",
  };

  return (
    <div className="panel overflow-hidden p-0">
      <div className={`bg-gradient-to-r ${toneMap[tone]} px-5 py-4 text-white`}>
        <p className="text-xs uppercase tracking-[0.25em] text-white/80">{label}</p>
        <p className="mt-3 text-4xl font-semibold">{value}</p>
      </div>
    </div>
  );
}
