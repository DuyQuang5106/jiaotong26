import { expect, test } from 'vitest'
import { iv } from '../src/domain/interval'
import { runCheck } from '../src/ui/check'
import { state } from './helpers/fixtures'

// Typed 400 cm becomes 399–401 cm (±1 cm). Upper bound 401 > the 400 cm bed of Tải 2000kg → Tải 2500kg.
test('runCheck: 4 m pipe pre_load motorbike → red and Tải 2500kg', () => {
  const r = runCheck(state({ itemId: 'ong_nhua', measured: { l: iv(399, 401) } }))
  expect(r.overall).toBe('red')
  expect(r.options[0].vehicle.name).toBe('Xe tải 2500kg')
})

test('runCheck: loaded without measurement → E01–E03 yellow and still options', () => {
  const r = runCheck(state({ stage: 'loaded' }))
  expect(['E01', 'E02', 'E03'].map(c => r.findings.find(f => f.code === c)!.light)).toEqual(['yellow', 'yellow', 'yellow'])
  expect(r.options.length).toBeGreaterThan(0)
})

test('photo measurement is used when nothing was taped', () => {
  const r = runCheck(state({ stage: 'loaded', photo: { refKind: 'plate', rearTapped: true, rear: { sideLeftCm: iv(40, 45), sideRightCm: iv(0, 2), heightCm: iv(120, 125) } } }))
  expect(r.findings.find(f => f.code === 'E01')!.light).toBe('red')
  expect(r.sizeSource).toBe('biển số')
})

test('a tape value wins over the photo for that dimension', () => {
  const r = runCheck(state({ stage: 'loaded', manualLoad: { sideLeftCm: iv(44, 46) }, photo: { refKind: 'aruco', rearTapped: false, rear: { sideLeftCm: iv(0, 2), sideRightCm: iv(0, 2), heightCm: iv(120, 125) } } }))
  expect(r.findings.find(f => f.code === 'E01')!.light).toBe('red')
})

test('hand-tapped reference cannot give green on E01–E03', () => {
  const r = runCheck(state({ stage: 'loaded', manualLoad: { rearCm: iv(10, 12) }, photo: { refKind: 'plate', rearTapped: true, rear: { sideLeftCm: iv(0, 2), sideRightCm: iv(0, 2), heightCm: iv(120, 125) } } }))
  expect(r.findings.find(f => f.code === 'E01')!.light).toBe('yellow')
  expect(r.findings.find(f => f.code === 'E03')!.light).toBe('yellow')
  expect(r.findings.find(f => f.code === 'E02')!.light).toBe('green') // taped, not capped
})

test('detected card may give green', () => {
  const r = runCheck(state({ stage: 'loaded', manualLoad: { rearCm: iv(10, 12) }, photo: { refKind: 'aruco', rearTapped: false, rear: { sideLeftCm: iv(0, 2), sideRightCm: iv(0, 2), heightCm: iv(120, 125) } } }))
  expect(r.findings.find(f => f.code === 'E01')!.light).toBe('green')
})

test('pre-load with typical sizes is never green on E01–E03', () => {
  const r = runCheck(state({ qty: 20 }))
  expect(['E01', 'E02', 'E03'].map(c => r.findings.find(f => f.code === c)!.light)).toEqual(['yellow', 'yellow', 'yellow'])
  expect(r.overall).not.toBe('green')
})

test('pre-load with measured load sizes can be green', () => {
  const r = runCheck(state({ measured: { l: iv(39, 41), w: iv(29, 31), h: iv(29, 31) } }))
  expect(r.findings.find(f => f.code === 'E01')!.light).toBe('green')
})

test('uncertain rear overhang keeps the red-marker check (E05 yellow)', () => {
  const s = state({ stage: 'loaded', manualLoad: { rearCm: iv(0, 45) } })
  const r = runCheck({ ...s, answers: { ...s.answers, redMarker: false } })
  expect(r.findings.find(f => f.code === 'E05')?.light).toBe('yellow')
})

test('a taped 430 cm pipe is not shrunk to 4 m', () => {
  const r = runCheck(state({ itemId: 'ong_nhua', measured: { l: iv(429, 431) } }))
  expect(r.options[0].vehicle.bedCm.l).toBeGreaterThanOrEqual(431)
})

test('manual loaded entry is used without a photo', () => {
  const r = runCheck(state({ stage: 'loaded', manualLoad: { sideLeftCm: iv(10, 12), sideRightCm: iv(10, 12), rearCm: iv(20, 22), heightCm: iv(120, 122) } }))
  expect(r.findings.find(f => f.code === 'E02')!.light).toBe('green')
  expect(r.sizeSource).toBe('nhập tay')
})

// Demo script scenes (DEMO_vi.md) that need no photo.
// Typical fridge 1,2–1,8 m + rack 0,7–0,9 m straddles 2 m (yellow); the demo enters the measured 1,6 m.
test('demo 3: standing fridge (1,6 m) on a motorbike is red E03', () => expect(runCheck(state({ itemId: 'tu_lanh', measured: { h: iv(159, 161) } })).findings.find(f => f.code === 'E03')!.light).toBe('red'))
test('demo 3b: unmeasured fridge is only yellow E03', () => expect(runCheck(state({ itemId: 'tu_lanh' })).findings.find(f => f.code === 'E03')!.light).toBe('yellow'))
test('demo 4: goods covering the plate is red E04', () => {
  const s = state({})
  expect(runCheck({ ...s, answers: { ...s.answers, plateAndLightsVisible: false } }).findings.find(f => f.code === 'E04')!.light).toBe('red')
})
test('demo 5: unregistered 3–4 wheel motor cart is red E09 and still gets vehicle options', () => {
  const s = state({ vehicle: 'motor_3_4_wheel' })
  const r = runCheck({ ...s, answers: { ...s.answers, registered: false } })
  expect(r.findings.find(f => f.code === 'E09')!.light).toBe('red')
  expect(r.options.length).toBeGreaterThan(0)
})

test('typical size is labelled as an assumption', () => expect(runCheck(state({})).sizeSource).toBe('kích thước điển hình (giả định)'))

test('cement bags trigger the loose-material check', () => expect(runCheck(state({ itemId: 'bao_xi_mang' })).findings.some(f => f.code === 'E10')).toBe(true))

test('manual weight overrides the catalog estimate', () => {
  const r = runCheck(state({ itemId: 'bao_xi_mang', qty: 4, weightKgManual: iv(210, 210), vehicleMaxKg: 150 }))
  expect(r.findings.find(f => f.code === 'E11')!.light).toBe('red')
})
