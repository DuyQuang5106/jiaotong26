import { iv } from '../domain/interval'
import type { CheckState } from './check'
import { itemById } from './check'

type Key = keyof CheckState['answers']

function YesNo({ label, value, onChange }: { label: string; value: boolean | null; onChange: (v: boolean | null) => void }) {
  return (
    <div className="yesno">
      <span>{label}</span>
      <div className="choices">
        <button className={value === true ? 'on' : ''} onClick={() => onChange(true)}>Có</button>
        <button className={value === false ? 'on' : ''} onClick={() => onChange(false)}>Không</button>
        <button className={value === null ? 'on' : ''} onClick={() => onChange(null)}>Không rõ</button>
      </div>
    </div>
  )
}

export function StepChecklist({ s, set }: { s: CheckState; set: (p: Partial<CheckState>) => void }) {
  const a = s.answers
  const setA = (k: Key, v: boolean | number | null) => set({ answers: { ...a, [k]: v } })
  const item = itemById(s.itemId)
  const num = (v: string) => (v.trim() === '' ? null : Number(v))
  return (
    <section>
      <h2>Kiểm nhanh</h2>
      <YesNo label="Biển số và đèn có nhìn thấy rõ không?" value={a.plateAndLightsVisible} onChange={v => setA('plateAndLightsVisible', v)} />
      <YesNo label="Hàng lòi trước/sau đã gắn báo hiệu đỏ chưa?" value={a.redMarker} onChange={v => setA('redMarker', v)} />
      <YesNo label="Hàng đã chằng buộc chắc chắn chưa?" value={a.lashingOk} onChange={v => setA('lashingOk', v)} />
      <YesNo label="Người lái hoặc người ngồi sau có ôm, vác hàng không?" value={a.carryingBulky} onChange={v => setA('carryingBulky', v)} />
      <YesNo label="Xe có kéo theo xe hoặc vật khác không?" value={a.towing} onChange={v => setA('towing', v)} />
      {item.looseMaterial && <YesNo label="Hàng rời đã đóng bao hoặc che phủ chưa?" value={a.looseCovered} onChange={v => setA('looseCovered', v)} />}
      {s.vehicle === 'motor_3_4_wheel' && <YesNo label="Xe có đăng ký và biển số không?" value={a.registered} onChange={v => setA('registered', v)} />}
      {s.vehicle === 'non_motorized' && (
        <label>Chiều dài thân xe (cm)
          <input type="number" value={a.bodyLengthCm ?? ''} onChange={e => setA('bodyLengthCm', num(e.target.value))} />
        </label>
      )}
      <label>Khối lượng hàng (kg), nếu biết
        <input type="number" value={s.weightKgManual?.max ?? ''} onChange={e => { const v = num(e.target.value); set({ weightKgManual: v === null ? null : iv(v, v) }) }} />
      </label>
      <label>Tải cho phép của xe (kg), nếu biết
        <input type="number" value={s.vehicleMaxKg ?? ''} onChange={e => set({ vehicleMaxKg: num(e.target.value) })} />
      </label>
    </section>
  )
}
