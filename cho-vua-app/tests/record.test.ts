import { expect, test } from 'vitest'
import { iv } from '../src/domain/interval'
import { loadRecords, saveRecord, toCsv, toRecord, updateTape, type CheckRecord } from '../src/record/log'
import { ticketText } from '../src/record/ticket'
import { runCheck } from '../src/ui/check'
import { state } from './helpers/fixtures'

const AT = new Date('2026-11-20T08:00:00Z')
const result = () => runCheck(state({ itemId: 'ong_nhua', measured: { l: iv(395, 400) } }))

function memStorage(): Storage {
  const m = new Map<string, string>()
  return {
    get length() { return m.size },
    clear: () => m.clear(),
    getItem: k => m.get(k) ?? null,
    key: i => [...m.keys()][i] ?? null,
    removeItem: k => { m.delete(k) },
    setItem: (k, v) => { m.set(k, v) },
  }
}

function rec(p: Partial<CheckRecord> = {}): CheckRecord {
  return { ...toRecord(state({}), runCheck(state({})), AT), ...p }
}

test('ticket has disclaimer', () => expect(ticketText(result(), AT)).toContain('không thay thế việc kiểm tra, xử lý của cơ quan chức năng'))
test('ticket lists red findings and the overall result', () => {
  const t = ticketText(result(), AT)
  expect(t).toContain('Không đạt')
  expect(t).toContain('Hàng lòi trước/sau')
})
test('csv header exact', () => expect(toCsv([]).split('\n')[0]).toBe('id,at,vehicle,item,ref_kind,overall,side_left_min,side_left_max,side_right_min,side_right_max,rear_min,rear_max,height_min,height_max,tape_side_left,tape_side_right,tape_rear,tape_height,note'))
test('save/load round-trip', () => { const s = memStorage(); saveRecord(rec(), s); expect(loadRecords(s)).toHaveLength(1) })
test('note with comma is quoted', () => expect(toCsv([rec({ note: 'a,b' })])).toContain('"a,b"'))
test('record keeps app measurements, not photos', () => {
  const s = state({ stage: 'loaded', photo: { refKind: 'plate', rear: { sideLeftCm: iv(40, 45), sideRightCm: iv(0, 2), heightCm: iv(120, 125) } } })
  const r = toRecord(s, runCheck(s), AT)
  expect(r.refKind).toBe('plate')
  expect(r.app.sideLeft).toEqual({ min: 40, max: 45 })
  expect(JSON.stringify(r)).not.toMatch(/data:image|blob:/)
})
test('tape values are stored and exported', () => {
  const s = memStorage()
  const r = rec()
  saveRecord(r, s)
  updateTape(r.id, { rear: 55 }, s)
  expect(toCsv(loadRecords(s)).split('\n')[1].split(',')[16]).toBe('55')
})
test('corrupt storage reads as empty', () => { const s = memStorage(); s.setItem('chovua.checks.v1', '{oops'); expect(loadRecords(s)).toEqual([]) })
