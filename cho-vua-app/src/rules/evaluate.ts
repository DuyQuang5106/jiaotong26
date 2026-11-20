import { fmtM, lightFromFlag, lightVsMax, worst } from '../domain/interval'
import type { ErrorCode, Finding, Interval, Light, LoadInput } from '../domain/types'
import { MOTORBIKE, NON_MOTORIZED, RULES, nonMotorizedFrontRearLimit, ruleColumn } from './limits'

const capYellow = (l: Light): Light => (l === 'red' ? 'yellow' : l)
const show = (a: Interval | null): string => (a === null ? 'chưa đo' : fmtM(a))
const meters = (cm: number): string => `${(cm / 100).toFixed(2).replace('.', ',')} m`

export function evaluateLoad(input: LoadInput): { findings: Finding[]; overall: Light } {
  const col = ruleColumn(input.vehicle)
  const findings: Finding[] = []
  const push = (code: ErrorCode, light: Light, detail: string) => {
    const r = RULES[code]
    findings.push({ code, light, title: r.title, detail, legalBasis: r.basis[col], fine: r.fine[col] })
  }
  const nm = input.vehicle === 'non_motorized'

  // E01 — both sides
  const sideLimit = nm ? NON_MOTORIZED.sideCm : MOTORBIKE.sideCm
  push('E01', worst([lightVsMax(input.sideLeftCm, sideLimit), lightVsMax(input.sideRightCm, sideLimit)]),
    `Trái ${show(input.sideLeftCm)}, phải ${show(input.sideRightCm)}; tối đa ${meters(sideLimit)} mỗi bên ${nm ? 'bánh xe' : 'giá chở hàng'}.`)

  // E02 — motorbike: rear only (no front limit in law); non-motorized: rear and front
  if (nm) {
    const limit = nonMotorizedFrontRearLimit(input.bodyLengthCm)
    let light = worst([lightVsMax(input.rearCm, limit), lightVsMax(input.frontCm, limit)])
    let detail = `Sau ${show(input.rearCm)}, trước ${show(input.frontCm)}; tối đa ${meters(limit)} (không quá 1/3 thân xe và không quá 1 m — cách hiểu Điều 31 khoản 5).`
    if (input.bodyLengthCm === null && light === 'green') {
      light = 'yellow'
      detail += ' Chưa biết chiều dài thân xe để kiểm quy tắc 1/3.'
    }
    push('E02', light, detail)
  } else {
    push('E02', lightVsMax(input.rearCm, MOTORBIKE.rearCm), `Phía sau giá chở hàng ${show(input.rearCm)}; tối đa 0,50 m.`)
  }

  // E03 — height limit exists only for motorbikes
  if (!nm) push('E03', lightVsMax(input.heightCm, MOTORBIKE.heightCm), `Cao từ mặt đường ${show(input.heightCm)}; tối đa 2,00 m.`)

  push('E04', lightFromFlag(input.plateAndLightsVisible, false), 'Hàng không được che biển số, đèn hoặc cản tầm nhìn người lái.')

  if (input.extendsBeyondVehicle !== false) {
    // A fitted marker settles it either way; otherwise an uncertain overhang stays a question.
    const light = input.redMarker === true ? 'green' : input.extendsBeyondVehicle === null ? 'yellow' : lightFromFlag(input.redMarker, false)
    push('E05', light, 'Hàng lòi trước/sau xe phải có báo hiệu màu đỏ ở điểm đầu và điểm cuối; ban đêm phải có đèn.')
  }

  push('E06', lightFromFlag(input.lashingOk, false), 'Hàng phải xếp gọn và chằng buộc chắc chắn.')
  push('E07', capYellow(lightFromFlag(input.carryingBulky, true)), 'Luật không định nghĩa "vật cồng kềnh" bằng số; đây chỉ là cảnh báo.')
  push('E08', lightFromFlag(input.towing, true), 'Không được kéo theo xe khác hoặc vật khác.')

  if (input.vehicle === 'motor_3_4_wheel') {
    push('E09', lightFromFlag(input.registered, false), 'Xe ba, bốn bánh có gắn động cơ phải có đăng ký, biển số và đủ điều kiện kỹ thuật.')
  }

  if (input.looseMaterial) {
    push('E10', lightFromFlag(input.looseCovered, false), 'Hàng rời, vật liệu xây dựng phải đóng bao hoặc che phủ, không để rơi vãi.')
  }

  const w = input.weightKg
  const max = input.vehicleMaxKg
  if (w === null || max === null) {
    push('E11', 'yellow', 'Chưa có khối lượng hàng hoặc tải cho phép của xe.')
  } else {
    push('E11', lightVsMax(w, max), `Khối lượng ${w.min}–${w.max} kg; tải cho phép ${max} kg.`)
  }

  return { findings, overall: worst(findings.map(f => f.light)) }
}
