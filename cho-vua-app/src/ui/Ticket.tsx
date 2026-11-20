import QRCode from 'qrcode'
import { useEffect, useState } from 'react'

export function Ticket({ text, onClose }: { text: string; onClose: () => void }) {
  const [src, setSrc] = useState('')
  useEffect(() => {
    QRCode.toDataURL(text, { errorCorrectionLevel: 'M', margin: 1, width: 280 }).then(setSrc).catch(() => setSrc(''))
  }, [text])
  return (
    <section className="ticket">
      <h2>Phiếu kết quả</h2>
      {src ? <img src={src} alt="Mã QR phiếu kết quả" width={280} height={280} /> : <p className="note">Không tạo được mã QR.</p>}
      <pre>{text}</pre>
      <div className="choices">
        <button onClick={() => window.print()}>In phiếu</button>
        <button onClick={onClose}>Đóng</button>
      </div>
    </section>
  )
}
