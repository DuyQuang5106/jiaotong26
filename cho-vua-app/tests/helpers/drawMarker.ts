import { markerBits } from '../../src/measure/aruco'

export interface Img { data: Uint8ClampedArray; width: number; height: number }

export function blank(width: number, height: number): Img {
  return { data: new Uint8ClampedArray(width * height * 4).fill(255), width, height }
}

/**
 * Draw ARUCO marker `id` on white: a black border one cell wide around the 5×5 bit grid
 * ('1' = white cell). `offset` is the outer top-left corner of the black border.
 */
export function drawMarker(id: number, cellPx: number, offset: { x: number; y: number }, width = 640, height = 480): Img {
  const img = blank(width, height)
  const bits = markerBits(id)
  const n = Math.sqrt(bits.length)
  const cells = n + 2
  for (let cy = 0; cy < cells; cy++) {
    for (let cx = 0; cx < cells; cx++) {
      const inner = cx > 0 && cy > 0 && cx <= n && cy <= n
      const white = inner && bits[(cy - 1) * n + (cx - 1)] === '1'
      if (white) continue
      for (let y = 0; y < cellPx; y++) {
        for (let x = 0; x < cellPx; x++) {
          const px = offset.x + cx * cellPx + x, py = offset.y + cy * cellPx + y
          const i = (py * width + px) * 4
          img.data[i] = img.data[i + 1] = img.data[i + 2] = 0
        }
      }
    }
  }
  return img
}
