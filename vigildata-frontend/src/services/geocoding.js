// Reverse geocoding via Nominatim (OpenStreetMap). Sin API key.
// Devuelve { region, comuna } matcheados contra regionesData.
import { regionesData } from '../utils/regiones'

function normalizar(s) {
  return (s || '')
    .toString()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .trim()
}

function matchRegion(nombreRaw) {
  if (!nombreRaw) return null
  const n = normalizar(nombreRaw)
  // Nominatim suele devolver "Región Metropolitana de Santiago", "Región del Biobío", etc.
  for (const r of regionesData) {
    const nr = normalizar(r.nombre)
    if (n === nr || n.includes(nr) || nr.includes(n)) return r
  }
  // Fallback: comparar quitando palabras "region", "de", "del", "la"
  const limpio = n.replace(/\bregion\b|\bde\b|\bdel\b|\bla\b/g, '').replace(/\s+/g, ' ').trim()
  for (const r of regionesData) {
    const nr = normalizar(r.nombre).replace(/\bde\b|\bdel\b|\bla\b/g, '').replace(/\s+/g, ' ').trim()
    if (limpio === nr) return r
  }
  return null
}

function matchComuna(region, nombreRaw) {
  if (!region || !nombreRaw) return null
  const n = normalizar(nombreRaw)
  for (const c of region.comunas) {
    if (normalizar(c) === n) return c
  }
  // Match parcial
  for (const c of region.comunas) {
    const nc = normalizar(c)
    if (nc.includes(n) || n.includes(nc)) return c
  }
  return null
}

export async function reverseGeocode(lat, lon) {
  const url = new URL('https://nominatim.openstreetmap.org/reverse')
  url.searchParams.set('lat', lat)
  url.searchParams.set('lon', lon)
  url.searchParams.set('format', 'json')
  url.searchParams.set('addressdetails', '1')
  url.searchParams.set('accept-language', 'es')
  url.searchParams.set('zoom', '14')

  try {
    const r = await fetch(url.toString(), {
      headers: { Accept: 'application/json' },
    })
    if (!r.ok) return { region: '', comuna: '' }
    const data = await r.json()
    const addr = data.address || {}

    // Region: state (Chile) o region
    const regionRaw = addr.state || addr.region || ''
    // Comuna: city / town / municipality / county / village
    const comunaRaw =
      addr.city ||
      addr.town ||
      addr.municipality ||
      addr.county ||
      addr.village ||
      addr.suburb ||
      ''

    const region = matchRegion(regionRaw)
    const comuna = matchComuna(region, comunaRaw)

    return {
      region: region ? region.nombre : '',
      comuna: comuna || '',
    }
  } catch {
    return { region: '', comuna: '' }
  }
}
