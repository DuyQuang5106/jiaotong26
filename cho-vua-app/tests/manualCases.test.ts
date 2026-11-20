import { expect, test } from 'vitest'
import { runCheck } from '../src/ui/check'
import { CASES, toState } from './manualCases'

for (const c of CASES) {
  test(`${c.id}: ${c.title}`, () => {
    const r = runCheck(toState(c.input))
    const light = (code: string) => r.findings.find(f => f.code === code)?.light ?? 'none'
    for (const [code, want] of Object.entries(c.expect.lights)) expect(light(code), code).toBe(want)
    expect(r.overall).toBe(c.expect.overall)
    if (c.expect.firstVehicle !== undefined) expect(r.options[0]?.vehicle.name ?? null).toBe(c.expect.firstVehicle)
    if (c.expect.vehicleIncludes) expect(r.options.map(o => o.vehicle.name)).toContain(c.expect.vehicleIncludes)
  })
}
