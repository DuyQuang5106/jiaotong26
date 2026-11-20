import { useMemo, useState } from 'react'
import { saveRecord, toRecord } from '../record/log'
import { ticketText } from '../record/ticket'
import { runCheck, type CheckState } from './check'
import { FieldMode } from './FieldMode'
import { Ticket } from './Ticket'
import { Result } from './Result'
import { StepChecklist } from './StepChecklist'
import { StepItem } from './StepItem'
import { StepMeasure } from './StepMeasure'
import { StepVehicle } from './StepVehicle'

export type Step = 'vehicle' | 'item' | 'measure' | 'checklist' | 'result'
const ORDER: Step[] = ['vehicle', 'item', 'measure', 'checklist', 'result']

export const INITIAL: CheckState = {
  stage: 'pre_load', vehicle: 'motorbike', city: 'HCM', km: 5,
  itemId: 'thung_carton', qty: 1, measured: {}, manualLoad: {}, photo: {},
  answers: { plateAndLightsVisible: null, redMarker: null, lashingOk: null, carryingBulky: null, towing: null, looseCovered: null, registered: null, bodyLengthCm: null },
  weightKgManual: null, vehicleMaxKg: null,
}

export default function App({ initial = INITIAL, startAt = 'vehicle' }: { initial?: CheckState; startAt?: Step }) {
  const [s, setS] = useState<CheckState>(initial)
  const [step, setStep] = useState<Step>(startAt)
  const [overlay, setOverlay] = useState<{ kind: 'ticket'; text: string } | { kind: 'field' } | null>(null)
  const set = (p: Partial<CheckState>) => setS(prev => ({ ...prev, ...p }))
  const result = useMemo(() => runCheck(s), [s])
  const i = ORDER.indexOf(step)

  function openTicket() {
    const now = new Date()
    saveRecord(toRecord(s, result, now))
    setOverlay({ kind: 'ticket', text: ticketText(result, now) })
  }

  if (overlay?.kind === 'ticket') return <main className="app"><Ticket text={overlay.text} onClose={() => setOverlay(null)} /><nav className="nav"><button onClick={() => setOverlay({ kind: 'field' })}>Thực địa</button></nav></main>
  if (overlay?.kind === 'field') return <main className="app"><FieldMode onClose={() => setOverlay(null)} /></main>

  return (
    <main className="app">
      <header className="top">
        <div>
          <h1>CHỞ VỪA</h1>
          <p className="note">Kiểm tra xe – hàng trước khi lăn bánh</p>
        </div>
        <button onClick={() => setOverlay({ kind: 'field' })}>Thực địa</button>
      </header>
      {step === 'vehicle' && <StepVehicle s={s} set={set} />}
      {step === 'item' && <StepItem s={s} set={set} />}
      {step === 'measure' && <StepMeasure s={s} set={set} />}
      {step === 'checklist' && <StepChecklist s={s} set={set} />}
      {step === 'result' && <Result r={result} city={s.city} onMeasureMore={() => setStep('measure')} onTicket={openTicket} />}
      <nav className="nav">
        {i > 0 && <button onClick={() => setStep(ORDER[i - 1])}>Quay lại</button>}
        {i < ORDER.length - 1 && <button className="primary" onClick={() => setStep(ORDER[i + 1])}>{i === ORDER.length - 2 ? 'Xem kết quả' : 'Tiếp'}</button>}
        {step === 'result' && <button onClick={() => { setS(INITIAL); setStep('vehicle') }}>Kiểm chuyến mới</button>}
      </nav>
    </main>
  )
}
