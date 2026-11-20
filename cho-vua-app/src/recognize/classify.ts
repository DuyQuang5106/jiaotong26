import type { VehicleKind } from '../domain/types'
import { ITEM_IDS, type ItemId } from '../items/requirement'

export interface ClassifyResult {
  itemId: ItemId
  confidence: 'high' | 'medium' | 'low'
  alternatives: ItemId[]
  vehicle: VehicleKind | null
  plateAndLightsVisible: boolean | null
  carryingBulky: boolean | null
  looksSelfMade: boolean | null
}

const VEHICLE_KINDS: VehicleKind[] = ['motorbike', 'non_motorized', 'motor_3_4_wheel']
const CONFIDENCE = ['high', 'medium', 'low'] as const

const isItem = (v: unknown): v is ItemId => typeof v === 'string' && (ITEM_IDS as string[]).includes(v)
const bool = (v: unknown): boolean | null => (typeof v === 'boolean' ? v : null)

/** Validate whatever came back from the model or the server; never trust its shape. Shared by client and server. */
export function parseClassify(raw: unknown): ClassifyResult {
  const o = (raw && typeof raw === 'object' ? raw : {}) as Record<string, unknown>
  const known = isItem(o.itemId)
  const conf = CONFIDENCE.includes(o.confidence as never) ? (o.confidence as ClassifyResult['confidence']) : 'low'
  return {
    itemId: known ? (o.itemId as ItemId) : 'khac',
    confidence: known ? conf : 'low',
    alternatives: (Array.isArray(o.alternatives) ? o.alternatives : []).filter(isItem).slice(0, 3),
    vehicle: VEHICLE_KINDS.includes(o.vehicle as VehicleKind) ? (o.vehicle as VehicleKind) : null,
    plateAndLightsVisible: bool(o.plateAndLightsVisible),
    carryingBulky: bool(o.carryingBulky),
    looksSelfMade: bool(o.looksSelfMade),
  }
}

const MAX_SIDE = 1024

/** Shrink the photo to at most 1024 px on its long side (JPEG). Falls back to the original bytes. */
async function shrink(file: Blob): Promise<Blob> {
  if (typeof createImageBitmap !== 'function' || typeof document === 'undefined') return file
  try {
    const bmp = await createImageBitmap(file)
    const k = Math.min(1, MAX_SIDE / Math.max(bmp.width, bmp.height))
    const c = document.createElement('canvas')
    c.width = Math.round(bmp.width * k)
    c.height = Math.round(bmp.height * k)
    c.getContext('2d')!.drawImage(bmp, 0, 0, c.width, c.height)
    return await new Promise<Blob>((ok, fail) => c.toBlob(b => (b ? ok(b) : fail(new Error('toBlob'))), 'image/jpeg', 0.85))
  } catch {
    return file
  }
}

async function toBase64(b: Blob): Promise<string> {
  const bytes = new Uint8Array(await b.arrayBuffer())
  let s = ''
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000))
  return btoa(s)
}

/** Ask the server to recognise the goods. Any failure returns null so the UI falls back to manual selection. */
export async function classifyImage(file: Blob, fetchFn: typeof fetch = fetch): Promise<ClassifyResult | null> {
  try {
    const img = await shrink(file)
    const res = await fetchFn('/api/classify', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ imageBase64: await toBase64(img), mediaType: img.type || 'image/jpeg' }),
    })
    if (!res.ok) return null
    return parseClassify(await res.json())
  } catch {
    return null
  }
}
