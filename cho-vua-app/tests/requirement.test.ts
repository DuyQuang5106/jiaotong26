import { expect, test } from 'vitest'
import { iv } from '../src/domain/interval'
import { ITEMS, requirementFor, snapLength } from '../src/items/requirement'
import { item } from './helpers/fixtures'

test('snap 385–410 to 400', () => expect(snapLength(iv(385, 410), [400, 600])).toEqual({ min: 398, max: 402 }))
test('no snap when two candidates', () => expect(snapLength(iv(380, 620), [400, 600])).toEqual({ min: 380, max: 620 }))
test('no snap without standards', () => expect(snapLength(iv(250, 260), [])).toEqual({ min: 250, max: 260 }))
test('measured overrides typical', () => expect(requirementFor(item('tu_lanh'), 1, { h: iv(158, 162) }).heightCm).toEqual({ min: 158, max: 162 }))
test('typical dims used when not measured', () => expect(requirementFor(item('tu_lanh'), 1, {}).heightCm).toEqual(item('tu_lanh').dimsCm.h))
test('pipe length snaps after measurement', () => expect(requirementFor(item('ong_nhua'), 10, { l: iv(395, 400) }).lengthCm).toEqual({ min: 398, max: 402 }))
test('weight scales by quantity', () => expect(requirementFor(item('bao_xi_mang'), 4, {}).weightKg).toEqual({ min: 200, max: 200 }))
test('unknown weight stays null', () => expect(requirementFor(item('ong_nhua'), 10, {}).weightKg).toBeNull())
test('every catalog item is marked as an assumption', () => expect(ITEMS.every(i => i.assumption === true)).toBe(true))
