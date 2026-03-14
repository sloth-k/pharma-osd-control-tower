const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

async function fetchJson(path, fallback) {
  try {
    const response = await fetch(`${API_BASE}${path}`);
    if (!response.ok) {
      throw new Error(`API request failed for ${path}`);
    }
    return await response.json();
  } catch (error) {
    return fallback;
  }
}

export async function getDashboardData() {
  const [sites, products, scores, alerts] = await Promise.all([
    fetchJson("/sites", []),
    fetchJson("/products?limit=6", []),
    fetchJson("/stability_scores", []),
    fetchJson("/alerts", []),
  ]);

  return { sites, products, scores, alerts };
}

export async function getProductHealth(productId = 1) {
  return fetchJson(`/product_health/${productId}`, {
    product: { product_id: productId, product_name: `Product ${productId}`, dosage_form: "Tablet", strength: "500 mg" },
    stage_scores: { granulation: 82, drying: 79, blending: 86, compression: 74, coating: 88 },
    kpi_trends: {},
    recent_batches: [],
  });
}

export async function getBatchData(batchId = 1) {
  return fetchJson(`/kpis?batch_id=${batchId}`, []);
}

export async function getBenchmark(productId = 1) {
  return fetchJson(`/site_benchmark?product_id=${productId}`, []);
}
