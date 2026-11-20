import { expect, test } from 'vitest'
import type { Pt } from '../src/measure/homography'
import { halfWidthCm, MeasureError, measureRear } from '../src/measure/measure'
import { measurePhoto, referenceFromTaps, shouldResetReference } from '../src/ui/photoMeasure'

// 10 px per cm; plate 19×14 cm with top-left at (500, 600) px.
const TL = { x: 500, y: 600 }, TR = { x: 690, y: 600 }, BR = { x: 690, y: 740 }, BL = { x: 500, y: 740 }
// True scene: 45 cm overhang each side of a rack spanning 400..800 px, cargo top 250 cm above the ground.
const rear = (o: Partial<Record<'rackLeft' | 'rackRight' | 'cargoLeft' | 'cargoRight' | 'cargoTop' | 'ground', Pt>> = {}) => ({
  rackLeft: { x: 400, y: 650 }, rackRight: { x: 800, y: 650 },
  cargoLeft: { x: -50, y: 650 }, cargoRight: { x: 1250, y: 650 },
  cargoTop: { x: 600, y: -1600 }, ground: { x: 600, y: 900 }, ...o,
})
const contains = (a: { min: number; max: number }, v: number) => a.min <= v && v <= a.max

for (const [name, order] of [['TR,TL,BL,BR', [TR, TL, BL, BR]], ['BL,BR,TR,TL', [BL, BR, TR, TL]], ['BR,BL,TL,TR', [BR, BL, TL, TR]]] as const) {
  test(`corner order ${name} still measures the true overhang`, () => {
    const r = measureRear({ kind: 'plate', tapped: true, cornersPx: [...order] as [Pt, Pt, Pt, Pt], sizeCm: { w: 19, h: 14 } }, rear())
    expect(contains(r.sideLeftCm, 45)).toBe(true)
    expect(contains(r.sideRightCm, 45)).toBe(true)
    expect(contains(r.heightCm, 250)).toBe(true)
  })
}

test('top tapped below the ground is rejected', () => {
  const ref = referenceFromTaps('plate', [TL, TR, BR, BL])
  try { measureRear(ref, rear({ cargoTop: { x: 600, y: 900 }, ground: { x: 600, y: -1600 } })); expect.unreachable() } catch (e) { expect((e as MeasureError).reason).toBe('bad_taps') }
})

test('rack edges tapped right-to-left are rejected', () => {
  const ref = referenceFromTaps('plate', [TL, TR, BR, BL])
  try { measureRear(ref, rear({ rackLeft: { x: 800, y: 650 }, rackRight: { x: 400, y: 650 } })); expect.unreachable() } catch (e) { expect((e as MeasureError).reason).toBe('bad_taps') }
})

test('hand-tapped corners get a wider interval than a detected card', () => {
  const tapped = referenceFromTaps('aruco', [TL, TR, BR, BL])
  expect(halfWidthCm(40, tapped, 0.1)).toBeGreaterThan(halfWidthCm(40, { ...tapped, tapped: false }, 0.1))
})

test('referenceFromTaps orders corners and marks them tapped', () => {
  const r = referenceFromTaps('plate', [BR, TL, BL, TR])
  expect(r.cornersPx).toEqual([TL, TR, BR, BL])
  expect(r.tapped).toBe(true)
  expect(r.sizeCm).toEqual({ w: 19, h: 14 })
})

test('measurePhoto: degenerate corners ask to re-tap the corners', () => {
  const out = measurePhoto('rear', { ...referenceFromTaps('plate', [TL, TR, BR, BL]), cornersPx: [{ x: 0, y: 0 }, { x: 10, y: 0 }, { x: 20, y: 0 }, { x: 30, y: 0 }] }, Object.values(rear()))
  expect(out).toMatchObject({ ok: false, resetReference: true })
  if (!out.ok) expect(out.message).toMatch(/chạm lại 4 góc/)
})

test('measurePhoto: wrong tap order asks to re-tap the points only', () => {
  const pts = Object.values(rear({ cargoTop: { x: 600, y: 900 }, ground: { x: 600, y: -1600 } }))
  const out = measurePhoto('rear', referenceFromTaps('plate', [TL, TR, BR, BL]), pts)
  expect(out).toMatchObject({ ok: false, resetReference: false })
  if (!out.ok) expect(out.message).toMatch(/thứ tự/i)
})

test('measurePhoto: success records that the reference was tapped', () => {
  const out = measurePhoto('rear', referenceFromTaps('plate', [TL, TR, BR, BL]), Object.values(rear()))
  expect(out.ok).toBe(true)
  if (out.ok) { expect(out.photo.rearTapped).toBe(true); expect(out.photo.rear).toBeDefined() }
})

test('reset clears a tapped reference but keeps a detected card', () => {
  expect(shouldResetReference(referenceFromTaps('aruco', [TL, TR, BR, BL]))).toBe(true)
  expect(shouldResetReference({ ...referenceFromTaps('aruco', [TL, TR, BR, BL]), tapped: false })).toBe(false)
})
