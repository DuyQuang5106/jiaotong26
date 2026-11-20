import { add, clamp0, iv, scale, sub } from '../domain/interval'
import type { CargoRequirement, Interval, Light, LoadInput } from '../domain/types'
import { evaluateLoad } from './evaluate'

export interface RackAssumption {
  widthCm: Interval
  lengthCm: Interval
  /** Rack top above the road. */
  heightCm: Interval
  /** How far goods may reach forward of the rack (towards the rider). */
  forwardCm: Interval
  assumption: true
}

/** GIẢ ĐỊNH — thay bằng số đo giá chở hàng của các xe phổ biến ở thực địa. */
export const DEFAULT_RACK: RackAssumption = {
  widthCm: iv(30, 50),
  lengthCm: iv(30, 50),
  heightCm: iv(70, 90),
  forwardCm: iv(0, 30),
  assumption: true,
}

type Geometry = Pick<LoadInput, 'sideLeftCm' | 'sideRightCm' | 'rearCm' | 'heightCm' | 'extendsBeyondVehicle'>

function place(along: Interval, across: Interval, h: Interval, rack: RackAssumption): Geometry {
  const side = clamp0(scale(sub(across, rack.widthCm), 0.5))
  const rear = clamp0(sub(sub(along, rack.lengthCm), rack.forwardCm))
  // null when it may or may not stick out, so the red-marker check stays visible.
  return { sideLeftCm: side, sideRightCm: side, rearCm: rear, heightCm: add(h, rack.heightCm), extendsBeyondVehicle: rear.min > 0 ? true : rear.max > 0 ? null : false }
}

const RANK: Record<Light, number> = { green: 0, yellow: 1, red: 2 }

/** Where goods would stick out if loaded on a motorbike, in the better of the two orientations. */
export function predictMotorbike(req: CargoRequirement, rack: RackAssumption = DEFAULT_RACK): Geometry {
  const options = [
    place(req.lengthCm, req.widthCm, req.heightCm, rack),
    place(req.widthCm, req.lengthCm, req.heightCm, rack),
  ]
  const score = (g: Geometry) => {
    const probe: LoadInput = {
      vehicle: 'motorbike', ...g, frontCm: null, bodyLengthCm: null,
      plateAndLightsVisible: true, redMarker: true, lashingOk: true, carryingBulky: false, towing: false,
      looseMaterial: false, looseCovered: null, registered: null, weightKg: iv(0, 0), vehicleMaxKg: 1,
    }
    const fs = evaluateLoad(probe).findings.filter(f => f.code === 'E01' || f.code === 'E02' || f.code === 'E03')
    return Math.max(...fs.map(f => RANK[f.light]))
  }
  // Lengthwise is how goods are normally loaded; go crosswise only if it is strictly better.
  return score(options[1]) < score(options[0]) ? options[1] : options[0]
}
