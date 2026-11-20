import { around, clamp0 } from '../domain/interval'
import type { Interval } from '../domain/types'
import { applyH, computeHomography, MeasureError, orderQuad, type Pt, type Quad } from './homography'

export { MeasureError }

export interface Reference {
  kind: 'aruco' | 'plate'
  /** True when the corners were tapped by hand (plate, or a card that was not detected). */
  tapped: boolean
  /** Four corners in image pixels; any order — they are sorted before use. */
  cornersPx: Quad
  sizeCm: { w: number; h: number }
}

export interface RearTaps { rackLeft: Pt; rackRight: Pt; cargoLeft: Pt; cargoRight: Pt; cargoTop: Pt; ground: Pt }
export interface SideTaps { rackRearEnd: Pt; cargoRearEnd: Pt }

/** Biển số xe mô tô theo QCVN 08:2024/BCA. */
export const PLATE_SIZE_CM = { w: 19, h: 14 } as const

// Provisional — recalibrate from field data (plan Task 10).
export const TAP_ERR_PX = 6
export const CORNER_ERR_PX = 2
export const OFF_PLANE_REL = { aruco: 0.03, plate: 0.05 } as const

const dist = (a: Pt, b: Pt) => Math.hypot(a.x - b.x, a.y - b.y)

function refSidePx(ref: Reference): number {
  const c = orderQuad(ref.cornersPx)
  return (dist(c[0], c[1]) + dist(c[1], c[2]) + dist(c[2], c[3]) + dist(c[3], c[0])) / 4
}

function cmPerPxOf(ref: Reference): number {
  const c = orderQuad(ref.cornersPx)
  return ref.sizeCm.w / ((dist(c[0], c[1]) + dist(c[3], c[2])) / 2)
}

/** Half-width of the uncertainty interval for a distance of dCm. */
export function halfWidthCm(dCm: number, ref: Reference, cmPerPx: number): number {
  // Hand-tapped corners are as imprecise as any other tap.
  const cornerErr = ref.tapped ? TAP_ERR_PX : CORNER_ERR_PX
  return Math.abs(dCm) * (cornerErr / refSidePx(ref) + OFF_PLANE_REL[ref.kind]) + TAP_ERR_PX * Math.SQRT2 * cmPerPx
}

function toPlane(ref: Reference) {
  const { w, h } = ref.sizeCm
  const H = computeHomography(orderQuad(ref.cornersPx), [{ x: 0, y: 0 }, { x: w, y: 0 }, { x: w, y: h }, { x: 0, y: h }])
  return (p: Pt) => applyH(H, p)
}

function requireTaps(points: (Pt | undefined)[]): void {
  if (points.some(p => !p || !Number.isFinite(p.x) || !Number.isFinite(p.y))) throw new MeasureError('missing_taps')
}

function overhang(dCm: number, ref: Reference, cmPerPx: number): Interval {
  return clamp0(around(dCm, halfWidthCm(dCm, ref, cmPerPx)))
}

/** Photo from behind: side overhang beyond each rack edge and height above the road. */
export function measureRear(ref: Reference, t: RearTaps): { sideLeftCm: Interval; sideRightCm: Interval; heightCm: Interval } {
  requireTaps([t?.rackLeft, t?.rackRight, t?.cargoLeft, t?.cargoRight, t?.cargoTop, t?.ground])
  const P = toPlane(ref)
  const k = cmPerPxOf(ref)
  // A mixed-up tap order must not quietly turn into a zero overhang.
  if (P(t.rackLeft).x >= P(t.rackRight).x || P(t.cargoTop).y >= P(t.ground).y) throw new MeasureError('bad_taps')
  const left = P(t.rackLeft).x - P(t.cargoLeft).x
  const right = P(t.cargoRight).x - P(t.rackRight).x
  const height = P(t.ground).y - P(t.cargoTop).y
  return { sideLeftCm: overhang(left, ref, k), sideRightCm: overhang(right, ref, k), heightCm: overhang(height, ref, k) }
}

/** Photo from the side (reference card on the side): how far goods reach behind the rack. */
export function measureSide(ref: Reference, t: SideTaps): { rearCm: Interval } {
  requireTaps([t?.rackRearEnd, t?.cargoRearEnd])
  const P = toPlane(ref)
  const d = Math.abs(P(t.cargoRearEnd).x - P(t.rackRearEnd).x)
  return { rearCm: overhang(d, ref, cmPerPxOf(ref)) }
}
