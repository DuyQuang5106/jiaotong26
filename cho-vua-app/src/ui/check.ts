import { fmtM, worst } from '../domain/interval'
import type { Finding, Interval, Light, LoadInput, VehicleKind } from '../domain/types'
import { ITEMS, requirementFor, type ItemCategory, type ItemId } from '../items/requirement'
import type { measureRear, measureSide } from '../measure/measure'
import { evaluateLoad } from '../rules/evaluate'
import { predictMotorbike } from '../rules/predict'
import { matchVehicles, VEHICLES, type City, type VehicleOption } from '../services/match'

type Geometry = Pick<LoadInput, 'sideLeftCm' | 'sideRightCm' | 'rearCm' | 'frontCm' | 'heightCm'>

export interface CheckState {
  /** At the counter before loading, or a vehicle that is already loaded. */
  stage: 'pre_load' | 'loaded'
  vehicle: VehicleKind
  city: City
  km: number
  itemId: ItemId
  qty: number
  /** Dimensions of the goods themselves. */
  measured: Partial<{ l: Interval; w: Interval; h: Interval }>
  /** Overhang entered by hand for a loaded vehicle (tape measure). */
  manualLoad: Partial<Geometry>
  photo: {
    rear?: ReturnType<typeof measureRear>
    side?: ReturnType<typeof measureSide>
    refKind?: 'aruco' | 'plate'
    /** Reference corners tapped by hand (uncalibrated) — such photos cannot give green. Unknown counts as tapped. */
    rearTapped?: boolean
    sideTapped?: boolean
  }
  answers: Pick<LoadInput, 'plateAndLightsVisible' | 'redMarker' | 'lashingOk' | 'carryingBulky' | 'towing' | 'looseCovered' | 'registered' | 'bodyLengthCm'>
  weightKgManual: Interval | null
  vehicleMaxKg: number | null
}

export type SizeSource = 'nhập tay' | 'thẻ chuẩn' | 'biển số' | 'kích thước điển hình (giả định)'

export interface CheckResult {
  item: ItemCategory
  sizeText: string
  sizeSource: SizeSource
  /** True when the overhang comes from the assumed motorbike rack, not a measurement. */
  rackAssumed: boolean
  findings: Finding[]
  overall: Light
  options: VehicleOption[]
}

const EMPTY: Geometry = { sideLeftCm: null, sideRightCm: null, rearCm: null, frontCm: null, heightCm: null }

export function itemById(id: ItemId): ItemCategory {
  return ITEMS.find(i => i.id === id) ?? ITEMS.find(i => i.id === 'khac')!
}

type Dim = keyof Geometry
/** Where each overhang/height value came from. Only 'tape' and 'card' may produce green. */
type Provenance = 'tape' | 'card' | 'tapped' | 'assumed'

interface GeometryResult { g: Geometry; prov: Partial<Record<Dim, Provenance>>; source: SizeSource; rackAssumed: boolean; extends: boolean | null }

