import type { CheckResult } from '../ui/check'

export const DISCLAIMER = 'Kết quả kiểm tra kích thước và cách xếp hàng, không thay thế việc kiểm tra, xử lý của cơ quan chức năng.'

const OVERALL = { green: 'Đạt', yellow: 'Cần kiểm thêm', red: 'Không đạt' } as const
const MARK = { green: '[XANH]', yellow: '[VÀNG]', red: '[ĐỎ]' } as const

/** Plain text carried by the QR code and printed on the ticket. */
export function ticketText(r: CheckResult, at: Date): string {
  const lines = [
    'CHỞ VỪA — phiếu kết quả',
    `Thời điểm: ${at.toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' })}`,
    `Hàng: ${r.item.name}`,
    `Kích cỡ: ${r.sizeText} (${r.sizeSource})`,
    `Kết quả: ${OVERALL[r.overall]}`,
    ...r.findings.filter(f => f.light !== 'green').map(f => `${MARK[f.light]} ${f.title} — ${f.fine}`),
    DISCLAIMER,
  ]
  return lines.join('\n')
}
