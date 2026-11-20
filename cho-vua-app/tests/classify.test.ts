import { expect, test } from 'vitest'
import { classifyImage, parseClassify } from '../src/recognize/classify'

test('unknown item → khac low', () => expect(parseClassify({ itemId: 'tivi', confidence: 'high', alternatives: [] })).toMatchObject({ itemId: 'khac', confidence: 'low' }))
test('bad boolean → null', () => expect(parseClassify({ itemId: 'nem', confidence: 'high', alternatives: [], plateAndLightsVisible: 'yes' }).plateAndLightsVisible).toBeNull())
test('alternatives filtered to known ids, max 3', () => expect(parseClassify({ itemId: 'nem', confidence: 'medium', alternatives: ['tu_lanh', 'xe_hoi', 'may_giat', 'cua_go', 'ton_tam'] }).alternatives).toEqual(['tu_lanh', 'may_giat', 'cua_go']))
test('unknown vehicle → null', () => expect(parseClassify({ itemId: 'nem', confidence: 'high', alternatives: [], vehicle: 'truck' }).vehicle).toBeNull())
test('garbage input → khac low', () => expect(parseClassify('nope')).toMatchObject({ itemId: 'khac', confidence: 'low', alternatives: [] }))
test('valid result passes through', () => expect(parseClassify({ itemId: 'ong_nhua', confidence: 'high', alternatives: ['thep_cay'], vehicle: 'motorbike', plateAndLightsVisible: false, carryingBulky: true, looksSelfMade: false })).toEqual({ itemId: 'ong_nhua', confidence: 'high', alternatives: ['thep_cay'], vehicle: 'motorbike', plateAndLightsVisible: false, carryingBulky: true, looksSelfMade: false }))
test('server down → null', async () => expect(await classifyImage(new Blob(['x']), async () => new Response('', { status: 503 }))).toBeNull())
test('network error → null', async () => expect(await classifyImage(new Blob(['x']), async () => { throw new Error('offline') })).toBeNull())
test('server answer is parsed', async () => {
  const r = await classifyImage(new Blob(['x'], { type: 'image/jpeg' }), async () => new Response(JSON.stringify({ itemId: 'tu_lanh', confidence: 'high', alternatives: [] }), { status: 200 }))
  expect(r?.itemId).toBe('tu_lanh')
})
