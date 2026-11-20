import { fmtM } from '../domain/interval'
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
  photo: { rear?: ReturnType<typeof measureRear>; side?: ReturnType<typeof measureSide>; refKind?: 'aruco' | 'plate' }
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

function geometryOf(s: CheckState, req: ReturnType<typeof requirementFor>): { g: Geometry; source: SizeSource; rackAssumed: boolean; extends: boolean | null } {
  const hasManualItem = Object.keys(s.measured).length > 0
  if (s.photo.rear || s.photo.side) {
    const g: Geometry = { ...EMPTY, ...s.manualLoad, ...(s.photo.rear ?? {}), ...(s.photo.side ?? {}) }
    return { g, source: s.photo.refKind === 'aruco' ? 'thẻ chuẩn' : 'biển số', rackAssumed: false, extends: extendsFrom(g) }
  }
  if (s.stage === 'loaded') {
    const g: Geometry = { ...EMPTY, ...s.manualLoad }
    const any = Object.values(s.manualLoad).some(v => v != null)
    return { g, source: any ? 'nhập tay' : hasManualItem ? 'nhập tay' : 'kích thước điển hình (giả định)', rackAssumed: false, extends: extendsFrom(g) }
  }
  const source: SizeSource = hasManualItem ? 'nhập tay' : 'kích thước điển hình (giả định)'
  if (s.vehicle === 'motorbike') {
    const p = predictMotorbike(req)
    return { g: { ...EMPTY, ...p }, source, rackAssumed: true, extends: p.extendsBeyondVehicle }
  }
  // No pre-load prediction for other vehicles in the demo.
  return { g: EMPTY, source, rackAssumed: false, extends: null }
}

function extendsFrom(g: Geometry): boolean | null {
  if (g.rearCm === null && g.frontCm === null) return null
  return (g.rearCm?.min ?? 0) > 0 || (g.frontCm?.min ?? 0) > 0
}

export function runCheck(s: CheckState): CheckResult {
  const item = itemById(s.itemId)
  const req = requirementFor(item, s.qty, s.measured)
  const { g, source, rackAssumed, extends: ext } = geometryOf(s, req)
  const input: LoadInput = {
    vehicle: s.vehicle,
    ...g,
    ...s.answers,
    extendsBeyondVehicle: ext,
    looseMaterial: item.looseMaterial,
    weightKg: s.weightKgManual ?? req.weightKg,
    vehicleMaxKg: s.vehicleMaxKg,
  }
  const { findings, overall } = evaluateLoad(input)
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
