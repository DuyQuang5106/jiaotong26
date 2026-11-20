import { expect, test } from 'vitest'
import { iv } from '../src/domain/interval'
import { estimatePrice, matchVehicles, VEHICLES as V } from '../src/services/match'
import { pipe } from './helpers/fixtures'

test('aha 5 km = 158800', () => expect(estimatePrice({ baseVnd: 124000, baseKm: 2, perKmVnd: 11600 }, 5)).toBe(158800))
test('price within base distance is base', () => expect(estimatePrice({ baseVnd: 124000, baseKm: 2, perKmVnd: 11600 }, 1.5)).toBe(124000))
test('pipe 390–400 cm in HCM → Lalamove Tải 2000kg first', () => expect(matchVehicles(pipe(390, 400), V, 'HCM', 5)[0].vehicle.name).toBe('Xe tải 2000kg'))
test('pipe up to 420 cm → Tải 2500kg first', () => expect(matchVehicles(pipe(380, 420), V, 'HCM', 5)[0].vehicle.name).toBe('Xe tải 2500kg'))
test('pipe 400 cm in HN → none', () => expect(matchVehicles(pipe(390, 400), V, 'HN', 5)).toEqual([]))
test('rotation: 140×60 fits bán tải 140×150', () => expect(matchVehicles({ lengthCm: iv(55, 60), widthCm: iv(135, 140), heightCm: iv(40, 45), weightKg: null }, V, 'HCM', 3).map(o => o.vehicle.name)).toContain('Xe bán tải'))
test('null weight flagged', () => expect(matchVehicles(pipe(390, 400), V, 'HCM', 5)[0].weightUnchecked).toBe(true))
test('weight above capacity excludes vehicle', () => {
  const opts = matchVehicles({ lengthCm: iv(50, 55), widthCm: iv(40, 45), heightCm: iv(40, 45), weightKg: iv(600, 650) }, V, 'HCM', 3, 20)
  expect(opts.every(o => o.vehicle.maxKg === null || o.vehicle.maxKg >= 650)).toBe(true)
  expect(opts.map(o => o.vehicle.name)).not.toContain('Xe van 500kg')
})
test('ahamove van gets a price estimate', () => {
  const o = matchVehicles({ lengthCm: iv(150, 160), widthCm: iv(100, 110), heightCm: iv(90, 100), weightKg: null }, V, 'HCM', 5, 20).find(x => x.vehicle.provider === 'ahamove')
  expect(o?.estimateVnd).toBe(158800)
})
test('default limit is 3', () => expect(matchVehicles({ lengthCm: iv(10, 20), widthCm: iv(10, 20), heightCm: iv(10, 20), weightKg: null }, V, 'HCM', 3)).toHaveLength(3))
