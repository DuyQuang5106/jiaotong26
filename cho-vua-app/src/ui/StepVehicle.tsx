import type { VehicleKind } from '../domain/types'
import type { City } from '../services/match'
import type { CheckState } from './check'

const VEHICLES: { id: VehicleKind; label: string }[] = [
  { id: 'motorbike', label: 'Xe máy' },
  { id: 'non_motorized', label: 'Xe thô sơ (xe đạp, ba gác đạp/đẩy)' },
  { id: 'motor_3_4_wheel', label: 'Xe ba, bốn bánh có gắn máy' },
]

export function StepVehicle({ s, set }: { s: CheckState; set: (p: Partial<CheckState>) => void }) {
  return (
    <section>
      <h2>Tình huống</h2>
      <div className="choices">
        <button className={s.stage === 'pre_load' ? 'on' : ''} onClick={() => set({ stage: 'pre_load' })}>Lúc bán — chưa chất hàng</button>
        <button className={s.stage === 'loaded' ? 'on' : ''} onClick={() => set({ stage: 'loaded' })}>Xe đã chất hàng</button>
      </div>
      <h2>Loại xe định chở</h2>
      <div className="choices">
        {VEHICLES.map(v => (
          <button key={v.id} className={s.vehicle === v.id ? 'on' : ''} onClick={() => set({ vehicle: v.id })}>{v.label}</button>
        ))}
      </div>
      <h2>Khu vực</h2>
      <div className="row">
        <select aria-label="Thành phố" value={s.city} onChange={e => set({ city: e.target.value as City })}>
          <option value="HCM">TP.HCM</option>
          <option value="HN">Hà Nội</option>
        </select>
        <label>Quãng đường (km)
          <input type="number" min={0.5} step={0.5} value={s.km} onChange={e => set({ km: Number(e.target.value) || 0 })} />
        </label>
      </div>
    </section>
  )
}
