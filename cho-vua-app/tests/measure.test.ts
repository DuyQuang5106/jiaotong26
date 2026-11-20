import { expect, test } from 'vitest'
import { applyH, computeHomography, type Pt } from '../src/measure/homography'
import { halfWidthCm, MeasureError, measureRear, measureSide, type Reference, type RearTaps } from '../src/measure/measure'

// Synthetic photo: 10 px per cm, no perspective; a 19×14 cm plate with its top-left at (500, 600) px.
const plate: Reference = { kind: 'plate', cornersPx: [{ x: 500, y: 600 }, { x: 690, y: 600 }, { x: 690, y: 740 }, { x: 500, y: 740 }], sizeCm: { w: 19, h: 14 } }

function taps(o: { rackLeftX?: number; cargoLeftX?: number; rackRightX?: number; cargoRightX?: number; topY?: number; groundY?: number }): RearTaps {
  const y = 650
  return {
    rackLeft: { x: o.rackLeftX ?? 400, y }, cargoLeft: { x: o.cargoLeftX ?? 300, y },
    rackRight: { x: o.rackRightX ?? 800, y }, cargoRight: { x: o.cargoRightX ?? 900, y },
    cargoTop: { x: 600, y: o.topY ?? 100 }, ground: { x: 600, y: o.groundY ?? 900 },
  }
}

const contains = (a: { min: number; max: number }, v: number) => a.min <= v && v <= a.max

test('identity-scale homography maps 190 px to 19 cm', () => {
  const H = computeHomography(plate.cornersPx, [{ x: 0, y: 0 }, { x: 19, y: 0 }, { x: 19, y: 14 }, { x: 0, y: 14 }])
  expect(applyH(H, { x: 690, y: 600 }).x).toBeCloseTo(19, 6)
})

test('perspective H round-trip within 1e-6', () => {
  const known = [1.2, 0.1, 30, 0.05, 0.9, 10, 0.0005, 0.0002, 1]
  const src: [Pt, Pt, Pt, Pt] = [{ x: 0, y: 0 }, { x: 100, y: 0 }, { x: 100, y: 100 }, { x: 0, y: 100 }]
  const dst = src.map(p => applyH(known, p)) as [Pt, Pt, Pt, Pt]
  const H = computeHomography(src, dst)
  H.forEach((h, i) => expect(h).toBeCloseTo(known[i], 6))
})

test('left overhang 40 cm contains 40', () => {
  const r = measureRear(plate, taps({ rackLeftX: 400, cargoLeftX: 0 }))
  expect(contains(r.sideLeftCm, 40)).toBe(true)
})

test('right overhang and height are measured', () => {
  const r = measureRear(plate, taps({}))
  expect(contains(r.sideRightCm, 10)).toBe(true)
  expect(contains(r.heightCm, 80)).toBe(true)
})

test('reversed taps give zero not negative', () => expect(measureRear(plate, taps({ rackLeftX: 400, cargoLeftX: 450 })).sideLeftCm.min).toBe(0))

test('plate wider than aruco uncertainty', () => expect(halfWidthCm(40, plate, 0.1)).toBeGreaterThan(halfWidthCm(40, { ...plate, kind: 'aruco' }, 0.1)))

test('collinear corners throw degenerate_reference', () => {
  const bad: Reference = { ...plate, cornersPx: [{ x: 0, y: 0 }, { x: 10, y: 0 }, { x: 20, y: 0 }, { x: 30, y: 0 }] }
  expect(() => measureRear(bad, taps({}))).toThrow(MeasureError)
  try { measureRear(bad, taps({})) } catch (e) { expect((e as MeasureError).reason).toBe('degenerate_reference') }
})

test('missing tap throws missing_taps', () => {
  const t = { ...taps({}), ground: undefined } as unknown as RearTaps
  try { measureRear(plate, t); expect.unreachable() } catch (e) { expect((e as MeasureError).reason).toBe('missing_taps') }
})

test('side photo: 60 cm behind the rack', () => {
  const r = measureSide(plate, { rackRearEnd: { x: 500, y: 650 }, cargoRearEnd: { x: 1100, y: 650 } })
  expect(contains(r.rearCm, 60)).toBe(true)
})
