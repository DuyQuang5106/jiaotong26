import { useState } from 'react'
import { fmtM } from '../domain/interval'
import { loadRecords, toCsv, updateTape, type CheckRecord } from '../record/log'

const DIMS: { k: keyof NonNullable<CheckRecord['tape']>; label: string }[] = [
  { k: 'sideLeft', label: 'Lòi trái' },
  { k: 'sideRight', label: 'Lòi phải' },
  { k: 'rear', label: 'Lòi sau' },
  { k: 'height', label: 'Cao' },
]

function download(name: string, text: string) {
  const url = URL.createObjectURL(new Blob(['﻿' + text], { type: 'text/csv;charset=utf-8' }))
  const a = document.createElement('a')
  a.href = url; a.download = name; a.click()
  URL.revokeObjectURL(url)
}

/** Field mode: add tape-measure values to each saved check and export CSV for evaluation. */
export function FieldMode({ onClose }: { onClose: () => void }) {
  const [recs, setRecs] = useState<CheckRecord[]>(() => loadRecords())
  const set = (id: string, tape: CheckRecord['tape'], note?: string) => { updateTape(id, tape, undefined, note); setRecs(loadRecords()) }
  return (
    <section>
      <h2>Chế độ thực địa</h2>
      <p className="note">Nhập số đo bằng thước (cm) cho từng lần kiểm. Dữ liệu chỉ nằm trên máy này; không lưu ảnh.</p>
      {recs.length === 0 && <p>Chưa có lần kiểm nào. Bấm "Phiếu kết quả" ở màn hình kết quả để lưu.</p>}
      {recs.map(r => (
        <div key={r.id} className="record">
          <strong>{new Date(r.at).toLocaleString('vi-VN')}</strong> · {r.itemId} · {r.refKind}
          {DIMS.map(d => (
            <label key={d.k}>{d.label}{r.app[d.k] ? ` (app ${fmtM(r.app[d.k]!)})` : ''}
              <input type="number" min={0} value={r.tape?.[d.k] ?? ''} onChange={e => set(r.id, { [d.k]: e.target.value === '' ? undefined : Number(e.target.value) })} />
            </label>
          ))}
          <label>Ghi chú
            <input value={r.note ?? ''} onChange={e => set(r.id, {}, e.target.value)} />
          </label>
        </div>
      ))}
      <div className="choices">
        <button className="primary" disabled={recs.length === 0} onClick={() => download('chovua_checks.csv', toCsv(recs))}>Xuất CSV</button>
        <button onClick={onClose}>Đóng</button>
      </div>
    </section>
  )
}
