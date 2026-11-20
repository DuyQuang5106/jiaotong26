import { useState } from 'react'
import { ITEMS } from '../items/requirement'
import { classifyImage, type ClassifyResult } from '../recognize/classify'
import type { CheckState } from './check'
import { itemById } from './check'

const CONF = { high: 'cao', medium: 'vừa', low: 'thấp' } as const

/**
 * Apply a recognition result: the item, plus only what makes the check stricter.
 * The model's vehicle guess never replaces the user's choice (a self-made look adds the
 * registration question), and only warnings are pre-filled — never reassurances.
 */
export function applySuggestion(s: CheckState, r: ClassifyResult): Partial<CheckState> {
  const a = s.answers
  return {
    itemId: r.itemId,
    ...(r.looksSelfMade ? { vehicle: 'motor_3_4_wheel' as const } : {}),
    answers: {
      ...a,
      plateAndLightsVisible: a.plateAndLightsVisible ?? (r.plateAndLightsVisible === false ? false : null),
      carryingBulky: a.carryingBulky ?? (r.carryingBulky === true ? true : null),
    },
  }
}

const VEHICLE_NAME = { motorbike: 'xe máy', non_motorized: 'xe thô sơ', motor_3_4_wheel: 'xe ba, bốn bánh có gắn máy' } as const

export function StepItem({ s, set, classify = classifyImage }: { s: CheckState; set: (p: Partial<CheckState>) => void; classify?: typeof classifyImage }) {
  const [busy, setBusy] = useState(false)
  const [sug, setSug] = useState<ClassifyResult | null>(null)
  const [msg, setMsg] = useState('')

  async function onFile(f: File | undefined) {
    if (!f) return
    setBusy(true); setMsg(''); setSug(null)
    const r = await classify(f)
    setBusy(false)
    if (!r) { setMsg('Không nhận diện được — chọn loại hàng bên dưới.'); return }
    setSug(r)
  }

  return (
    <section>
      <h2>Loại hàng</h2>
      <label className="btn">{busy ? 'Đang nhận diện…' : 'Chụp ảnh để nhận diện'}
        <input type="file" accept="image/*" capture="environment" hidden disabled={busy} onChange={e => onFile(e.target.files?.[0])} />
      </label>
      <p className="note">Ảnh này được gửi tới máy chủ nhận diện (dịch vụ AI bên ngoài) để đoán loại hàng; không được lưu lại.</p>
      {msg && <p className="note">{msg}</p>}
      {sug && (
        <div className="suggest">
          <p>Gợi ý: <strong>{itemById(sug.itemId).name}</strong> (độ tin cậy {CONF[sug.confidence]})</p>
          {sug.vehicle && sug.vehicle !== s.vehicle && <p className="note">Ảnh có vẻ là {VEHICLE_NAME[sug.vehicle]} — đổi loại xe ở bước 1 nếu đúng.</p>}
          {sug.looksSelfMade && <p className="note">Xe trông như xe tự chế — sẽ chuyển sang "xe ba, bốn bánh có gắn máy" và hỏi xe có đăng ký, biển số không.</p>}
          <div className="choices">
            <button className="primary" onClick={() => { set(applySuggestion(s, sug)); setSug(null) }}>Dùng gợi ý</button>
            {sug.alternatives.map(id => (
              <button key={id} onClick={() => { set(applySuggestion(s, { ...sug, itemId: id })); setSug(null) }}>{itemById(id).name}</button>
            ))}
          </div>
        </div>
      )}
      <p className="note">Danh mục mẫu (giả định) — thay bằng danh mục của cửa hàng thí điểm.</p>
      <div className="choices">
        {ITEMS.map(i => (
          <button key={i.id} className={s.itemId === i.id ? 'on' : ''} onClick={() => set({ itemId: i.id })}>{i.name}</button>
        ))}
      </div>
      <label>Số lượng
        <input type="number" min={1} value={s.qty} onChange={e => set({ qty: Math.max(1, Number(e.target.value) || 1) })} />
      </label>
    </section>
  )
}
