import { ITEMS } from '../items/requirement'
import type { CheckState } from './check'

export function StepItem({ s, set }: { s: CheckState; set: (p: Partial<CheckState>) => void }) {
  return (
    <section>
      <h2>Loại hàng</h2>
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
