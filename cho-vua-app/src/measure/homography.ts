export type Pt = { x: number; y: number }
export type Quad = [Pt, Pt, Pt, Pt]

export type MeasureErrorReason = 'degenerate_reference' | 'missing_taps' | 'bad_taps'

export class MeasureError extends Error {
  reason: MeasureErrorReason
  constructor(reason: MeasureErrorReason) {
    super(reason)
    this.reason = reason
    this.name = 'MeasureError'
  }
}

/** Put four corners in top-left, top-right, bottom-right, bottom-left order, whatever order they were tapped in. */
export function orderQuad(c: Pt[]): Quad {
  const by = (f: (p: Pt) => number, pick: 'min' | 'max') =>
    c.reduce((a, b) => ((pick === 'min' ? f(b) < f(a) : f(b) > f(a)) ? b : a))
  return [by(p => p.x + p.y, 'min'), by(p => p.x - p.y, 'max'), by(p => p.x + p.y, 'max'), by(p => p.x - p.y, 'min')]
}

/** Solve A·x = b (n×n) by Gaussian elimination with partial pivoting. */
function solve(A: number[][], b: number[]): number[] {
  const n = b.length
  const M = A.map((row, i) => [...row, b[i]])
  for (let c = 0; c < n; c++) {
    let p = c
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r
    if (Math.abs(M[p][c]) < 1e-12) throw new MeasureError('degenerate_reference')
    ;[M[c], M[p]] = [M[p], M[c]]
    for (let r = 0; r < n; r++) {
      if (r === c) continue
      const f = M[r][c] / M[c][c]
      for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k]
    }
  }
  return M.map((row, i) => row[n] / row[i])
}

function shoelace(q: Quad): number {
  let s = 0
  for (let i = 0; i < 4; i++) {
    const a = q[i], b = q[(i + 1) % 4]
    s += a.x * b.y - b.x * a.y
  }
  return Math.abs(s) / 2
}

function assertNotDegenerate(q: Quad): void {
  const xs = q.map(p => p.x), ys = q.map(p => p.y)
  const box = (Math.max(...xs) - Math.min(...xs)) * (Math.max(...ys) - Math.min(...ys))
  if (!(box > 0) || shoelace(q) < 0.01 * box) throw new MeasureError('degenerate_reference')
}

/** 3×3 homography (row-major, h33 = 1) mapping src[i] → dst[i]; direct linear transform on 4 points. */
export function computeHomography(src: Quad, dst: Quad): number[] {
  assertNotDegenerate(src)
  assertNotDegenerate(dst)
  const A: number[][] = []
  const b: number[] = []
  for (let i = 0; i < 4; i++) {
    const { x, y } = src[i], { x: u, y: v } = dst[i]
    A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u)
    A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v)
  }
  return [...solve(A, b), 1]
}

export function applyH(H: number[], p: Pt): Pt {
  const w = H[6] * p.x + H[7] * p.y + H[8]
  return { x: (H[0] * p.x + H[1] * p.y + H[2]) / w, y: (H[3] * p.x + H[4] * p.y + H[5]) / w }
}
