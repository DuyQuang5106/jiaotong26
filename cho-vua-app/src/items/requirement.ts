import { iv, scale } from '../domain/interval'
import type { CargoRequirement, Interval } from '../domain/types'
import data from '../data/items.json'

export type ItemId =
  | 'ong_nhua' | 'thep_cay' | 'ton_tam' | 'tu_lanh' | 'may_giat'
  | 'nem' | 'bao_xi_mang' | 'cua_go' | 'thung_carton' | 'khac'

export interface ItemCategory {
  id: ItemId
  name: string
  dimsCm: { l: Interval; w: Interval; h: Interval }
  standardLengthsCm: number[]
  kgPerUnit: Interval | null
  looseMaterial: boolean
  /** Sample values — replace with the pilot store's catalog. */
  assumption: true
}

export const ITEMS = data as ItemCategory[]
export const ITEM_IDS = ITEMS.map(i => i.id)

/** Snap a measured length to the single standard product length it can be; otherwise keep it. */
export function snapLength(a: Interval, standards: number[], tolRel = 0.1): Interval {
  const hits = standards.filter(s => s >= a.min * (1 - tolRel) && s <= a.max * (1 + tolRel))
  return hits.length === 1 ? iv(hits[0] - 2, hits[0] + 2) : a
}

/**
 * The bed a vehicle needs. Measurements override typical dimensions; quantity
 * changes weight only (the demo treats the goods as one bundle).
 */
export function requirementFor(
  item: ItemCategory,
  qty: number,
  measured: Partial<{ l: Interval; w: Interval; h: Interval }>,
): CargoRequirement {
  const l = measured.l ?? item.dimsCm.l
  return {
    lengthCm: snapLength(l, item.standardLengthsCm),
    widthCm: measured.w ?? item.dimsCm.w,
    heightCm: measured.h ?? item.dimsCm.h,
    weightKg: item.kgPerUnit ? scale(item.kgPerUnit, qty) : null,
  }
}
