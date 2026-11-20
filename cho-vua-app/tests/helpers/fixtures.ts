import { iv } from '../../src/domain/interval'
import type { ErrorCode, Finding, LoadInput } from '../../src/domain/types'

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

export function code(r: { findings: Finding[] }, c: ErrorCode): Finding {
  const f = r.findings.find(x => x.code === c)
  if (!f) throw new Error(`no finding ${c}`)
  return f
}
