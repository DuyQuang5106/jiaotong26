import '@testing-library/jest-dom/vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, expect, test } from 'vitest'
import { iv } from '../src/domain/interval'
import App from '../src/ui/App'
import { state } from './helpers/fixtures'

afterEach(cleanup)

test('UI shows red light and open-app button', () => {
  render(<App initial={state({ itemId: 'ong_nhua', measured: { l: iv(395, 400) } })} startAt="result" />)
  expect(screen.getAllByText(/Mở lalamove/i).length).toBeGreaterThan(0)
  expect(screen.getAllByLabelText('đèn đỏ').length).toBeGreaterThan(0)
})

test('UI never shows forbidden wording', () => {
  render(<App initial={state({})} startAt="result" />)
  expect(document.body.textContent).not.toMatch(/thực thi luật|chứng nhận an toàn/i)
})

test('result shows the four parts', () => {
  render(<App initial={state({})} startAt="result" />)
  for (const h of ['Loại hàng', 'Kích cỡ ước tính', 'Luật áp dụng', 'Xe phù hợp']) expect(screen.getByRole('heading', { name: h })).toBeInTheDocument()
})

test('assumed sizes are labelled', () => {
  render(<App initial={state({})} startAt="result" />)
  expect(document.body.textContent).toMatch(/giả định/)
})

test('red findings are listed before yellow ones', () => {
  // E01 is yellow (sides not measured) and comes before E02 (red) in code order
  render(<App initial={state({ stage: 'loaded', manualLoad: { rearCm: iv(80, 82) } })} startAt="result" />)
  const lights = Array.from(document.querySelectorAll('.findings .light')).map(e => e.getAttribute('aria-label'))
  expect(lights[0]).toBe('đèn đỏ')
  expect(lights.indexOf('đèn vàng')).toBeGreaterThan(lights.lastIndexOf('đèn đỏ'))
})

test('ticket button saves a record and shows the ticket', async () => {
  localStorage.clear()
  render(<App initial={state({})} startAt="result" />)
  fireEvent.click(screen.getByRole('button', { name: 'Phiếu kết quả' }))
  expect(screen.getByRole('heading', { name: 'Phiếu kết quả' })).toBeInTheDocument()
  expect(JSON.parse(localStorage.getItem('chovua.checks.v1')!)).toHaveLength(1)
})

test('field mode lists saved checks with tape inputs', () => {
  localStorage.clear()
  render(<App initial={state({})} startAt="result" />)
  fireEvent.click(screen.getByRole('button', { name: 'Phiếu kết quả' }))
  fireEvent.click(screen.getByRole('button', { name: 'Thực địa' }))
  expect(screen.getByRole('heading', { name: 'Chế độ thực địa' })).toBeInTheDocument()
  expect(screen.getAllByLabelText(/Lòi sau/).length).toBe(1)
})

test('no matching vehicle message', () => {
  render(<App initial={state({ city: 'HN', itemId: 'thep_cay' })} startAt="result" />)
  expect(screen.getByText(/Không có xe phù hợp trong bảng cho HN/)).toBeInTheDocument()
})
