import { expect, test } from 'vitest'
import { iv, sub, clamp0, lightVsMax, lightFromFlag, worst, fmtM } from '../src/domain/interval'

test('equal to limit is green', () => expect(lightVsMax(iv(40, 50), 50)).toBe('green'))
test('min above limit is red', () => expect(lightVsMax(iv(51, 60), 50)).toBe('red'))
test('straddling is yellow', () => expect(lightVsMax(iv(45, 55), 50)).toBe('yellow'))
test('missing is yellow', () => expect(lightVsMax(null, 50)).toBe('yellow'))
test('sub widens', () => expect(sub(iv(380, 420), iv(30, 50))).toEqual({ min: 330, max: 390 }))
test('clamp0', () => expect(clamp0(iv(-5, 10))).toEqual({ min: 0, max: 10 }))
test('flag', () => {
  expect(lightFromFlag(null, false)).toBe('yellow')
  expect(lightFromFlag(false, false)).toBe('red')
  expect(lightFromFlag(true, false)).toBe('green')
})
test('worst', () => expect(worst(['green', 'yellow', 'red'])).toBe('red'))
test('fmtM', () => expect(fmtM(iv(32, 40))).toBe('0,32–0,40 m'))
test('iv reorders', () => expect(iv(5, 1)).toEqual({ min: 1, max: 5 }))
