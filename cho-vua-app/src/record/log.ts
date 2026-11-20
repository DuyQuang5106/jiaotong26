import type { Interval, Light, VehicleKind } from '../domain/types'
import type { ItemId } from '../items/requirement'
import type { CheckResult, CheckState } from '../ui/check'

const KEY = 'chovua.checks.v1'

type Dim = 'sideLeft' | 'sideRight' | 'rear' | 'height'

/** One check, kept on this device only. Numbers, never photos. */
export interface CheckRecord {
  id: string
  at: string
  vehicle: VehicleKind
  itemId: ItemId
  refKind: 'aruco' | 'plate' | 'manual' | 'none'
  app: Partial<Record<Dim, Interval>>
  overall: Light
  /** Tape-measure values (cm) entered in field mode. */
  tape?: Partial<Record<Dim, number>>
  note?: string
}

export function toRecord(s: CheckState, r: CheckResult, at: Date): CheckRecord {
  const rear = s.photo.rear, side = s.photo.side, ml = s.manualLoad
  const pick = <T>(...xs: (T | null | undefined)[]) => xs.find(x => x != null) ?? undefined
  const app: CheckRecord['app'] = {}
  const put = (k: Dim, v: Interval | undefined) => { if (v) app[k] = v }
  put('sideLeft', pick(rear?.sideLeftCm, ml.sideLeftCm))
  put('sideRight', pick(rear?.sideRightCm, ml.sideRightCm))
  put('rear', pick(side?.rearCm, ml.rearCm))
  put('height', pick(rear?.heightCm, ml.heightCm))
  const hasManual = Object.values(ml).some(v => v != null)
  return {
    id: `${at.getTime().toString(36)}-${Math.random().toString(36).slice(2, 7)}`,
    at: at.toISOString(),
    vehicle: s.vehicle,
    itemId: s.itemId,
    refKind: s.photo.refKind ?? (hasManual ? 'manual' : 'none'),
    app,
    overall: r.overall,
  }
}

function storage(store?: Storage): Storage | null {
  if (store) return store
  try { return globalThis.localStorage ?? null } catch { return null }
}

export function loadRecords(store?: Storage): CheckRecord[] {
  const s = storage(store)
  if (!s) return []
  try {
    const v = JSON.parse(s.getItem(KEY) ?? '[]')
    return Array.isArray(v) ? v : []
  } catch {
    return []
  }
}

function write(recs: CheckRecord[], store?: Storage): void {
  try { storage(store)?.setItem(KEY, JSON.stringify(recs)) } catch { /* storage full or blocked */ }
}

export function saveRecord(rec: CheckRecord, store?: Storage): void {
  write([...loadRecords(store), rec], store)
}

export function updateTape(id: string, tape: CheckRecord['tape'], store?: Storage, note?: string): void {
  write(loadRecords(store).map(r => (r.id === id ? { ...r, tape: { ...r.tape, ...tape }, ...(note !== undefined ? { note } : {}) } : r)), store)
}

const HEADER = 'id,at,vehicle,item,ref_kind,overall,side_left_min,side_left_max,side_right_min,side_right_max,rear_min,rear_max,height_min,height_max,tape_side_left,tape_side_right,tape_rear,tape_height,note'

function cell(v: string | number | undefined): string {
  if (v === undefined) return ''
  const s = String(v)
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s
}

export function toCsv(recs: CheckRecord[]): string {
  const dims: Dim[] = ['sideLeft', 'sideRight', 'rear', 'height']
  const rows = recs.map(r => [
    r.id, r.at, r.vehicle, r.itemId, r.refKind, r.overall,
    ...dims.flatMap(d => [r.app[d]?.min, r.app[d]?.max]),
    ...dims.map(d => r.tape?.[d]),
    r.note,
  ].map(cell).join(','))
  return [HEADER, ...rows].join('\n')
}