function geometryOf(s: CheckState, req: ReturnType<typeof requirementFor>): GeometryResult {
  const hasManualItem = Object.keys(s.measured).length > 0
  const g: Geometry = { ...EMPTY }
  const prov: GeometryResult['prov'] = {}
  const put = (d: Dim, v: Interval | null | undefined, p: Provenance) => { if (v) { g[d] = v; prov[d] = p } }

  if (s.stage === 'loaded' || s.photo.rear || s.photo.side) {
    // Photo first, then tape on top: a tape value is the more trusted source for its dimension.
    const rearP: Provenance = s.photo.rearTapped === false ? 'card' : 'tapped'
    const sideP: Provenance = s.photo.sideTapped === false ? 'card' : 'tapped'
    put('sideLeftCm', s.photo.rear?.sideLeftCm, rearP)
    put('sideRightCm', s.photo.rear?.sideRightCm, rearP)
    put('heightCm', s.photo.rear?.heightCm, rearP)
    put('rearCm', s.photo.side?.rearCm, sideP)
    for (const d of Object.keys(EMPTY) as Dim[]) put(d, s.manualLoad[d], 'tape')
    const fromPhoto = Object.values(prov).some(p => p !== 'tape')
    const anyTape = Object.values(prov).some(p => p === 'tape')
    const source: SizeSource = fromPhoto && !anyTape ? (s.photo.refKind === 'aruco' ? 'thẻ chuẩn' : 'biển số')
      : anyTape || hasManualItem ? 'nhập tay' : 'kích thước điển hình (giả định)'
    return { g, prov, source, rackAssumed: false, extends: extendsFrom(g) }
  }

  const source: SizeSource = hasManualItem ? 'nhập tay' : 'kích thước điển hình (giả định)'
  if (s.vehicle === 'motorbike') {
    const p = predictMotorbike(req)
    // Typical catalog sizes say nothing about this load (or how many pieces are stacked): never green.
    const pv: Provenance = hasManualItem ? 'tape' : 'assumed'
    put('sideLeftCm', p.sideLeftCm, pv); put('sideRightCm', p.sideRightCm, pv)
    put('rearCm', p.rearCm, pv); put('heightCm', p.heightCm, pv)
    return { g, prov, source, rackAssumed: true, extends: p.extendsBeyondVehicle }
  }
  // No pre-load prediction for other vehicles in the demo.
  return { g, prov, source, rackAssumed: false, extends: null }
}

/** true: surely sticks out; false: surely does not; null: cannot tell (keeps the red-marker check). */
function extendsFrom(g: Geometry): boolean | null {
  const parts = [g.rearCm, g.frontCm].filter((x): x is Interval => x !== null)
  if (parts.length === 0) return null
  if (parts.some(p => p.min > 0)) return true
  return parts.some(p => p.max > 0) ? null : false
}

const DIMS_OF: Partial<Record<Finding['code'], Dim[]>> = {
  E01: ['sideLeftCm', 'sideRightCm'],
  E02: ['rearCm', 'frontCm'],
  E03: ['heightCm'],
}

/** A green on E01–E03 needs every value behind it to be taped or from a detected card. */
function capUncalibrated(findings: Finding[], prov: GeometryResult['prov']): Finding[] {
  return findings.map(f => {
    const dims = DIMS_OF[f.code]
    if (!dims || f.light !== 'green') return f
    const weak = dims.map(d => prov[d]).filter(p => p === 'tapped' || p === 'assumed')
    if (weak.length === 0) return f
    const why = weak.includes('assumed')
      ? ' Ước theo kích thước điển hình và giá chở hàng giả định — cần đo lô hàng thật.'
      : ' Đo bằng góc chạm tay, chưa hiệu chỉnh — kiểm lại bằng thước hoặc thẻ chuẩn.'
    return { ...f, light: 'yellow' as const, detail: f.detail + why }
  })
}

export function runCheck(s: CheckState): CheckResult {
  const item = itemById(s.itemId)
  const req = requirementFor(item, s.qty, s.measured)
  const { g, prov, source, rackAssumed, extends: ext } = geometryOf(s, req)
  const input: LoadInput = {
    vehicle: s.vehicle,
    ...g,
    ...s.answers,
    extendsBeyondVehicle: ext,
    looseMaterial: item.looseMaterial,
    weightKg: s.weightKgManual ?? req.weightKg,
    vehicleMaxKg: s.vehicleMaxKg,
  }
  const findings = capUncalibrated(evaluateLoad(input).findings, prov)
  const overall = worst(findings.map(f => f.light))
  return {
    item,
    sizeText: `Dài ${fmtM(req.lengthCm)}, rộng ${fmtM(req.widthCm)}, cao ${fmtM(req.heightCm)}`,
    sizeSource: source,
    rackAssumed,
    findings,
    overall,
    options: matchVehicles(req, VEHICLES, s.city, s.km),
  }
}
