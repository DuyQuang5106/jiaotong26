import type { CheckResult } from './check'
import { LightDot } from './Light'

const PROVIDER: Record<string, string> = { lalamove: 'Lalamove', ahamove: 'Ahamove', grab: 'Grab' }
const vnd = (n: number) => `${n.toLocaleString('vi-VN')}đ`

export function Result({ r, city, onMeasureMore, onTicket }: { r: CheckResult; city: string; onMeasureMore: () => void; onTicket?: () => void }) {
  const order = { red: 0, yellow: 1, green: 2 } as const
  const sorted = [...r.findings].sort((a, b) => order[a.light] - order[b.light])
  return (
    <section className="result">
      <div className={`banner banner-${r.overall}`}>
        <LightDot light={r.overall} />
        <strong>{r.overall === 'green' ? 'Đạt' : r.overall === 'red' ? 'Không đạt' : 'Cần kiểm thêm'}</strong>
      </div>

      <h2>Loại hàng</h2>
      <p>{r.item.name} <span className="note">(danh mục mẫu, giả định)</span></p>

      <h2>Kích cỡ ước tính</h2>
      <p>{r.sizeText}</p>
      <p className="note">Nguồn: {r.sizeSource}{r.rackAssumed ? '; phần lòi tính theo giá chở hàng giả định (rộng 0,30–0,50 m, cao 0,70–0,90 m)' : ''}.</p>
      <button onClick={onMeasureMore}>Đo kỹ hơn</button>

      <h2>Luật áp dụng</h2>
      <ul className="findings">
        {sorted.map(f => (
          <li key={f.code}>
            <LightDot light={f.light} />
            <div>
              <strong>{f.title}</strong>
              <div>{f.detail}</div>
              <div className="note">{f.legalBasis} · Phạt: {f.fine}</div>
            </div>
          </li>
        ))}
      </ul>

      <h2>Xe phù hợp</h2>
      {r.options.length === 0 ? (
        <p>Không có xe phù hợp trong bảng cho {city}.</p>
      ) : (
        <ul className="options">
          {r.options.map(o => (
            <li key={o.vehicle.id}>
              <div>
                <strong>{o.vehicle.name}</strong> · {PROVIDER[o.vehicle.provider]}
                <div className="note">Thùng {o.vehicle.bedCm.l}×{o.vehicle.bedCm.w}×{o.vehicle.bedCm.h} cm{o.vehicle.maxKg ? `, tải ${o.vehicle.maxKg} kg` : ''}{o.vehicle.note ? ` — ${o.vehicle.note}` : ''}</div>
                <div>{o.estimateVnd !== null ? `Khoảng ${vnd(o.estimateVnd)} (giá công bố, chưa gồm phụ phí)` : 'Xem giá trên app'}</div>
                {o.weightUnchecked && <div className="note">Chưa kiểm được khối lượng.</div>}
              </div>
              <a className="btn" href={o.vehicle.bookingUrl} target="_blank" rel="noreferrer">Mở {PROVIDER[o.vehicle.provider]}</a>
            </li>
          ))}
        </ul>
      )}
      {onTicket && <button onClick={onTicket}>Phiếu kết quả</button>}
      <p className="note">Kết quả kiểm tra kích thước và cách xếp hàng, không thay thế việc kiểm tra, xử lý của cơ quan chức năng.</p>
    </section>
  )
}
