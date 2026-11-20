import '@testing-library/jest-dom/vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, expect, test } from 'vitest'
import type { ClassifyResult } from '../src/recognize/classify'
import { applySuggestion, StepItem } from '../src/ui/StepItem'
import { state } from './helpers/fixtures'

afterEach(cleanup)

const r = (p: Partial<ClassifyResult> = {}): ClassifyResult => ({ itemId: 'tu_lanh', confidence: 'high', alternatives: ['may_giat'], vehicle: null, plateAndLightsVisible: false, carryingBulky: null, looksSelfMade: null, ...p })

test('suggestion does not overwrite answers the user already gave', () => {
  const s = state({})
  expect(applySuggestion(s, r()).answers!.plateAndLightsVisible).toBe(true)
})

test('suggestion fills unanswered questions', () => {
  const s = state({})
  const p = applySuggestion({ ...s, answers: { ...s.answers, plateAndLightsVisible: null } }, r())
  expect(p.answers!.plateAndLightsVisible).toBe(false)
})

test('self-made look switches to the 3–4 wheel motor vehicle', () => expect(applySuggestion(state({}), r({ looksSelfMade: true })).vehicle).toBe('motor_3_4_wheel'))

test('failed recognition falls back to manual selection', async () => {
  render(<StepItem s={state({})} set={() => {}} classify={async () => null} />)
  fireEvent.change(document.querySelector('input[type=file]')!, { target: { files: [new File(['x'], 'a.jpg', { type: 'image/jpeg' })] } })
  await waitFor(() => expect(screen.getByText(/Không nhận diện được/)).toBeInTheDocument())
})

test('recognised item can be applied', async () => {
  let applied: unknown = null
  render(<StepItem s={state({})} set={p => { applied = p }} classify={async () => r()} />)
  fireEvent.change(document.querySelector('input[type=file]')!, { target: { files: [new File(['x'], 'a.jpg', { type: 'image/jpeg' })] } })
  fireEvent.click(await screen.findByRole('button', { name: 'Dùng gợi ý' }))
  expect(applied).toMatchObject({ itemId: 'tu_lanh' })
})
