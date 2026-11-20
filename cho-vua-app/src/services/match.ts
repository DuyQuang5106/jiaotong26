import type { CargoRequirement } from '../domain/types'
import data from '../data/vehicles.json'

export interface PriceModel { baseVnd: number; baseKm: number; perKmVnd: number }
export type City = 'HCM' | 'HN'

export interface Vehicle {
  id: string
  provider: 'lalamove' | 'ahamove' | 'grab'
  name: string
  city: City
  bedCm: { l: number; w: number; h: number }
  maxKg: number | null
  price: PriceModel | null
  bookingUrl: string
  source: string
  accessed: string
  note?: string
}

export interface VehicleOption { vehicle: Vehicle; estimateVnd: number | null; weightUnchecked: boolean }

export const VEHICLES = data as Vehicle[]

export function estimatePrice(p: PriceModel, km: number): number {
  return km <= p.baseKm ? p.baseVnd : Math.round(p.baseVnd + p.perKmVnd * (km - p.baseKm))
}

function fits(req: CargoRequirement, v: Vehicle): boolean {
  const need = [req.lengthCm.max, req.widthCm.max].sort((a, b) => b - a)
  const bed = [v.bedCm.l, v.bedCm.w].sort((a, b) => b - a)
  if (need[0] > bed[0] || need[1] > bed[1]) return false
  if (req.heightCm.max > v.bedCm.h) return false
  if (req.weightKg !== null && v.maxKg !== null && req.weightKg.max > v.maxKg) return false
  return true
}

/**
 * Vehicles whose bed holds the cargo at the upper bound of every interval,
 * smallest first (by capacity, then bed area). Unknown capacity sorts as 0.
 */
export function matchVehicles(req: CargoRequirement, all: Vehicle[], city: City, km: number, limit = 3): VehicleOption[] {
  return all
    .filter(v => v.city === city && fits(req, v))
    .sort((a, b) => (a.maxKg ?? 0) - (b.maxKg ?? 0) || a.bedCm.l * a.bedCm.w - b.bedCm.l * b.bedCm.w)
    .slice(0, limit)
    .map(v => ({
      vehicle: v,
      estimateVnd: v.price ? estimatePrice(v.price, km) : null,
      weightUnchecked: req.weightKg === null || v.maxKg === null,
    }))
}
