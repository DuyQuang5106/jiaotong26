import { useEffect, useRef, useState } from 'react'
import { CARD_SIZE_CM, detectMarker } from '../measure/aruco'
import type { Pt, Quad } from '../measure/homography'
import { MeasureError, measureRear, measureSide, PLATE_SIZE_CM, type Reference } from '../measure/measure'
import type { CheckState } from './check'

type Mode = 'rear' | 'side'
type Photo = CheckState['photo']

const CORNERS = ['góc trên trái', 'góc trên phải', 'góc dưới phải', 'góc dưới trái']
function tapLabels(mode: Mode, nonMotorized: boolean): string[] {
  const edge = nonMotorized ? 'mép bánh xe' : 'mép giá chở hàng'
  return mode === 'rear'
    ? [`${edge} bên trái`, `${edge} bên phải`, 'điểm ngoài cùng bên trái của hàng', 'điểm ngoài cùng bên phải của hàng', 'điểm cao nhất của hàng', 'mặt đất ngay dưới xe']
    : [nonMotorized ? 'mép sau thân xe' : 'mép sau giá chở hàng', 'điểm xa nhất phía sau của hàng']
}

const MAX_SIDE = 1600

/** Pick a photo, find the reference (card automatically, or 4 tapped corners), then tap the measuring points. */
export function PhotoTapper({ mode, nonMotorized, onDone }: { mode: Mode; nonMotorized: boolean; onDone: (p: Photo) => void }) {
  const canvas = useRef<HTMLCanvasElement>(null)
  const [img, setImg] = useState<HTMLImageElement | null>(null)
  const [ref, setRef] = useState<Reference | null>(null)
  const [corners, setCorners] = useState<Pt[]>([])
  const [taps, setTaps] = useState<Pt[]>([])
  const [msg, setMsg] = useState('')

  const manualKind: Reference['kind'] = mode === 'rear' ? 'plate' : 'aruco'
  const manualName = manualKind === 'plate' ? 'biển số' : 'thẻ chuẩn'
  const labels = tapLabels(mode, nonMotorized)
  const step = !ref ? `Chạm ${CORNERS[corners.length]} của ${manualName}` : taps.length < labels.length ? `Chạm ${labels[taps.length]}` : 'Đã đo xong'

  useEffect(() => {
    const c = canvas.current
    if (!c || !img) return
    const k = Math.min(1, MAX_SIDE / Math.max(img.naturalWidth, img.naturalHeight))
    c.width = Math.round(img.naturalWidth * k)
    c.height = Math.round(img.naturalHeight * k)
    const g = c.getContext('2d')!
    g.drawImage(img, 0, 0, c.width, c.height)
    const dot = (p: Pt, color: string) => { g.fillStyle = color; g.beginPath(); g.arc(p.x, p.y, Math.max(4, c.width / 200), 0, Math.PI * 2); g.fill() }
    ref?.cornersPx.forEach(p => dot(p, '#0a84ff'))
    corners.forEach(p => dot(p, '#0a84ff'))
    taps.forEach(p => dot(p, '#ff3b30'))
  }, [img, ref, corners, taps])

  function onFile(f: File | undefined) {
    if (!f) return
    const url = URL.createObjectURL(f)
    const el = new Image()
    el.onload = () => {
      setImg(el); setCorners([]); setTaps([]); setMsg('')
      const c = document.createElement('canvas')
      const k = Math.min(1, MAX_SIDE / Math.max(el.naturalWidth, el.naturalHeight))
      c.width = Math.round(el.naturalWidth * k); c.height = Math.round(el.naturalHeight * k)
      const g = c.getContext('2d')!
      g.drawImage(el, 0, 0, c.width, c.height)
      let found: Reference | null = null
      try { found = detectMarker(g.getImageData(0, 0, c.width, c.height)) } catch { found = null }
      setRef(found)
      setMsg(found ? 'Đã tìm thấy thẻ chuẩn.' : `Không thấy thẻ chuẩn — chạm 4 góc ${manualName}.`)
      URL.revokeObjectURL(url)
    }
    el.src = url
  }

  function finish(reference: Reference, points: Pt[]) {
    try {
      const out: Photo = { refKind: reference.kind }
      if (mode === 'rear') {
        const [rackLeft, rackRight, cargoLeft, cargoRight, cargoTop, ground] = points
        out.rear = measureRear(reference, { rackLeft, rackRight, cargoLeft, cargoRight, cargoTop, ground })
      } else {
        const [rackRearEnd, cargoRearEnd] = points
        out.side = measureSide(reference, { rackRearEnd, cargoRearEnd })
      }
      onDone(out)
      setMsg('Đã đo xong.')
    } catch (e) {
      if (e instanceof MeasureError && e.reason === 'degenerate_reference') {
        setMsg(`Không đo được từ 4 góc này — chạm lại 4 góc ${manualName}.`)
        setRef(null); setCorners([]); setTaps([])
      } else setMsg('Chưa đủ điểm chạm.')
    }
  }

  function onTap(e: React.MouseEvent<HTMLCanvasElement>) {
    const c = canvas.current!
    const r = c.getBoundingClientRect()
    const p = { x: ((e.clientX - r.left) * c.width) / r.width, y: ((e.clientY - r.top) * c.height) / r.height }
    if (!ref) {
      const next = [...corners, p]
      if (next.length < 4) { setCorners(next); return }
      const size = manualKind === 'plate' ? PLATE_SIZE_CM : { w: CARD_SIZE_CM, h: CARD_SIZE_CM }
      setRef({ kind: manualKind, cornersPx: next as Quad, sizeCm: { ...size } })
      setCorners([])
      return
    }
    if (taps.length >= labels.length) return
    const next = [...taps, p]
    setTaps(next)
    if (next.length === labels.length) finish(ref, next)
  }

  return (
    <div className="tapper">
      <label className="btn">{mode === 'rear' ? 'Chụp phía sau xe' : 'Chụp bên hông xe'}
        <input type="file" accept="image/*" capture="environment" hidden onChange={e => onFile(e.target.files?.[0])} />
      </label>
      {img && (
        <>
          <p className="step">{step}</p>
          <canvas ref={canvas} onClick={onTap} className="photo" />
          <button onClick={() => { setTaps([]); setCorners([]); if (ref && ref.kind !== 'aruco') setRef(null) }}>Chạm lại</button>
        </>
      )}
      {msg && <p className="note">{msg}</p>}
    </div>
  )
}
