import type { Light } from '../domain/types'

const LABEL: Record<Light, string> = { green: 'đèn xanh', yellow: 'đèn vàng', red: 'đèn đỏ' }

export function LightDot({ light }: { light: Light }) {
  return <span className={`light light-${light}`} role="img" aria-label={LABEL[light]} />
}
