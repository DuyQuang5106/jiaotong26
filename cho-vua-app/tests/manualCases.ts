/**
 * Hand-entry test cases. Each case is written the way a person fills in the app,
 * and `toState` turns it into a CheckState exactly as the screens do:
 * a typed cm value v becomes v ± 1 cm, a typed weight is exact, "Không rõ" is null.
 * TESTCASES_nhap_tay.md lists the same cases for trying by hand.
 */
import { around, iv } from '../src/domain/interval'
import type { ErrorCode, Light, VehicleKind } from '../src/domain/types'
import type { ItemId } from '../src/items/requirement'
import type { City } from '../src/services/match'
import type { CheckState } from '../src/ui/check'

type Ans = 'co' | 'khong' | 'khong_ro'

export interface UiInput {
  stage: 'pre_load' | 'loaded'
  vehicle: VehicleKind
  city?: City
  item: ItemId
  qty?: number
  /** "Kích thước cả lô hàng" (cm) */
  hang?: { dai?: number; rong?: number; cao?: number }
  /** "Hàng đã chất" overhang (cm) */
  loi?: { trai?: number; phai?: number; sau?: number; truoc?: number; cao?: number }
  /** Kiểm nhanh */
  hoi?: { bienSo?: Ans; coDo?: Ans; chang?: Ans; omVac?: Ans; keo?: Ans; phu?: Ans; dangKy?: Ans }
  thanXe?: number
  kg?: number
  taiXe?: number
}

export interface ManualCase {
  id: string
  title: string
  input: UiInput
  expect: {
    overall: Light
    lights: Partial<Record<ErrorCode, Light | 'none'>>
    /** Name of the first suggested vehicle; null = "Không có xe phù hợp". */
    firstVehicle?: string | null
    vehicleIncludes?: string
  }
}

const TAPE = 1
const cm = (v: number | undefined) => (v === undefined ? undefined : around(v, TAPE))
const ans = (a: Ans | undefined, dflt: boolean | null): boolean | null => (a === undefined ? dflt : a === 'co' ? true : a === 'khong' ? false : null)

/** All good answers unless the case says otherwise. */
export function toState(u: UiInput): CheckState {
  const h = u.hoi ?? {}
  const measured: CheckState['measured'] = {}
  if (u.hang?.dai !== undefined) measured.l = cm(u.hang.dai)
  if (u.hang?.rong !== undefined) measured.w = cm(u.hang.rong)
  if (u.hang?.cao !== undefined) measured.h = cm(u.hang.cao)
  const manualLoad: CheckState['manualLoad'] = {}
  if (u.loi?.trai !== undefined) manualLoad.sideLeftCm = cm(u.loi.trai)
  if (u.loi?.phai !== undefined) manualLoad.sideRightCm = cm(u.loi.phai)
  if (u.loi?.sau !== undefined) manualLoad.rearCm = cm(u.loi.sau)
  if (u.loi?.truoc !== undefined) manualLoad.frontCm = cm(u.loi.truoc)
  if (u.loi?.cao !== undefined) manualLoad.heightCm = cm(u.loi.cao)
  return {
    stage: u.stage, vehicle: u.vehicle, city: u.city ?? 'HCM', km: 5,
    itemId: u.item, qty: u.qty ?? 1, measured, manualLoad, photo: {},
    answers: {
      plateAndLightsVisible: ans(h.bienSo, true),
      redMarker: ans(h.coDo, true),
      lashingOk: ans(h.chang, true),
      carryingBulky: ans(h.omVac, false),
      towing: ans(h.keo, false),
      looseCovered: ans(h.phu, true),
      registered: ans(h.dangKy, true),
      bodyLengthCm: u.thanXe ?? null,
    },
    weightKgManual: u.kg === undefined ? null : iv(u.kg, u.kg),
    vehicleMaxKg: u.taiXe ?? null,
  }
}

const GOOD_LOAD = { trai: 20, phai: 20, sau: 30, cao: 150 }

