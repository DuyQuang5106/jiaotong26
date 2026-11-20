import { expect, test } from 'vitest'
import { iv } from '../src/domain/interval'
import { ITEMS, requirementFor } from '../src/items/requirement'
import { item } from './helpers/fixtures'

test('measured overrides typical', () => expect(requirementFor(item('tu_lanh'), 1, { h: iv(158, 162) }).heightCm).toEqual({ min: 158, max: 162 }))
test('typical dims used when not measured', () => expect(requirementFor(item('tu_lanh'), 1, {}).heightCm).toEqual(item('tu_lanh').dimsCm.h))
test('measured length is kept as measured', () => expect(requirementFor(item('ong_nhua'), 10, { l: iv(429, 431) }).lengthCm).toEqual({ min: 429, max: 431 }))
test('weight scales by quantity', () => expect(requirementFor(item('bao_xi_mang'), 4, {}).weightKg).toEqual({ min: 200, max: 200 }))
test('unknown weight stays null', () => expect(requirementFor(item('ong_nhua'), 10, {}).weightKg).toBeNull())
test('every catalog item is marked as an assumption', () => expect(ITEMS.every(i => i.assumption === true)).toBe(true))
