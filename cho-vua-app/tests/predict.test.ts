import { expect, test } from 'vitest'
import { evaluateLoad } from '../src/rules/evaluate'
import { predictMotorbike } from '../src/rules/predict'
import { base, box, code, pipe } from './helpers/fixtures'

test('4 m pipe on motorbike is red', () => expect(evaluateLoad({ ...base(), ...predictMotorbike(pipe(398, 402)) }).overall).toBe('red'))
// It may stick out up to 11 cm behind the rack, so the red-marker question (E05) stays open.
test('carton 40×30×30 on motorbike is within the size limits', () => {
  const r = evaluateLoad({ ...base(), redMarker: null, ...predictMotorbike(box(40, 30, 30)) })
  expect(['E01', 'E02', 'E03'].map(c => code(r, c as 'E01').light)).toEqual(['green', 'green', 'green'])
  expect(code(r, 'E05').light).toBe('yellow')
})
test('fridge 160 high + rack 70–90 is red E03', () => expect(code(evaluateLoad({ ...base(), ...predictMotorbike(box(60, 65, 160)) }), 'E03').light).toBe('red'))
test('long load extends beyond vehicle', () => expect(predictMotorbike(pipe(398, 402)).extendsBeyondVehicle).toBe(true))
test('uncertain rear overhang is not reported as "does not stick out"', () => {
  // along 89..91: rear 89−50−30 .. 91−30 = 9..61 → min > 0 → true; along 59..61: rear −21..31 → clamp 0..31 → unknown
  expect(predictMotorbike(box(60, 30, 20)).extendsBeyondVehicle).toBeNull()
})

test('ties stay lengthwise: 100×40 is yellow either way', () => {
  // lengthwise: side 0..5, rear 100−50−30..100−30 = 20..70 (yellow); crosswise: side 25..35 (yellow)
  const p = predictMotorbike(box(100, 40, 20))
  expect(p.sideLeftCm!.max).toBeLessThanOrEqual(6)
})
test('goes crosswise when strictly better: 40 long × 120 wide', () => {
  // as given: side (119..121 − 30..50)/2 = 34.5..45.5 → red; turned: rear 119..121 − 30..50 − 0..30 = 39..91 → yellow, side 0..5.5
  const p = predictMotorbike(box(40, 120, 20))
  expect(p.rearCm!.min).toBeGreaterThan(0)
  expect(p.sideLeftCm!.max).toBeLessThanOrEqual(6)
})