export const CASES: ManualCase[] = [
  {
    id: 'TC01', title: 'Ống nhựa 4 m lúc bán, định chở bằng xe máy (TP.HCM)',
    input: { stage: 'pre_load', vehicle: 'motorbike', item: 'ong_nhua', hang: { dai: 400 } },
    expect: { overall: 'red', lights: { E01: 'green', E02: 'red', E03: 'green', E05: 'green', E11: 'yellow' }, firstVehicle: 'Xe tải 2500kg' },
  },
  {
    id: 'TC02', title: 'Ống nhựa 4 m ở Hà Nội — bảng xe không có thùng đủ dài',
    input: { stage: 'pre_load', vehicle: 'motorbike', city: 'HN', item: 'ong_nhua', hang: { dai: 400 } },
    expect: { overall: 'red', lights: { E02: 'red' }, firstVehicle: null },
  },
  {
    id: 'TC03', title: 'Thùng carton đã đo 40×30×30 cm, 10 kg, lúc bán, xe máy',
    input: { stage: 'pre_load', vehicle: 'motorbike', item: 'thung_carton', hang: { dai: 40, rong: 30, cao: 30 }, kg: 10, taiXe: 150 },
    expect: { overall: 'green', lights: { E01: 'green', E02: 'green', E03: 'green', E05: 'green', E11: 'green' }, vehicleIncludes: 'Xe máy' },
  },
  {
    id: 'TC04', title: 'Tủ lạnh cao 160 cm dựng đứng, lúc bán, xe máy',
    input: { stage: 'pre_load', vehicle: 'motorbike', item: 'tu_lanh', hang: { cao: 160 } },
    expect: { overall: 'red', lights: { E03: 'red' }, firstVehicle: 'Xe tải 1500kg' },
  },
  {
    id: 'TC05', title: 'Xe máy đã chất hàng, mọi số đo trong giới hạn',
    input: { stage: 'loaded', vehicle: 'motorbike', item: 'thung_carton', loi: GOOD_LOAD, kg: 20, taiXe: 150 },
    expect: { overall: 'green', lights: { E01: 'green', E02: 'green', E03: 'green', E04: 'green', E05: 'green', E06: 'green', E07: 'green', E08: 'green', E11: 'green' } },
  },
  {
    id: 'TC06a', title: 'Lòi sau đúng 50 cm — sát ngưỡng nên chưa chắc',
    input: { stage: 'loaded', vehicle: 'motorbike', item: 'thung_carton', loi: { ...GOOD_LOAD, sau: 50 }, kg: 20, taiXe: 150 },
    expect: { overall: 'yellow', lights: { E02: 'yellow' } },
  },
  {
    id: 'TC06b', title: 'Lòi sau 49 cm — vẫn trong giới hạn kể cả sai số',
    input: { stage: 'loaded', vehicle: 'motorbike', item: 'thung_carton', loi: { ...GOOD_LOAD, sau: 49 }, kg: 20, taiXe: 150 },
    expect: { overall: 'green', lights: { E02: 'green' } },
  },
  {
    id: 'TC07', title: 'Lòi bên trái 35 cm (giới hạn 30 cm)',
    input: { stage: 'loaded', vehicle: 'motorbike', item: 'thung_carton', loi: { ...GOOD_LOAD, trai: 35 }, kg: 20, taiXe: 150 },
    expect: { overall: 'red', lights: { E01: 'red' } },
  },
  {
    id: 'TC08', title: 'Hàng cao 205 cm tính từ mặt đường',
    input: { stage: 'loaded', vehicle: 'motorbike', item: 'thung_carton', loi: { ...GOOD_LOAD, cao: 205 }, kg: 20, taiXe: 150 },
    expect: { overall: 'red', lights: { E03: 'red' } },
  },
  {
    id: 'TC09', title: 'Xe thô sơ thân 180 cm, lòi sau 70 cm (giới hạn 60 cm), lòi bên 35 cm',
    input: { stage: 'loaded', vehicle: 'non_motorized', item: 'cua_go', thanXe: 180, loi: { trai: 35, phai: 35, sau: 70, truoc: 10 }, kg: 30, taiXe: 100 },
    expect: { overall: 'red', lights: { E01: 'green', E02: 'red', E03: 'none' } },
  },
  {
    id: 'TC10', title: 'Xe thô sơ chưa nhập chiều dài thân xe',
    input: { stage: 'loaded', vehicle: 'non_motorized', item: 'cua_go', loi: { trai: 10, phai: 10, sau: 30, truoc: 10 }, kg: 30, taiXe: 100 },
    expect: { overall: 'yellow', lights: { E02: 'yellow' } },
  },
  {
    id: 'TC11', title: 'Xe ba bánh gắn máy không có đăng ký',
    input: { stage: 'loaded', vehicle: 'motor_3_4_wheel', item: 'thung_carton', loi: GOOD_LOAD, hoi: { dangKy: 'khong' }, kg: 20, taiXe: 150 },
    expect: { overall: 'red', lights: { E09: 'red', E01: 'green' } },
  },
  {
    id: 'TC12', title: '4 bao xi măng (200 kg) chưa che phủ, xe máy tải 150 kg, chưa đo kích thước',
    input: { stage: 'pre_load', vehicle: 'motorbike', item: 'bao_xi_mang', qty: 4, hoi: { phu: 'khong' }, taiXe: 150 },
    expect: { overall: 'red', lights: { E01: 'yellow', E02: 'yellow', E03: 'yellow', E10: 'red', E11: 'red' } },
  },
  {
    id: 'TC13', title: 'Hàng che biển số, người ngồi sau ôm hàng',
    input: { stage: 'loaded', vehicle: 'motorbike', item: 'thung_carton', loi: GOOD_LOAD, hoi: { bienSo: 'khong', omVac: 'co' }, kg: 20, taiXe: 150 },
    expect: { overall: 'red', lights: { E04: 'red', E07: 'yellow' } },
  },
  {
    id: 'TC14', title: 'Xe máy kéo theo xe đẩy',
    input: { stage: 'loaded', vehicle: 'motorbike', item: 'thung_carton', loi: GOOD_LOAD, hoi: { keo: 'co' }, kg: 20, taiXe: 150 },
    expect: { overall: 'red', lights: { E08: 'red' } },
  },
  {
    id: 'TC15', title: 'Số đo ổn nhưng bỏ trống phần Kiểm nhanh (Không rõ)',
    input: { stage: 'loaded', vehicle: 'motorbike', item: 'thung_carton', loi: GOOD_LOAD, hoi: { bienSo: 'khong_ro', coDo: 'khong_ro', chang: 'khong_ro', omVac: 'khong_ro', keo: 'khong_ro' } },
    expect: { overall: 'yellow', lights: { E04: 'yellow', E05: 'yellow', E06: 'yellow', E07: 'yellow', E08: 'yellow', E11: 'yellow' } },
  },
]
