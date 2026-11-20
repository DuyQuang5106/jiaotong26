import { expect, test } from 'vitest'
import { CARD_SIZE_CM, detectMarker } from '../src/measure/aruco'
import { blank, drawMarker } from './helpers/drawMarker'

test('detects synthetic marker corners within 2 px', () => {
  const cell = 20, off = { x: 100, y: 80 }, side = 7 * cell
  const r = detectMarker(drawMarker(0, cell, off))
  expect(r).not.toBeNull()
  const want = [{ x: off.x, y: off.y }, { x: off.x + side, y: off.y }, { x: off.x + side, y: off.y + side }, { x: off.x, y: off.y + side }]
  r!.cornersPx.forEach((c, i) => {
    expect(Math.abs(c.x - want[i].x)).toBeLessThanOrEqual(2)
    expect(Math.abs(c.y - want[i].y)).toBeLessThanOrEqual(2)
  })
})

test('detected reference is a 15 cm aruco card', () => {
  const r = detectMarker(drawMarker(0, 20, { x: 100, y: 80 }))!
  expect(r.kind).toBe('aruco')
  expect(r.sizeCm).toEqual({ w: CARD_SIZE_CM, h: CARD_SIZE_CM })
  expect(CARD_SIZE_CM).toBe(15)
})

test('blank image returns null', () => expect(detectMarker(blank(640, 480))).toBeNull())

test('a different marker id is ignored', () => expect(detectMarker(drawMarker(5, 20, { x: 100, y: 80 }))).toBeNull())
