export type Light = 'green' | 'yellow' | 'red'
export interface Interval { min: number; max: number }

export type VehicleKind = 'motorbike' | 'non_motorized' | 'motor_3_4_wheel'
export type ErrorCode = 'E01' | 'E02' | 'E03' | 'E04' | 'E05' | 'E06' | 'E07' | 'E08' | 'E09' | 'E10' | 'E11'

export interface LoadInput {
  vehicle: VehicleKind
  /** Motorbike: beyond the rack edge. Non-motorized: beyond the wheel. */
  sideLeftCm: Interval | null
  sideRightCm: Interval | null
  /** Motorbike: behind the rack. Non-motorized: beyond the body. */
  rearCm: Interval | null
  frontCm: Interval | null
  /** From the road surface. */
  heightCm: Interval | null
  /** Non-motorized only. */
  bodyLengthCm: number | null
  extendsBeyondVehicle: boolean | null
  plateAndLightsVisible: boolean | null
  redMarker: boolean | null
  lashingOk: boolean | null
  carryingBulky: boolean | null
  towing: boolean | null
  looseMaterial: boolean
  looseCovered: boolean | null
  /** Used for motor_3_4_wheel. */
  registered: boolean | null
  weightKg: Interval | null
  vehicleMaxKg: number | null
}

/** What a vehicle's cargo bed must hold. Vehicles are chosen against the upper bounds. */
export interface CargoRequirement {
  lengthCm: Interval
  widthCm: Interval
  heightCm: Interval
  weightKg: Interval | null
}

export interface Finding {
  code: ErrorCode
  light: Light
  title: string
  detail: string
  legalBasis: string
  fine: string
}
