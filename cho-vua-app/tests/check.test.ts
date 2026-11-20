import { expect, test } from 'vitest'
import { iv } from '../src/domain/interval'
import { runCheck } from '../src/ui/check'
import { state } from './helpers/fixtures'

// ống 395–400 cm được làm tròn về 398–402 cm (chuẩn 400). Cận trên 402 > thùng 400 cm của Tải 2000kg → chọn Tải 2500kg (theo cận trên).
test('runCheck: 4 m pipe pre_load motorbike → red and Tải 2500kg', () => {
  const r = runCheck(state({ itemId: 'ong_nhua', measured: { l: iv(395, 400) } }))
  expect(r.overall).toBe('red')
  expect(r.options[0].vehicle.name).toBe('Xe tải 2500kg')
})

test('runCheck: loaded without measurement → E01–E03 yellow and still options', () => {
  const r = runCheck(state({ stage: 'loaded' }))
  expect(['E01', 'E02', 'E03'].map(c => r.findings.find(f => f.code === c)!.light)).toEqual(['yellow', 'yellow', 'yellow'])
  expect(r.options.length).toBeGreaterThan(0)
})

test('photo measurement wins over manual entry', () => {
  const r = runCheck(state({ stage: 'loaded', manualLoad: { sideLeftCm: iv(0, 1) }, photo: { refKind: 'plate', rear: { sideLeftCm: iv(40, 45), sideRightCm: iv(0, 2), heightCm: iv(120, 125) } } }))
  expect(r.findings.find(f => f.code === 'E01')!.light).toBe('red')
  expect(r.sizeSource).toBe('biển số')
})

test('manual loaded entry is used without a photo', () => {
  const r = runCheck(state({ stage: 'loaded', manualLoad: { sideLeftCm: iv(10, 12), sideRightCm: iv(10, 12), rearCm: iv(20, 22), heightCm: iv(120, 122) } }))
  expect(r.findings.find(f => f.code === 'E02')!.light).toBe('green')
  expect(r.sizeSource).toBe('nhập tay')
})

test('typical size is labelled as an assumption', () => expect(runCheck(state({})).sizeSource).toBe('kích thước điển hình (giả định)'))

test('cement bags trigger the loose-material check', () => expect(runCheck(state({ itemId: 'bao_xi_mang' })).findings.some(f => f.code === 'E10')).toBe(true))

test('manual weight overrides the catalog estimate', () => {
  const r = runCheck(state({ itemId: 'bao_xi_mang', qty: 4, weightKgManual: iv(210, 210), vehicleMaxKg: 150 }))
  expect(r.findings.find(f => f.code === 'E11')!.light).toBe('red')
})
