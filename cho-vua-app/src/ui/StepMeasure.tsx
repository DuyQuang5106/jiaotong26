import { useState } from 'react'
import { around, fmtM } from '../domain/interval'
import type { Interval } from '../domain/types'
import type { CheckState } from './check'
import { PhotoTapper } from './PhotoTapper'

const TAPE_HALF_CM = 1

function CmInput({ label, value, onChange }: { label: string; value: Interval | null | undefined; onChange: (v: Interval | undefined) => void }) {
  const shown = value ? String(Math.round((value.min + value.max) / 2)) : ''
  return (
    <label>{label}
      <input type="number" min={0} value={shown} onChange={e => { const t = e.target.value.trim(); onChange(t === '' ? undefined : around(Number(t), TAPE_HALF_CM)) }} />
    </label>
  )
}

export function StepMeasure({ s, set }: { s: CheckState; set: (p: Partial<CheckState>) => void }) {
  const [tab, setTab] = useState<'manual' | 'photo'>('manual')
  const nm = s.vehicle === 'non_motorized'
  const m = s.measured
  const ml = s.manualLoad
  return (
    <section>
      <h2>Kích thước</h2>
      <div className="choices">
        <button className={tab === 'manual' ? 'on' : ''} onClick={() => setTab('manual')}>Nhập tay</button>
        <button className={tab === 'photo' ? 'on' : ''} onClick={() => setTab('photo')}>Chụp ảnh</button>
      </div>

      {tab === 'manual' && (
        <>
          <p className="note">Kích thước cả lô hàng (cm) — để trống nếu chưa đo, app dùng kích thước điển hình (giả định) và không cho đèn xanh.</p>
          <CmInput label="Dài" value={m.l} onChange={v => set({ measured: { ...m, l: v } })} />
          <CmInput label="Rộng" value={m.w} onChange={v => set({ measured: { ...m, w: v } })} />
          <CmInput label="Cao" value={m.h} onChange={v => set({ measured: { ...m, h: v } })} />
          {s.stage === 'loaded' && (
            <>
              <p className="note">Hàng đã chất: đo phần lòi ra (cm) so với {nm ? 'mép bánh xe / thân xe' : 'mép giá chở hàng'}.</p>
              <CmInput label="Lòi bên trái" value={ml.sideLeftCm} onChange={v => set({ manualLoad: { ...ml, sideLeftCm: v ?? null } })} />
              <CmInput label="Lòi bên phải" value={ml.sideRightCm} onChange={v => set({ manualLoad: { ...ml, sideRightCm: v ?? null } })} />
              <CmInput label="Lòi phía sau" value={ml.rearCm} onChange={v => set({ manualLoad: { ...ml, rearCm: v ?? null } })} />
              {nm && <CmInput label="Lòi phía trước" value={ml.frontCm} onChange={v => set({ manualLoad: { ...ml, frontCm: v ?? null } })} />}
              {!nm && <CmInput label="Cao từ mặt đường" value={ml.heightCm} onChange={v => set({ manualLoad: { ...ml, heightCm: v ?? null } })} />}
            </>
          )}
        </>
      )}

      {tab === 'photo' && (
        <>
          <p className="note">Ảnh chỉ dùng để đo trên máy này, không được lưu hay gửi đi.</p>
          <PhotoTapper mode="rear" nonMotorized={nm} onDone={p => set({ stage: 'loaded', photo: { ...s.photo, ...p } })} />
          {s.photo.rear && <p>Đo được: trái {fmtM(s.photo.rear.sideLeftCm)}, phải {fmtM(s.photo.rear.sideRightCm)}, cao {fmtM(s.photo.rear.heightCm)}</p>}
          <PhotoTapper mode="side" nonMotorized={nm} onDone={p => set({ stage: 'loaded', photo: { ...s.photo, side: p.side, sideTapped: p.sideTapped, refKind: s.photo.refKind ?? p.refKind } })} />
          {s.photo.side && <p>Đo được: phía sau {fmtM(s.photo.side.rearCm)}</p>}
          {(s.photo.rear || s.photo.side) && <button onClick={() => set({ photo: {} })}>Xóa số đo ảnh</button>}
          <p className="note">Số đo bằng thước (tab Nhập tay) được ưu tiên hơn số đo ảnh.</p>
          {nm && <CmInput label="Lòi phía trước (nhập tay)" value={ml.frontCm} onChange={v => set({ manualLoad: { ...ml, frontCm: v ?? null } })} />}
        </>
      )}
    </section>
  )
}
