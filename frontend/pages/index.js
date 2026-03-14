import Layout from "../components/Layout";
import ProductSiteMatrix from "../components/ProductSiteMatrix";
import AlertTable from "../components/AlertTable";
import ScoreCard from "../components/ScoreCard";
import BarChartPanel from "../charts/BarChartPanel";
import { getDashboardData } from "../lib/api";

export async function getServerSideProps() {
  const data = await getDashboardData();
  return { props: data };
}

export default function Home({ sites, products, scores, alerts }) {
  const latestMatrix = products.map((product) =>
    sites.map((site) =>
      scores.find((score) => score.product_id === product.product_id && score.site_id === site.site_id)
    )
  );
  const matrixRows = latestMatrix.flat().filter(Boolean);

  const avgBySite = sites.map((site) => {
    const siteScores = scores.filter((row) => row.site_id === site.site_id);
    const value = siteScores.length
      ? siteScores.reduce((sum, row) => sum + row.process_stability_score, 0) / siteScores.length
      : 0;
    return { label: site.site_name.split(" ")[0], value: Number(value.toFixed(1)) };
  });

  const criticalCount = alerts.filter((alert) => alert.severity === "HIGH").length;
  const avgNetwork = scores.length
    ? (scores.reduce((sum, row) => sum + row.process_stability_score, 0) / scores.length).toFixed(1)
    : "0.0";

  return (
    <Layout
      title="Network Control Tower"
      subtitle="Proactive process health monitoring across a five-site oral solid dosage manufacturing network."
    >
      <section className="grid gap-4 md:grid-cols-3">
        <ScoreCard label="Network PSS" value={avgNetwork} tone="blue" />
        <ScoreCard label="Live Alerts" value={alerts.length} tone={criticalCount ? "red" : "green"} />
        <ScoreCard label="High Severity" value={criticalCount} tone={criticalCount ? "amber" : "green"} />
      </section>

      <section className="mt-6 grid gap-6 xl:grid-cols-[1.55fr,1fr]">
        <ProductSiteMatrix rows={matrixRows} products={products} sites={sites} />
        <BarChartPanel
          title="Site Stability"
          subtitle="Average Process Stability Score by site."
          data={avgBySite}
        />
      </section>

      <section className="mt-6">
        <AlertTable alerts={alerts} />
      </section>
    </Layout>
  );
}
