import Layout from "../components/Layout";
import ScoreCard from "../components/ScoreCard";
import TrendChart from "../charts/TrendChart";
import { getProductHealth } from "../lib/api";

export async function getServerSideProps() {
  const data = await getProductHealth(1);
  return { props: data };
}

function buildTrendDataset(kpiTrends) {
  const selected = ["Granulation_Torque_CV", "Dryer_Temp_Stability", "Compression_Force_CV", "Coating_Spray_Stability"];
  const maxLength = Math.max(0, ...selected.map((key) => (kpiTrends[key] || []).length));
  return Array.from({ length: maxLength }).map((_, index) => {
    const row = { label: `Batch ${index + 1}` };
    selected.forEach((key) => {
      row[key] = kpiTrends[key]?.[index]?.score ?? null;
    });
    return row;
  });
}

export default function ProductHealth({ product, stage_scores, kpi_trends }) {
  const trendData = buildTrendDataset(kpi_trends);

  return (
    <Layout
      title={`Product Health: ${product.product_name}`}
      subtitle="Stage-level stability and leading indicator trends for a selected OSD product."
    >
      <section className="grid gap-4 md:grid-cols-5">
        <ScoreCard label="Granulation" value={stage_scores.granulation?.toFixed?.(1) || "0.0"} tone="green" />
        <ScoreCard label="Drying" value={stage_scores.drying?.toFixed?.(1) || "0.0"} tone="amber" />
        <ScoreCard label="Blending" value={stage_scores.blending?.toFixed?.(1) || "0.0"} tone="blue" />
        <ScoreCard label="Compression" value={stage_scores.compression?.toFixed?.(1) || "0.0"} tone="red" />
        <ScoreCard label="Coating" value={stage_scores.coating?.toFixed?.(1) || "0.0"} tone="green" />
      </section>

      <section className="mt-6">
        <TrendChart
          title="KPI Trend Overlay"
          subtitle="Leading indicator scores across recent batches."
          data={trendData}
          lines={[
            { key: "Granulation_Torque_CV" },
            { key: "Dryer_Temp_Stability" },
            { key: "Compression_Force_CV" },
            { key: "Coating_Spray_Stability" },
          ]}
        />
      </section>
    </Layout>
  );
}
