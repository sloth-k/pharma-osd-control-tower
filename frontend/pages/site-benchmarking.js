import Layout from "../components/Layout";
import Heatmap from "../components/Heatmap";
import { getBenchmark, getDashboardData } from "../lib/api";

export async function getServerSideProps() {
  const [{ sites }, benchmark] = await Promise.all([getDashboardData(), getBenchmark(1)]);
  const grouped = benchmark.reduce((acc, row) => {
    if (!acc[row.product_id]) {
      acc[row.product_id] = { product_id: row.product_id, sites: [] };
    }
    acc[row.product_id].sites.push(row);
    return acc;
  }, {});

  return {
    props: {
      sites,
      data: Object.values(grouped).slice(0, 10),
    },
  };
}

export default function SiteBenchmarking({ sites, data }) {
  return (
    <Layout
      title="Site Benchmarking"
      subtitle="Cross-site comparison of the same product using Process Stability Score."
    >
      <Heatmap data={data} sites={sites} />
    </Layout>
  );
}
