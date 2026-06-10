const BASE = import.meta.env.VITE_API_BASE_URL ?? ''

export async function detectRice(imageBase64, basePrice = 0) {
  const res = await fetch(`${BASE}/detect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: imageBase64, base_price: parseFloat(basePrice) || 0 }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Server error ${res.status}`)
  }
  return res.json()
}

export async function fetchHistory(limit = 20) {
  const res = await fetch(`${BASE}/history?limit=${limit}`)
  if (!res.ok) throw new Error('Gagal memuat riwayat')
  return res.json()
}

export async function clearHistory() {
  const res = await fetch(`${BASE}/history`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Gagal hapus riwayat')
  return res.json()
}

export async function fetchStats() {
  const res = await fetch(`${BASE}/stats`)
  if (!res.ok) throw new Error('Gagal memuat statistik')
  return res.json()
}

export async function checkHealth() {
  try {
    const res = await fetch(`${BASE}/health`, { signal: AbortSignal.timeout(3000) })
    return res.ok
  } catch {
    return false
  }
}
