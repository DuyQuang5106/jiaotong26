import * as pkg from 'js-aruco2'
import type { Pt, Quad } from './homography'
import type { Reference } from './measure'

/** The printed card: ARUCO dictionary, id 0, black border 15 cm per side. */
export const CARD_SIZE_CM = 15
export const CARD_ID = 0
const DICTIONARY = 'ARUCO'

interface ArMarker { id: number; corners: Pt[] }
interface ArNamespace {
  Detector: new (cfg: { dictionaryName: string }) => { detect(img: ImageLike): ArMarker[] }
  Dictionary: new (name: string) => { codeList: string[] }
}
export interface ImageLike { data: Uint8ClampedArray; width: number; height: number }

// js-aruco2 is CommonJS that assigns `this.AR`; depending on the bundler this lands on
// the module exports or on globalThis.
function ar(): ArNamespace {
  const m = pkg as unknown as { AR?: ArNamespace; default?: { AR?: ArNamespace } }
  const found = m.AR ?? m.default?.AR ?? (globalThis as { AR?: ArNamespace }).AR
  if (!found) throw new Error('js-aruco2 not loaded')
  return found
}

let detector: { detect(img: ImageLike): ArMarker[] } | null = null

/** Bit string of a marker in the card dictionary ('1' = white cell), row by row. */
export function markerBits(id: number): string {
  return new (ar().Dictionary)(DICTIONARY).codeList[id]
}

function order(c: Pt[]): Quad {
  const by = (f: (p: Pt) => number, pick: 'min' | 'max') =>
    c.reduce((a, b) => ((pick === 'min' ? f(b) < f(a) : f(b) > f(a)) ? b : a))
  return [
    by(p => p.x + p.y, 'min'), // top-left
    by(p => p.x - p.y, 'max'), // top-right
    by(p => p.x + p.y, 'max'), // bottom-right
    by(p => p.x - p.y, 'min'), // bottom-left
  ]
}

/** Find the reference card in an image; null when it is not visible. */
export function detectMarker(img: ImageLike): Reference | null {
  detector ??= new (ar().Detector)({ dictionaryName: DICTIONARY })
  const m = detector.detect(img).find(x => x.id === CARD_ID)
  if (!m) return null
  return { kind: 'aruco', cornersPx: order(m.corners.map(p => ({ x: p.x, y: p.y }))), sizeCm: { w: CARD_SIZE_CM, h: CARD_SIZE_CM } }
}
