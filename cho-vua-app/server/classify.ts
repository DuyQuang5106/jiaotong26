import Anthropic from '@anthropic-ai/sdk'
import { ITEMS, ITEM_IDS } from '../src/items/requirement'
import { parseClassify, type ClassifyResult } from '../src/recognize/classify'

const MODEL = 'claude-opus-5-5'

const SCHEMA = {
  type: 'object',
  properties: {
    itemId: { type: 'string', enum: ITEM_IDS },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    alternatives: { type: 'array', items: { type: 'string', enum: ITEM_IDS } },
    vehicle: { type: ['string', 'null'], enum: ['motorbike', 'non_motorized', 'motor_3_4_wheel', null] },
    plateAndLightsVisible: { type: ['boolean', 'null'] },
    carryingBulky: { type: ['boolean', 'null'] },
    looksSelfMade: { type: ['boolean', 'null'] },
  },
  required: ['itemId', 'confidence', 'alternatives', 'vehicle', 'plateAndLightsVisible', 'carryingBulky', 'looksSelfMade'],
  additionalProperties: false,
} as const

const PROMPT = `You look at one photo taken at a building-materials or furniture shop in Vietnam, of goods and possibly the vehicle that will carry them.
Classify the goods into exactly one of these ids:
${ITEMS.map(i => `- ${i.id}: ${i.name}`).join('\n')}
Use "khac" when none fits. Give up to 3 other plausible ids in "alternatives".
"vehicle": motorbike (xe máy), non_motorized (bicycle, push/pedal cart), motor_3_4_wheel (three- or four-wheeled motor cart); null if no vehicle is visible.
"plateAndLightsVisible": true if the rear licence plate and rear light are visible and not covered by goods, false if goods cover them, null if you cannot tell.
"carryingBulky": true if the rider or a passenger is holding or carrying goods in their arms or on their shoulder, null if you cannot tell.
"looksSelfMade": true if the vehicle looks home-built or improvised (welded frame, no factory body), null if you cannot tell.
Do not estimate sizes or weights. Answer only with the JSON object.`

export class ClassifyUnavailable extends Error {}

let client: Anthropic | null = null

/** Recognise the goods in one image. The image is sent to the API and not stored or logged here. */
export async function classifyWithClaude(imageBase64: string, mediaType: string): Promise<ClassifyResult> {
  client ??= new Anthropic()
  try {
    const response = await client.beta.messages.create({
      model: MODEL,
      max_tokens: 2000,
      betas: ['server-side-fallback-2026-07-01'],
      fallbacks: 'default',
      output_config: { effort: 'low', format: { type: 'json_schema', schema: SCHEMA } },
      messages: [{
        role: 'user',
        content: [
          { type: 'image', source: { type: 'base64', media_type: mediaType as 'image/jpeg', data: imageBase64 } },
          { type: 'text', text: PROMPT },
        ],
      }],
    })
    if (response.stop_reason === 'refusal') return parseClassify(null)
    const text = response.content.flatMap(b => (b.type === 'text' ? [b.text] : [])).join('')
    return parseClassify(JSON.parse(text))
  } catch (e) {
    if (e instanceof Anthropic.AuthenticationError) throw new ClassifyUnavailable('no credentials')
    if (e instanceof SyntaxError) return parseClassify(null)
    throw e
  }
}
