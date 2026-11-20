import type { ErrorCode, VehicleKind } from '../domain/types'

/** Luật 36/2024/QH15, Điều 33 khoản 5 (xe mô tô, xe gắn máy). */
export const MOTORBIKE = { sideCm: 30, rearCm: 50, heightCm: 200 } as const

/**
 * Luật 36/2024/QH15, Điều 31 khoản 5 (xe thô sơ).
 * Cách hiểu: "không vượt quá 1/3 chiều dài thân xe" áp dụng cho phần hàng lòi
 * trước/sau, cùng với mốc 1 m. Luật không có giới hạn chiều cao cho xe thô sơ.
 */
export const NON_MOTORIZED = { sideCm: 40, frontRearMaxCm: 100, bodyFraction: 1 / 3 } as const

export function nonMotorizedFrontRearLimit(bodyLengthCm: number | null): number {
  if (bodyLengthCm === null) return NON_MOTORIZED.frontRearMaxCm
  return Math.min(bodyLengthCm * NON_MOTORIZED.bodyFraction, NON_MOTORIZED.frontRearMaxCm)
}

interface RuleText {
  title: string
  /** [xe máy / xe có động cơ, xe thô sơ] */
  basis: [string, string]
  fine: [string, string]
}

/** Mức phạt theo Nghị định 168/2024; Nghị định 238/2026 không sửa các điều này. */
export const RULES: Record<ErrorCode, RuleText> = {
  E01: { title: 'Hàng lòi hai bên', basis: ['Luật 36 Đ33.5', 'Luật 36 Đ31.5'], fine: ['400.000–600.000đ (NĐ 168 Đ36.2.b)', '400.000–600.000đ (NĐ 168 Đ36.2.b)'] },
  E02: { title: 'Hàng lòi trước/sau', basis: ['Luật 36 Đ33.5', 'Luật 36 Đ31.5'], fine: ['400.000–600.000đ (NĐ 168 Đ36.2.b)', '400.000–600.000đ (NĐ 168 Đ36.2.b)'] },
  E03: { title: 'Hàng chất cao quá 2 m', basis: ['Luật 36 Đ33.5', '–'], fine: ['400.000–600.000đ (NĐ 168 Đ36.2.b)', '–'] },
  E04: { title: 'Hàng che biển số hoặc đèn', basis: ['Luật 36 Đ47.1.d', 'Luật 36 Đ47.1.d'], fine: ['300.000–400.000đ (NĐ 168 Đ36.1.b)', '300.000–400.000đ (NĐ 168 Đ36.1.b)'] },
  E05: { title: 'Thiếu báo hiệu đỏ khi hàng lòi trước/sau', basis: ['Luật 36 Đ47.1.e', 'Luật 36 Đ47.1.e'], fine: ['400.000–600.000đ (NĐ 168 Đ36.2.d)', '400.000–600.000đ (NĐ 168 Đ36.2.d)'] },
  E06: { title: 'Chằng buộc không chắc', basis: ['Luật 36 Đ47.1.d', 'Luật 36 Đ47.1.d'], fine: ['300.000–400.000đ (NĐ 168 Đ36.1.a)', '300.000–400.000đ (NĐ 168 Đ36.1.a)'] },
  E07: { title: 'Mang, vác vật cồng kềnh', basis: ['Luật 36 Đ33.3.đ, Đ33.4.a', 'Luật 36 Đ31.2'], fine: ['600.000–800.000đ (NĐ 168 Đ7.3.e); người ngồi sau 400.000–600.000đ (Đ12.5.a)', '150.000–250.000đ (NĐ 168 Đ9.2.c); người ngồi sau xe đạp 200.000–250.000đ (Đ12.2.đ)'] },
  E08: { title: 'Kéo theo xe hoặc vật khác', basis: ['Luật 36 Đ33.3.đ', 'Luật 36 Đ31.2'], fine: ['600.000–800.000đ (NĐ 168 Đ7.3.g)', '150.000–250.000đ (NĐ 168 Đ9.2.c)'] },
  E09: { title: 'Xe sản xuất, lắp ráp trái quy định', basis: ['Luật 36 Đ9.8', 'Luật 36 Đ9.8'], fine: ['Tịch thu phương tiện (NĐ 168 Đ14.4)', 'Tịch thu phương tiện (NĐ 168 Đ14.4)'] },
  E10: { title: 'Hàng rời, vật liệu xây dựng rơi vãi', basis: ['Luật 36 Đ47.1.đ', 'Luật 36 Đ47.1.đ'], fine: ['400.000–600.000đ (NĐ 168 Đ36.2.c)', '400.000–600.000đ (NĐ 168 Đ36.2.c)'] },
  E11: { title: 'Chở vượt khối lượng cho phép', basis: ['Luật 36 Đ47.1.c', 'Luật 36 Đ47.1.c'], fine: ['400.000–600.000đ (NĐ 168 Đ36.2.a)', '400.000–600.000đ (NĐ 168 Đ36.2.a)'] },
}

/** Motor 3–4 wheel vehicles use the motorized column. */
export function ruleColumn(v: VehicleKind): 0 | 1 {
  return v === 'non_motorized' ? 1 : 0
}
