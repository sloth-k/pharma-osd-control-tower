export default function StatusLight({ status }) {
  const styles = {
    GREEN: "bg-emerald-500 shadow-emerald-300/80",
    AMBER: "bg-amber-400 shadow-amber-300/80",
    RED: "bg-rose-500 shadow-rose-300/80",
  };

  return <span className={`inline-flex h-3 w-3 rounded-full shadow-lg ${styles[status] || styles.AMBER}`} />;
}
