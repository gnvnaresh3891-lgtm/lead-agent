// Production API Client for SignalSDR Dashboard
// Connects to live FastAPI backend with fallback resilience

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://leadagent-backend.onrender.com/api';

async function fetchWithFallback<T>(endpoint: string, fallbackData: T): Promise<T> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000); // 4-second timeout

    const res = await fetch(`${API_BASE}${endpoint}`, {
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
      },
      next: { revalidate: 30 }, // Cache revalidation every 30s
    });

    clearTimeout(timeoutId);

    if (!res.ok) {
      console.warn(`API endpoint ${endpoint} returned status ${res.status}. Using local data fallback.`);
      return fallbackData;
    }

    const data = await res.json();
    return data as T;
  } catch (error) {
    console.warn(`API connection to ${endpoint} unavailable. Using resilient fallback.`, error);
    return fallbackData;
  }
}

export async function getDashboardAnalytics(fallback: any) {
  return fetchWithFallback('/analytics/dashboard', fallback);
}

export async function getSignalsFeed(fallback: any[]) {
  const data = await fetchWithFallback<{ signals: any[] }>('/signals', { signals: fallback });
  return data.signals || fallback;
}

export async function getLeadsPipeline(fallback: any) {
  return fetchWithFallback('/leads/pipeline', fallback);
}

export async function getCampaignsList(fallback: any[]) {
  const data = await fetchWithFallback<{ campaigns: any[] }>('/campaigns', { campaigns: fallback });
  return data.campaigns || fallback;
}

export async function getComplianceStats(fallback: any) {
  return fetchWithFallback('/compliance/stats', fallback);
}

export async function generateAIEmail(leadId: string, leadData: any) {
  try {
    const res = await fetch(`${API_BASE}/messages/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lead_id: leadId, lead: leadData }),
    });
    if (res.ok) {
      return await res.json();
    }
  } catch (e) {
    console.warn('Backend email generation fallback:', e);
  }
  return {
    subject: `Quick thought on ${leadData.company_name || 'your company'}`,
    body: `Hi ${leadData.first_name || 'there'}, noticed your recent growth signals. Would love to share how we can accelerate your outbound pipeline.`,
    quality_score: 92,
  };
}
