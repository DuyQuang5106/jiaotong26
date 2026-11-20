import { iv } from '../../src/domain/interval'
import type { CargoRequirement, ErrorCode, Finding, LoadInput } from '../../src/domain/types'
import { ITEMS, type ItemCategory, type ItemId } from '../../src/items/requirement'

/** A motorbike load where every check passes. */
export function base(): LoadInput {
  return {
    vehicle: 'motorbike',
    sideLeftCm: iv(0, 5), sideRightCm: iv(0, 5),
    rearCm: iv(0, 5), frontCm: iv(0, 5),
    heightCm: iv(100, 110),
    bodyLengthCm: null,
    extendsBeyondVehicle: false,
    plateAndLightsVisible: true, redMarker: true,
    lashingOk: true, carryingBulky: false, towing: false,
    looseMaterial: false, looseCovered: null,
    registered: null,
    weightKg: iv(10, 12), vehicleMaxKg: 150,
  }
}

/** A bundle of pipes a..b cm long, 25–30 cm across. */
export function pipe(a: number, b: number): CargoRequirement {
  return { lengthCm: iv(a, b), widthCm: iv(25, 30), heightCm: iv(25, 30), weightKg: null }
}

/** A box l×w×h cm, each dimension ±1 cm. */
export function box(l: number, w: number, h: number): CargoRequirement {
  return { lengthCm: iv(l - 1, l + 1), widthCm: iv(w - 1, w + 1), heightCm: iv(h - 1, h + 1), weightKg: null }
}

export function item(id: ItemId): ItemCategory {
  const it = ITEMS.find(x => x.id === id)
  if (!it) throw new Error(`no item ${id}`)
  return it
}

export function code(r: { findings: Finding[] }, c: ErrorCode): Finding {
  const f = r.findings.find(x => x.code === c)
  if (!f) throw new Error(`no finding ${c}`)
  return f
}
