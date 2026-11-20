import * as vendor from '../vendor/js-aruco2/aruco.js'
import { orderQuad, type Pt } from './homography'
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

const ar = (): ArNamespace => vendor.AR as ArNamespace

let detector: { detect(img: ImageLike): ArMarker[] } | null = null

/** Bit string of a marker in the card dictionary ('1' = white cell), row by row. */
export function markerBits(id: number): string {
  return new (ar().Dictionary)(DICTIONARY).codeList[id]
}

/** Find the reference card in an image; null when it is not visible. */
export function detectMarker(img: ImageLike): Reference | null {
  detector ??= new (ar().Detector)({ dictionaryName: DICTIONARY })
  const m = detector.detect(img).find(x => x.id === CARD_ID)
  if (!m) return null
  return { kind: 'aruco', tapped: false, cornersPx: orderQuad(m.corners.map(p => ({ x: p.x, y: p.y }))), sizeCm: { w: CARD_SIZE_CM, h: CARD_SIZE_CM } }
}
