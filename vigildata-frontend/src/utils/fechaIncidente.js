/**
 * La API persiste `fecha` como naive en GMT-4 (UTC−4).
 * Convierte a Date para mostrar u ordenar con el instante correcto.
 */
export function parseFechaIncidenteGmt4(val) {
  if (val == null || val === '') return new Date(NaN)
  const s = String(val).trim()
  if (/[zZ]$|[+-]\d{2}:\d{2}$/.test(s)) return new Date(s)
  const head = s.length >= 19 && s[10] === 'T' ? s.slice(0, 19) : s
  if (head.length >= 19 && head[10] === 'T') return new Date(`${head}-04:00`)
  return new Date(s)
}
