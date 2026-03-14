import Layout from "../components/Layout";
import GaugeCard from "../components/GaugeCard";
import TrendChart from "../charts/TrendChart";
import { getBatchData } from "../lib/api";

export async function getServerSideProps() {
  const kpis = await getBatchData(1);
  return { props: { kpis } };
}

function findScore(kpis, metricName) {
  return kpis.find((metric) => metric.metric_name === metricName)?.metric_score ?? 0;
}

function buildRealtimeTrend(kpis) {
  return kpis.slice(0, 10).map((kpi, index) => ({
    label: `T${index + 1}`,
    score: Number(kpi.metric_score?.toFixed?.(1) || 0),
    value: Number(kpi.metric_value?.toFixed?.(2) || 0),
  }));
}

export default function BatchMonitoring({ kpis }) {
  const realtimeTrend = buildRealtimeTrend(kpis);

  return (
    <Layout
      title="Batch Monitoring"
      subtitle="Real-time KPI watchlist for a selected batch with proactive focus on process instability."
    >
      <section className="grid gap-4 md:grid-cols-3">
        <GaugeCard label="Compression Force Variability" value={findScore(kpis, "Compression_Force_CV")} />
        <GaugeCard label="Torque Stability" value={findScore(kpis, "Granulation_Torque_CV")} />
        <GaugeCard label="Drying Temperature Stability" value={findScore(kpis, "Dryer_Temp_Stability")} />
      </section>

      <section className="mt-6">
        <TrendChart
          title="Live KPI Stream"
          subtitle="Batch-level KPI values and scores for the current watch window."
          data={realtimeTrend}
          lines={[{ key: "score" }, { key: "value" }]}
        />
      </section>
    </Layout>
  );
}
