import Anthropic from '@anthropic-ai/sdk'
import { createServer } from 'node:http'
import { classifyWithClaude, ClassifyUnavailable } from './classify'

const PORT = Number(process.env.PORT ?? 8787)
const MAX_BODY = 8 * 1024 * 1024
const MEDIA = new Set(['image/jpeg', 'image/png', 'image/webp', 'image/gif'])

function send(res: import('node:http').ServerResponse, status: number, body: unknown) {
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8' })
  res.end(JSON.stringify(body))
}

createServer((req, res) => {
  if (req.method !== 'POST' || req.url !== '/api/classify') return send(res, 404, { error: 'not_found' })
  const chunks: Buffer[] = []
  let size = 0
  req.on('data', (c: Buffer) => {
    size += c.length
    if (size > MAX_BODY) { send(res, 413, { error: 'too_large' }); req.destroy() } else chunks.push(c)
  })
  req.on('end', async () => {
    if (res.writableEnded) return
    let body: { imageBase64?: unknown; mediaType?: unknown }
    try { body = JSON.parse(Buffer.concat(chunks).toString('utf8')) } catch { return send(res, 400, { error: 'bad_json' }) }
    const media = typeof body.mediaType === 'string' && MEDIA.has(body.mediaType) ? body.mediaType : 'image/jpeg'
    if (typeof body.imageBase64 !== 'string' || body.imageBase64.length === 0) return send(res, 400, { error: 'no_image' })
    try {
      send(res, 200, await classifyWithClaude(body.imageBase64, media))
    } catch (e) {
      // Never log the image; log only the error kind.
      if (e instanceof ClassifyUnavailable) return send(res, 503, { error: 'unavailable' })
      if (e instanceof Anthropic.RateLimitError) return send(res, 429, { error: 'rate_limited' })
      if (e instanceof Anthropic.APIError) { console.error('classify api error', e.status); return send(res, 502, { error: 'upstream' }) }
      console.error('classify failed', (e as Error).name)
      send(res, 500, { error: 'internal' })
    }
  })
}).listen(PORT, '127.0.0.1', () => console.log(`CHỞ VỪA classify server on http://127.0.0.1:${PORT} (local only; the phone reaches it through the Vite proxy)`))
