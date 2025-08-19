// Lightweight client-side cache of college id->name (and name->id) for enriching UI results
// Used by pages/colleges/index.tsx

let loaded = false
let idToName = new Map<number | string, string>()
let nameToId = new Map<string, number | string>()

async function loadFromBackend(): Promise<boolean> {
  try {
    // Try to fetch a large page of colleges via Next.js API proxy to backend DB endpoint
    const res = await fetch('/api/colleges/list?limit=10000')
    if (!res.ok) return false
    const data = await res.json()
    const rows = Array.isArray(data?.colleges) ? data.colleges : []
    for (const r of rows) {
      const id = r.id ?? r.college_id ?? r._id
      const name = r.name || ''
      if (!id || !name) continue
      idToName.set(id, name)
      nameToId.set(name.toLowerCase(), id)
    }
    return idToName.size > 0
  } catch {
    return false
  }
}

async function loadFromPublicJson(): Promise<boolean> {
  const tryPaths = [
    '/data/all_colleges.json',
    '/comprehensive_college_database.json'
  ]
  for (const p of tryPaths) {
    try {
      const r = await fetch(p)
      if (!r.ok) continue
      const data = await r.json()
      const list = Array.isArray(data?.colleges) ? data.colleges : (Array.isArray(data) ? data : [])
      for (const c of list) {
        const id = c.id ?? c.college_id ?? c._id
        const name = c.name || ''
        if (!id || !name) continue
        idToName.set(id, name)
        nameToId.set(name.toLowerCase(), id)
      }
      if (idToName.size > 0) return true
    } catch {}
  }
  return false
}

export async function loadCollegeCache(): Promise<void> {
  if (loaded && idToName.size > 0) return
  idToName.clear()
  nameToId.clear()
  // Prefer backend for fresher names, fallback to public JSON
  const ok = await loadFromBackend()
  if (!ok) {
    await loadFromPublicJson()
  }
  loaded = true
}

export function getCollegeName(id: number | string | undefined | null, fallback?: string): string | undefined {
  if (id == null) return fallback
  return idToName.get(id) || fallback
}

export function getCollegeIdByName(name: string): number | string | undefined {
  return nameToId.get((name || '').toLowerCase())
}
