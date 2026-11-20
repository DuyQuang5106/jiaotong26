import type { Interval, Light } from './types'

export function iv(min: number, max: number): Interval {
  return min <= max ? { min, max } : { min: max, max: min }
}

export function around(v: number, half: number): Interval {
  return iv(v - Math.abs(half), v + Math.abs(half))
}

export function add(a: Interval, b: Interval): Interval {
  return { min: a.min + b.min, max: a.max + b.max }
}

/** Conservative difference: every value a−b can take. */
export function sub(a: Interval, b: Interval): Interval {
  return { min: a.min - b.max, max: a.max - b.min }
}

export function scale(a: Interval, k: number): Interval {
  return iv(a.min * k, a.max * k)
}

export function clamp0(a: Interval): Interval {
  return { min: Math.max(0, a.min), max: Math.max(0, a.max) }
}

/** Law says "không vượt quá": equal to the limit is allowed. */
export function lightVsMax(a: Interval | null, limit: number): Light {
  if (a === null) return 'yellow'
  if (a.max <= limit) return 'green'
  if (a.min > limit) return 'red'
  return 'yellow'
}

/** Yes/no/unknown answer: null → yellow, value equal to `bad` → red. */
export function lightFromFlag(v: boolean | null, bad: boolean): Light {
  if (v === null) return 'yellow'
  return v === bad ? 'red' : 'green'
}

const RANK: Record<Light, number> = { green: 0, yellow: 1, red: 2 }

export function worst(ls: Light[]): Light {
  return ls.reduce<Light>((w, l) => (RANK[l] > RANK[w] ? l : w), 'green')
}

function m(cm: number): string {
  return (cm / 100).toFixed(2).replace('.', ',')
}

export function fmtM(a: Interval): string {
  return `${m(a.min)}–${m(a.max)} m`
}
