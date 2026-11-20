import { expect, test } from 'vitest'
import { iv } from '../src/domain/interval'
import { evaluateLoad } from '../src/rules/evaluate'
import { base, code } from './helpers/fixtures'

test('motorbike rear 330–390 cm is red E02', () => expect(code(evaluateLoad({ ...base(), rearCm: iv(330, 390) }), 'E02').light).toBe('red'))
test('motorbike height 240 red E03', () => expect(code(evaluateLoad({ ...base(), heightCm: iv(235, 245) }), 'E03').light).toBe('red'))
test('non_motorized has no E03', () => expect(evaluateLoad({ ...base(), vehicle: 'non_motorized', heightCm: iv(300, 310) }).findings.find(f => f.code === 'E03')).toBeUndefined())
test('non_motorized side 45 red at 40 limit', () => expect(code(evaluateLoad({ ...base(), vehicle: 'non_motorized', sideLeftCm: iv(45, 48) }), 'E01').light).toBe('red'))
test('non_motorized 1/3 rule: body 210 → limit 70', () => expect(code(evaluateLoad({ ...base(), vehicle: 'non_motorized', bodyLengthCm: 210, rearCm: iv(75, 80) }), 'E02').light).toBe('red'))
test('non_motorized unknown body downgrades green', () => expect(code(evaluateLoad({ ...base(), vehicle: 'non_motorized', bodyLengthCm: null, rearCm: iv(10, 20) }), 'E02').light).toBe('yellow'))
test('carrying bulky caps at yellow', () => expect(code(evaluateLoad({ ...base(), carryingBulky: true }), 'E07').light).toBe('yellow'))
test('unregistered 3-4 wheel is red E09', () => expect(code(evaluateLoad({ ...base(), vehicle: 'motor_3_4_wheel', registered: false }), 'E09').light).toBe('red'))
test('overhang without red marker is red E05', () => expect(code(evaluateLoad({ ...base(), extendsBeyondVehicle: true, redMarker: false }), 'E05').light).toBe('red'))
test('overall is worst', () => expect(evaluateLoad({ ...base(), heightCm: iv(235, 245) }).overall).toBe('red'))
test('all good is green', () => expect(evaluateLoad(base()).overall).toBe('green'))
test('fine text for E07 motorbike', () => expect(code(evaluateLoad({ ...base(), carryingBulky: true }), 'E07').fine).toContain('600.000–800.000đ'))
test('motorbike rear exactly 50 is green', () => expect(code(evaluateLoad({ ...base(), rearCm: iv(45, 50) }), 'E02').light).toBe('green'))
test('E09 not reported for motorbike', () => expect(evaluateLoad(base()).findings.find(f => f.code === 'E09')).toBeUndefined())
test('E10 only when loose material', () => {
  expect(evaluateLoad(base()).findings.find(f => f.code === 'E10')).toBeUndefined()
  expect(code(evaluateLoad({ ...base(), looseMaterial: true, looseCovered: false }), 'E10').light).toBe('red')
})
test('E11 unknown weight is yellow', () => expect(code(evaluateLoad({ ...base(), weightKg: null }), 'E11').light).toBe('yellow'))
test('non_motorized front overhang counts for E02', () => expect(code(evaluateLoad({ ...base(), vehicle: 'non_motorized', bodyLengthCm: 300, frontCm: iv(110, 120) }), 'E02').light).toBe('red'))
