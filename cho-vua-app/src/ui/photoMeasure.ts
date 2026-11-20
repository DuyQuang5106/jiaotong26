import { CARD_SIZE_CM } from '../measure/aruco'
import { orderQuad, type Pt } from '../measure/homography'
import { MeasureError, measureRear, measureSide, PLATE_SIZE_CM, type Reference } from '../measure/measure'
import type { CheckState } from './check'

export type Photo = CheckState['photo']
export type PhotoOutcome = { ok: true; photo: Photo } | { ok: false; message: string; resetReference: boolean }

/** A reference built from four corners tapped by hand, in any order. */
export function referenceFromTaps(kind: Reference['kind'], corners: Pt[]): Reference {
  const size = kind === 'plate' ? PLATE_SIZE_CM : { w: CARD_SIZE_CM, h: CARD_SIZE_CM }
  return { kind, tapped: true, cornersPx: orderQuad(corners), sizeCm: { ...size } }
}

/** "Chạm lại" drops a hand-tapped reference; a detected card is kept. */
export function shouldResetReference(ref: Reference | null): boolean {
  return ref !== null && ref.tapped
}

/** Turn the tapped points into a measurement, or a message telling the user what to redo. */
export function measurePhoto(mode: 'rear' | 'side', ref: Reference, points: Pt[]): PhotoOutcome {
  const name = ref.kind === 'plate' ? 'biển số' : 'thẻ chuẩn'
  try {
    if (mode === 'rear') {
      const [rackLeft, rackRight, cargoLeft, cargoRight, cargoTop, ground] = points
      return { ok: true, photo: { refKind: ref.kind, rearTapped: ref.tapped, rear: measureRear(ref, { rackLeft, rackRight, cargoLeft, cargoRight, cargoTop, ground }) } }
    }
    const [rackRearEnd, cargoRearEnd] = points
    return { ok: true, photo: { refKind: ref.kind, sideTapped: ref.tapped, side: measureSide(ref, { rackRearEnd, cargoRearEnd }) } }
  } catch (e) {
    if (e instanceof MeasureError && e.reason === 'degenerate_reference') {
      return { ok: false, message: `Không đo được từ 4 góc này — chạm lại 4 góc ${name}.`, resetReference: true }
    }
    if (e instanceof MeasureError && e.reason === 'bad_taps') {
      return { ok: false, message: 'Thứ tự chạm chưa đúng (mép trái phải nằm bên trái mép phải, điểm cao nhất phải ở trên mặt đất) — chạm lại các điểm.', resetReference: false }
    }
    return { ok: false, message: 'Chưa đủ điểm chạm — chạm lại các điểm.', resetReference: false }
  }
}
