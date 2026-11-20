# CHỞ VỪA Demo App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Web app chạy trên điện thoại. Người dùng chọn loại xe và loại hàng, nhập hoặc đo kích thước từ ảnh. App trả về 4 phần: loại hàng, ước tính kích cỡ có khoảng sai số, 11 lỗi theo luật với đèn xanh/vàng/đỏ, và xe phù hợp kèm giá. Có chế độ thực địa để ghi số đo thước và xuất CSV đánh giá sai số.

**Architecture:** Lõi nghiệp vụ là các hàm TypeScript thuần, không phụ thuộc giao diện, test bằng Vitest:
- khoảng sai số (interval);
- bộ luật 11 lỗi;
- khớp xe;
- đo bằng phép biến đổi phối cảnh từ 4 góc vật tham chiếu.

Giao diện React chỉ gọi các hàm này. Một server Node nhỏ giữ khóa API và gọi mô hình đọc ảnh để nhận diện loại hàng. App vẫn chạy đủ khi không có server, khi đó người dùng chọn loại hàng bằng tay. Phần đánh giá sai số viết bằng Python trong `traffic-data-research/` theo kiểu `unittest` sẵn có của repo.

**Tech Stack:** Vite + React + TypeScript; Vitest + @testing-library/react (jsdom); `js-aruco2` (phát hiện thẻ ArUco); `qrcode` (phiếu QR); `pngjs` (fixture ảnh trong test); Node + `tsx` cho server; Python 3.10 `unittest` cho đánh giá.

**Spec:**
- [CHO_VUA_y_tuong_vi.md](../../../traffic-data-research/reports/track2_2026_11_20/CHO_VUA_y_tuong_vi.md): luồng, 11 lỗi, kế hoạch 4 tuần.
- [luat_cho_hang_vi.md](../../../traffic-data-research/reports/track2_2026_11_20/luat_cho_hang_vi.md): căn cứ luật và mức phạt.
- [cv_do_kich_thuoc_vi.md](../../../traffic-data-research/reports/track2_2026_11_20/cv_do_kich_thuoc_vi.md): đo từ ảnh và đèn theo sai số.

## Global Constraints

- **Thư mục app:** `cho-vua-app/` ở gốc repo. Làm trên nhánh `feat/cho-vua-demo`. **Không** `git add` các file nghiên cứu đang chưa commit ngoài thư mục của task (chỉ add đúng đường dẫn trong mỗi task).
- **Nội dung hiển thị bằng tiếng Việt.** Không dùng chữ "thực thi luật", "chứng nhận an toàn", "đảm bảo không bị phạt". Phiếu ghi: "Kết quả kiểm tra kích thước và cách xếp hàng, không thay thế việc kiểm tra, xử lý của cơ quan chức năng."
- **Đơn vị nội bộ:** cm, kg, VND. Hiển thị mét với 2 chữ số thập phân, dấu phẩy thập phân (ví dụ `0,35 m`).
- **Giới hạn luật (Luật 36/2024):**
  - Xe máy: lòi mỗi bên giá ≤ **30 cm**; lòi sau giá ≤ **50 cm**; cao từ mặt đường ≤ **200 cm** (Điều 33 khoản 5).
  - Xe thô sơ: lòi mỗi bên bánh ≤ **40 cm**; lòi trước/sau ≤ **min(chiều dài thân xe / 3, 100 cm)**; không có giới hạn cao (Điều 31 khoản 5). Cách hiểu "1/3 chiều dài thân xe áp dụng cho phần lòi" phải ghi trong comment và trong chi tiết hiển thị.
- **Đèn:**
  - `max ≤ limit` → green;
  - `min > limit` → red;
  - còn lại → yellow;
  - thiếu số đo (`null`) → yellow.
  - Đúng bằng ngưỡng là green, vì luật ghi "không vượt quá".
- **Câu hỏi có / không / không rõ:** `null` → yellow; giá trị xấu → red; giá trị tốt → green. Riêng **E07** (vật cồng kềnh) tối đa chỉ yellow, vì luật không định nghĩa bằng số.
- **Kích thước biển số xe máy:** 19,0 × 14,0 cm (QCVN 08:2024/BCA).
- **Hằng số sai số tạm thời** (Task 10 thay bằng số hiệu chỉnh):
  - `TAP_ERR_PX = 6`;
  - `CORNER_ERR_PX = 2`;
  - `OFF_PLANE_REL = { aruco: 0.03, plate: 0.05 }`.
- **Chọn xe thay thế:** theo **cận trên** của mọi khoảng. Không ước khối lượng từ ảnh; khối lượng chỉ lấy từ danh mục mẫu (ghi "ước theo loại hàng") hoặc người dùng nhập.
- **Không lưu ảnh** ở server hay localStorage. Chỉ lưu số đo và kết quả. Khóa API chỉ nằm ở server (biến môi trường `ANTHROPIC_API_KEY`).
- **Camera:** dùng `<input type="file" accept="image/*" capture="environment">`, không cần HTTPS khi chạy qua mạng LAN.
- **Số liệu giả định** (giá chở hàng, danh mục hàng mẫu) phải có cờ `assumption: true` và nhãn "giả định" trên giao diện.

## Review Focus

1. **Khoảng sai số chạm đúng ngưỡng** (`max == 50` với lòi sau xe máy) → phải ra green, không phải yellow. Test ở Task 1.
2. **Chưa có vật tham chiếu** (chưa chạm 4 góc, không thấy thẻ) → không đo, nhưng kết quả vẫn có loại hàng, luật (E01–E03 yellow "chưa đo") và gợi ý xe theo kích thước điển hình. Test ở Task 7.
3. **Chạm điểm ngược thứ tự** (mép hàng nằm trong mép giá) → phần lòi bằng 0, không âm. Test ở Task 5.
4. **4 góc tham chiếu gần thẳng hàng** → `computeHomography` ném `MeasureError('degenerate_reference')`, giao diện báo "chạm lại 4 góc", không hiện NaN. Test ở Task 5.
5. **Server nhận diện lỗi hoặc trả loại hàng ngoài danh mục** → client trả `null` hoặc `'khac'`, giao diện chuyển sang chọn tay. Test ở Task 9.

---

## Thứ tự theo tuần (khớp mục 11 của spec)

- **Tuần 1:** Task 1–4, 7, 8 (chế độ nhập tay chạy được, có chế độ thực địa để ghi số đo).
- **Tuần 2:** Task 5, 6, 9.
- **Tuần 3:** Task 10 (đánh giá trên ảnh thật). Nút mở app nền tảng đã có ở Task 3/7.
- **Tuần 4:** Task 11.

## File Structure

```
cho-vua-app/
  package.json, vite.config.ts, tsconfig.json, index.html
  src/domain/types.ts          — kiểu dùng chung
  src/domain/interval.ts       — số học khoảng + đèn
  src/rules/limits.ts          — ngưỡng luật, bảng căn cứ + mức phạt
  src/rules/evaluate.ts        — evaluateLoad: 11 lỗi
  src/rules/predict.ts         — dự đoán khi chưa chất hàng lên xe máy
  src/data/vehicles.json       — bảng xe nền tảng (có nguồn, ngày đọc)
  src/data/items.json          — danh mục hàng MẪU (assumption)
  src/services/match.ts        — khớp xe + ước giá
  src/items/requirement.ts     — loại hàng → yêu cầu thùng xe, làm tròn về kích thước chuẩn
  src/measure/homography.ts    — DLT 4 điểm
  src/measure/measure.ts       — đo ảnh phía sau / bên hông → khoảng
  src/measure/aruco.ts         — tự tìm thẻ
  src/recognize/classify.ts    — client gọi /api/classify + parse
  src/record/ticket.ts         — nội dung phiếu
  src/record/log.ts            — lưu localStorage + xuất CSV
  src/ui/*.tsx                 — màn hình
  server/index.ts, server/classify.ts
  public/the-chuan-aruco.svg
  tests/** (Vitest)
traffic-data-research/src/cho_vua_eval.py
traffic-data-research/tests/test_cho_vua_eval.py
```

---

### Task 1: Khởi tạo app + số học khoảng và đèn

**Files:**
- Create: `cho-vua-app/` (Vite react-ts), `cho-vua-app/src/domain/types.ts`, `cho-vua-app/src/domain/interval.ts`
- Test: `cho-vua-app/tests/interval.test.ts`

**Interfaces:**
- Produces:
  - `type Light = 'green' | 'yellow' | 'red'`;
  - `interface Interval { min: number; max: number }`;
  - `iv(min: number, max: number): Interval`, dùng để sắp lại khi `min > max`;
  - `around(v: number, half: number): Interval`;
  - `add`, `sub(a: Interval, b: Interval): Interval`, với `sub = {min: a.min - b.max, max: a.max - b.min}`;
  - `scale(a: Interval, k: number): Interval`;
  - `clamp0(a: Interval): Interval`;
  - `lightVsMax(a: Interval | null, limit: number): Light`;
  - `lightFromFlag(v: boolean | null, bad: boolean): Light`;
  - `worst(ls: Light[]): Light`;
  - `fmtM(a: Interval): string`, ví dụ `"0,32–0,40 m"`.

- [ ] **Step 1: Tạo nhánh và scaffold**

```bash
git switch -c feat/cho-vua-demo
npm create vite@latest cho-vua-app -- --template react-ts
cd cho-vua-app && npm install && npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```
Thêm script `"test": "vitest run"` và cấu hình `test: { environment: 'jsdom' }` trong `vite.config.ts`.

- [ ] **Step 2: Viết test thất bại**

```ts
test('equal to limit is green', () => expect(lightVsMax(iv(40, 50), 50)).toBe('green'));
test('min above limit is red', () => expect(lightVsMax(iv(51, 60), 50)).toBe('red'));
test('straddling is yellow', () => expect(lightVsMax(iv(45, 55), 50)).toBe('yellow'));
test('missing is yellow', () => expect(lightVsMax(null, 50)).toBe('yellow'));
test('sub widens', () => expect(sub(iv(380, 420), iv(30, 50))).toEqual({ min: 330, max: 390 }));
test('clamp0', () => expect(clamp0(iv(-5, 10))).toEqual({ min: 0, max: 10 }));
test('flag', () => { expect(lightFromFlag(null, false)).toBe('yellow'); expect(lightFromFlag(false, false)).toBe('red'); expect(lightFromFlag(true, false)).toBe('green'); });
test('worst', () => expect(worst(['green', 'yellow', 'red'])).toBe('red'));
test('fmtM', () => expect(fmtM(iv(32, 40))).toBe('0,32–0,40 m'));
```

- [ ] **Step 2b: Chạy** `npm test`. Mong đợi: FAIL (chưa có module).
- [ ] **Step 3: Cài đặt** `types.ts`, `interval.ts` theo Interfaces.
- [ ] **Step 4: Chạy** `npm test`. Mong đợi: PASS.
- [ ] **Step 5: Commit**

```bash
git add cho-vua-app
git commit -m "feat(cho-vua): scaffold app and interval/light primitives"
```

---

### Task 2: Bộ luật 11 lỗi

**Files:**
- Create: `cho-vua-app/src/rules/limits.ts`, `cho-vua-app/src/rules/evaluate.ts`
- Create: `cho-vua-app/tests/helpers/fixtures.ts`, file dùng chung cho mọi test, được mở rộng ở các task sau:
  - `base(): LoadInput`: xe máy, mọi kích thước 0–5 cm, cao 100–110, cờ tốt, `weightKg iv(10,12)`, `vehicleMaxKg 150`, `looseMaterial false`;
  - `code(r, c): Finding`.
  - Task 3 thêm `pipe(a, b)`.
  - Task 4 thêm `box(l, w, h)` (trả `CargoRequirement`, mỗi chiều ±1 cm) và `item(id)`.
  - Task 7 thêm `state(partial)`, mặc định: `pre_load`, motorbike, HCM, 5 km, `thung_carton`, qty 1, mọi câu trả lời tốt, `weightKgManual null`, `vehicleMaxKg null`.
- Test: `cho-vua-app/tests/evaluate.test.ts`

**Interfaces:**
- Consumes: Task 1.
- Produces:

```ts
type VehicleKind = 'motorbike' | 'non_motorized' | 'motor_3_4_wheel';
type ErrorCode = 'E01'|'E02'|'E03'|'E04'|'E05'|'E06'|'E07'|'E08'|'E09'|'E10'|'E11';
interface LoadInput {
  vehicle: VehicleKind;
  sideLeftCm: Interval | null; sideRightCm: Interval | null;   // xe máy: so với mép giá; thô sơ: so với mép bánh
  rearCm: Interval | null; frontCm: Interval | null;           // xe máy: phía sau giá; thô sơ: so với thân xe
  heightCm: Interval | null;                                    // từ mặt đường
  bodyLengthCm: number | null;                                  // chỉ xe thô sơ
  extendsBeyondVehicle: boolean | null;
  plateAndLightsVisible: boolean | null; redMarker: boolean | null;
  lashingOk: boolean | null; carryingBulky: boolean | null; towing: boolean | null;
  looseMaterial: boolean; looseCovered: boolean | null;
  registered: boolean | null;                                   // dùng cho motor_3_4_wheel
  weightKg: Interval | null; vehicleMaxKg: number | null;
}
interface Finding { code: ErrorCode; light: Light; title: string; detail: string; legalBasis: string; fine: string }
function evaluateLoad(input: LoadInput): { findings: Finding[]; overall: Light }
```

**Bảng giá trị trong `limits.ts`** (sao chép nguyên văn):

| Mã | Tiêu đề | Căn cứ (xe máy / thô sơ) | Mức phạt người lái (xe máy / thô sơ) |
|---|---|---|---|
| E01 | Hàng lòi hai bên | Luật 36 Đ33.5 / Đ31.5 | 400.000–600.000đ (NĐ 168 Đ36.2.b) / như xe máy |
| E02 | Hàng lòi trước/sau | Luật 36 Đ33.5 / Đ31.5 | 400.000–600.000đ (NĐ 168 Đ36.2.b) / như xe máy |
| E03 | Hàng chất cao quá 2 m | Luật 36 Đ33.5 / không áp dụng | 400.000–600.000đ (NĐ 168 Đ36.2.b) / – |
| E04 | Hàng che biển số hoặc đèn | Luật 36 Đ47.1.d | 300.000–400.000đ (NĐ 168 Đ36.1.b) |
| E05 | Thiếu báo hiệu đỏ khi hàng lòi trước/sau | Luật 36 Đ47.1.e | 400.000–600.000đ (NĐ 168 Đ36.2.d) |
| E06 | Chằng buộc không chắc | Luật 36 Đ47.1.d | 300.000–400.000đ (NĐ 168 Đ36.1.a) |
| E07 | Mang, vác vật cồng kềnh | Luật 36 Đ33.3.đ, Đ33.4.a / Đ31.2 | 600.000–800.000đ (NĐ 168 Đ7.3.e); người ngồi sau 400.000–600.000đ (Đ12.5.a) / 150.000–250.000đ (Đ9.2.c); người ngồi sau xe đạp 200.000–250.000đ (Đ12.2.đ) |
| E08 | Kéo theo xe hoặc vật khác | Luật 36 Đ33.3.đ / Đ31.2 | 600.000–800.000đ (NĐ 168 Đ7.3.g) / 150.000–250.000đ (Đ9.2.c) |
| E09 | Xe sản xuất, lắp ráp trái quy định | Luật 36 Đ9.8 | Tịch thu phương tiện (NĐ 168 Đ14.4) |
| E10 | Hàng rời, vật liệu xây dựng rơi vãi | Luật 36 Đ47.1.đ | 400.000–600.000đ (NĐ 168 Đ36.2.c) |
| E11 | Chở vượt khối lượng cho phép | Luật 36 Đ47.1.c | 400.000–600.000đ (NĐ 168 Đ36.2.a) |

**Quy tắc riêng:**
- **E01:** lấy đèn xấu nhất của trái và phải.
- **E02, xe máy:** chỉ dùng `rearCm`, vì luật không đặt giới hạn phía trước cho xe máy.
- **E02, xe thô sơ:** lấy `worst` của `rearCm` và `frontCm` so với cùng một giới hạn.
- **E02, xe thô sơ:** nếu `bodyLengthCm == null` thì dùng giới hạn 100, và hạ đèn green xuống yellow kèm chi tiết "chưa biết chiều dài thân xe để kiểm quy tắc 1/3".
- **E03:** chỉ áp dụng cho xe máy.
- **E05:** chỉ xét khi `extendsBeyondVehicle !== false`.
  - `extendsBeyondVehicle == null` → yellow;
  - `true` và `redMarker !== true` → `lightFromFlag(redMarker, false)`.
- **E07:** tối đa yellow.
- **E09:** chỉ áp dụng cho `motor_3_4_wheel`, dùng `lightFromFlag(registered, false)`.
- **E10:** chỉ xét khi `looseMaterial` là true.
- **E11:** một trong hai giá trị `null` → yellow.
- **Lỗi không áp dụng:** không trả về.

- [ ] **Step 1: Viết test thất bại** (dùng `base()` trả một `LoadInput` mà mọi trường đều tốt):

```ts
test('motorbike rear 330–390 cm is red E02', () => expect(code(evaluateLoad({ ...base(), rearCm: iv(330, 390) }), 'E02').light).toBe('red'));
test('motorbike height 240 red E03', () => expect(code(evaluateLoad({ ...base(), heightCm: iv(235, 245) }), 'E03').light).toBe('red'));
test('non_motorized has no E03', () => expect(evaluateLoad({ ...base(), vehicle: 'non_motorized', heightCm: iv(300, 310) }).findings.find(f => f.code === 'E03')).toBeUndefined());
test('non_motorized side 45 red at 40 limit', () => expect(code(evaluateLoad({ ...base(), vehicle: 'non_motorized', sideLeftCm: iv(45, 48) }), 'E01').light).toBe('red'));
test('non_motorized 1/3 rule: body 210 → limit 70', () => expect(code(evaluateLoad({ ...base(), vehicle: 'non_motorized', bodyLengthCm: 210, rearCm: iv(75, 80) }), 'E02').light).toBe('red'));
test('non_motorized unknown body downgrades green', () => expect(code(evaluateLoad({ ...base(), vehicle: 'non_motorized', bodyLengthCm: null, rearCm: iv(10, 20) }), 'E02').light).toBe('yellow'));
test('carrying bulky caps at yellow', () => expect(code(evaluateLoad({ ...base(), carryingBulky: true }), 'E07').light).toBe('yellow'));
test('unregistered 3-4 wheel is red E09', () => expect(code(evaluateLoad({ ...base(), vehicle: 'motor_3_4_wheel', registered: false }), 'E09').light).toBe('red'));
test('overhang without red marker is red E05', () => expect(code(evaluateLoad({ ...base(), extendsBeyondVehicle: true, redMarker: false }), 'E05').light).toBe('red'));
test('overall is worst', () => expect(evaluateLoad({ ...base(), heightCm: iv(235, 245) }).overall).toBe('red'));
test('all good is green', () => expect(evaluateLoad(base()).overall).toBe('green'));
test('fine text for E07 motorbike', () => expect(code(evaluateLoad({ ...base(), carryingBulky: true }), 'E07').fine).toContain('600.000–800.000đ'));
```

- [ ] **Step 2: Chạy** `npm test -- evaluate`. Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** `limits.ts` (hằng số + bảng trên) và `evaluateLoad`.
- [ ] **Step 4: Chạy** `npm test`. Mong đợi: PASS.
- [ ] **Step 5: Commit** `git add cho-vua-app/src/rules cho-vua-app/tests/evaluate.test.ts && git commit -m "feat(cho-vua): rule engine for 11 cargo violations"`

---

### Task 3: Bảng xe nền tảng + khớp xe + ước giá

**Files:**
- Create: `cho-vua-app/src/data/vehicles.json`, `cho-vua-app/src/services/match.ts`
- Test: `cho-vua-app/tests/match.test.ts`

**Interfaces:**
- Produces:

```ts
interface PriceModel { baseVnd: number; baseKm: number; perKmVnd: number }
interface Vehicle { id: string; provider: 'lalamove'|'ahamove'|'grab'; name: string; city: 'HCM'|'HN';
  bedCm: { l: number; w: number; h: number }; maxKg: number | null; price: PriceModel | null;
  bookingUrl: string; source: string; accessed: string; note?: string }
interface CargoRequirement { lengthCm: Interval; widthCm: Interval; heightCm: Interval; weightKg: Interval | null }
interface VehicleOption { vehicle: Vehicle; estimateVnd: number | null; weightUnchecked: boolean }
function estimatePrice(p: PriceModel, km: number): number   // base nếu km ≤ baseKm, cộng perKm × (km − baseKm)
function matchVehicles(req: CargoRequirement, all: Vehicle[], city: 'HCM'|'HN', km: number, limit?: number /* =3 */): VehicleOption[]
```

**Khớp:**
- Hai chiều ngang (`max` của length, width) sắp giảm dần, so với `bedCm.l` và `bedCm.w` cũng sắp giảm dần.
- `heightCm.max ≤ bedCm.h`.
- Nếu cả hai có giá trị: `weightKg.max ≤ maxKg`. Nếu `weightKg` là null thì `weightUnchecked = true`.
- Sắp xếp theo `maxKg` tăng dần, sau đó theo diện tích thùng tăng dần.

**Dữ liệu `vehicles.json`** (accessed `2026-11-20`):
- `source` của Lalamove: `https://www.lalamove.com/vi-vn/bang-gia-giao-hang`; `bookingUrl` `https://www.lalamove.com/vi-vn/`.
- **Lalamove HCM** `bedCm` (l×w×h) / maxKg:
  - Xe máy 50×40×50 / 30; Xe máy có baga 60×50×60 / 50; Xe bán tải 140×150×50 / null;
  - Van 500kg 170×120×120 / 500; Van 750kg 190×120×130 / 750; Van 1000kg 210×130×130 / 1000;
  - Tải 500kg 190×140×140 / 500; Tải 750kg 250×140×140 / 750; Tải 1000kg 300×160×160 / 1000;
  - Tải 1250kg 310×160×160 / 1250; Tải 1500kg 320×160×170 / 1500; Tải 2000kg 400×170×170 / 2000;
  - Tải 2500kg 420×180×170 / 2500; Tải 3500kg 500×200×190 / 3500; Tải 5000kg 600×220×220 / 5000.
- **Lalamove HN:** Tải 1000kg 300×160×130 / 1000; Tải 2000kg 350×160×170 / 2000. Ghi `note: "bảng HN đọc qua tóm tắt, cần kiểm lại"`.
- **Grab HCM** (`bookingUrl` `https://www.grab.com/vn/express/`):
  - Ba gác 170×120×100 / 400, `source` trang Grab Ba gác, `note: "trang năm 2022"`;
  - Tải/Van 500kg 160×120×120 / 500, `source` trang GrabExpress Tải/Van.
- **Ahamove HCM** (`bookingUrl` `https://ahamove.com/`, `source` `https://ahamove.com/service/aha-truck/price`): Van 500kg dùng `bedCm` của Lalamove Van 500kg, `note: "kích thước mượn từ Lalamove — Ahamove không công bố"`, `price {baseVnd:124000, baseKm:2, perKmVnd:11600}`.
- Các xe khác: `price: null`.

- [ ] **Step 1: Viết test thất bại**

```ts
test('aha 5 km = 158800', () => expect(estimatePrice({ baseVnd: 124000, baseKm: 2, perKmVnd: 11600 }, 5)).toBe(158800));
test('pipe 390–400 cm in HCM → Lalamove Tải 2000kg first', () => expect(matchVehicles(pipe(390, 400), V, 'HCM', 5)[0].vehicle.name).toBe('Xe tải 2000kg'));
test('pipe up to 420 cm → Tải 2500kg first', () => expect(matchVehicles(pipe(380, 420), V, 'HCM', 5)[0].vehicle.name).toBe('Xe tải 2500kg'));
test('pipe 400 cm in HN → none', () => expect(matchVehicles(pipe(390, 400), V, 'HN', 5)).toEqual([]));
test('rotation: 140×60 fits bán tải 140×150', () => expect(matchVehicles({ lengthCm: iv(55, 60), widthCm: iv(135, 140), heightCm: iv(40, 45), weightKg: null }, V, 'HCM', 3).map(o => o.vehicle.name)).toContain('Xe bán tải'));
test('null weight flagged', () => expect(matchVehicles(pipe(390, 400), V, 'HCM', 5)[0].weightUnchecked).toBe(true));
```
Trong đó `pipe(a, b)` trả `{ lengthCm: iv(a, b), widthCm: iv(25, 30), heightCm: iv(25, 30), weightKg: null }`.

- [ ] **Step 2: Chạy** `npm test -- match`. Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** `vehicles.json` (đúng dữ liệu trên) và `match.ts`.
- [ ] **Step 4: Chạy** `npm test`. Mong đợi: PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(cho-vua): vehicle table, fit matching and price estimate"` (chỉ add `src/data/vehicles.json`, `src/services`, test).

---

### Task 4: Danh mục hàng mẫu, yêu cầu thùng xe, dự đoán khi chưa chất hàng

**Files:**
- Create: `cho-vua-app/src/data/items.json`, `cho-vua-app/src/items/requirement.ts`, `cho-vua-app/src/rules/predict.ts`
- Test: `cho-vua-app/tests/requirement.test.ts`, `cho-vua-app/tests/predict.test.ts`

**Interfaces:**
- Consumes: Task 1, 2, 3.
- Produces:

```ts
type ItemId = 'ong_nhua'|'thep_cay'|'ton_tam'|'tu_lanh'|'may_giat'|'nem'|'bao_xi_mang'|'cua_go'|'thung_carton'|'khac';
interface ItemCategory { id: ItemId; name: string; dimsCm: { l: Interval; w: Interval; h: Interval };
  standardLengthsCm: number[]; kgPerUnit: Interval | null; looseMaterial: boolean; assumption: true }
function snapLength(a: Interval, standards: number[], tolRel?: number /* 0.1 */): Interval
function requirementFor(item: ItemCategory, qty: number, measured: Partial<{ l: Interval; w: Interval; h: Interval }>): CargoRequirement
interface RackAssumption { widthCm: Interval; lengthCm: Interval; heightCm: Interval; forwardCm: Interval; assumption: true }
const DEFAULT_RACK: RackAssumption   // { widthCm: iv(30,50), lengthCm: iv(30,50), heightCm: iv(70,90), forwardCm: iv(0,30) }
function predictMotorbike(req: CargoRequirement, rack?: RackAssumption): Pick<LoadInput, 'sideLeftCm'|'sideRightCm'|'rearCm'|'heightCm'|'extendsBeyondVehicle'>
```

**`snapLength`:**
- Tìm các chuẩn `s` thỏa `a.min·(1−tol) ≤ s ≤ a.max·(1+tol)`.
- Đúng một chuẩn → trả `iv(s − 2, s + 2)`.
- Không có hoặc nhiều hơn một → trả nguyên `a`.

**`requirementFor`:**
- Số đo (`measured`) được ưu tiên hơn `dimsCm`.
- Sau đó áp `snapLength` cho chiều dài.
- `weightKg = scale(kgPerUnit, qty)`, hoặc `null`.
- Số lượng không làm đổi kích thước. Bản demo coi như hàng xếp thành một bó.

**`predictMotorbike`:** thử hai hướng xếp (dọc theo xe và ngang xe), lấy hướng có `worst` đèn tốt hơn qua `evaluateLoad`.
- **Hướng dọc:**
  - `side = clamp0(scale(sub(w, rack.widthCm), 0.5))`;
  - `rear = clamp0(sub(sub(l, rack.lengthCm), rack.forwardCm))`.
- **Hướng ngang:** đổi vai trò `l` và `w`.
- `heightCm = add(h, rack.heightCm)`.
- `extendsBeyondVehicle = rear.min > 0`.

**`items.json`:** mỗi mục có `assumption: true`, ví dụ `ong_nhua`: `l` 200–600, `w` 10–40, `h` 10–40, `standardLengthsCm` [400, 600], `kgPerUnit` null. Thêm nhãn "giả định — thay bằng danh mục cửa hàng thí điểm".

- [ ] **Step 1: Viết test thất bại**

```ts
test('snap 385–410 to 400', () => expect(snapLength(iv(385, 410), [400, 600])).toEqual({ min: 398, max: 402 }));
test('no snap when two candidates', () => expect(snapLength(iv(380, 620), [400, 600])).toEqual({ min: 380, max: 620 }));
test('measured overrides typical', () => expect(requirementFor(item('tu_lanh'), 1, { h: iv(158, 162) }).heightCm).toEqual({ min: 158, max: 162 }));
test('4 m pipe on motorbike is red', () => expect(evaluateLoad({ ...base(), ...predictMotorbike(pipe(398, 402)) }).overall).toBe('red'));
test('carton 40×30×30 on motorbike is green', () => expect(evaluateLoad({ ...base(), ...predictMotorbike(box(40, 30, 30)) }).overall).toBe('green'));
test('fridge 160 high + rack 70–90 is red E03', () => expect(code(evaluateLoad({ ...base(), ...predictMotorbike(box(60, 65, 160)) }), 'E03').light).toBe('red'));
```

- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** theo Interfaces.
- [ ] **Step 4: Chạy** `npm test`. Mong đợi: PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(cho-vua): sample item catalog, requirements and pre-load prediction"`

---

### Task 5: Đo từ ảnh bằng 4 góc vật tham chiếu

**Files:**
- Create: `cho-vua-app/src/measure/homography.ts`, `cho-vua-app/src/measure/measure.ts`
- Test: `cho-vua-app/tests/measure.test.ts`

**Interfaces:**
- Produces:

```ts
type Pt = { x: number; y: number };
class MeasureError extends Error { constructor(public reason: 'degenerate_reference' | 'missing_taps') }
function computeHomography(src: [Pt, Pt, Pt, Pt], dst: [Pt, Pt, Pt, Pt]): number[]   // 3×3 phẳng, h33 = 1, DLT 8×8
function applyH(H: number[], p: Pt): Pt
interface Reference { kind: 'aruco' | 'plate'; cornersPx: [Pt, Pt, Pt, Pt] /* TL,TR,BR,BL */; sizeCm: { w: number; h: number } }
interface RearTaps { rackLeft: Pt; rackRight: Pt; cargoLeft: Pt; cargoRight: Pt; cargoTop: Pt; ground: Pt }
interface SideTaps { rackRearEnd: Pt; cargoRearEnd: Pt }
function halfWidthCm(dCm: number, ref: Reference, cmPerPx: number): number
function measureRear(ref: Reference, t: RearTaps): { sideLeftCm: Interval; sideRightCm: Interval; heightCm: Interval }
function measureSide(ref: Reference, t: SideTaps): { rearCm: Interval }
```

**Công thức:**
- Ánh xạ mọi điểm chạm sang mặt phẳng tham chiếu (cm) bằng `applyH`.
- Khoảng cách theo trục x (bên trái, bên phải, phía sau), theo trục y (chiều cao).
- `cmPerPx = sizeCm.w / (độ dài trung bình cạnh trên và cạnh dưới, tính bằng px)`.
- `refSidePx` = trung bình 4 cạnh.
- `half = |d|·(CORNER_ERR_PX/refSidePx + OFF_PLANE_REL[kind]) + TAP_ERR_PX·√2·cmPerPx`.
- Phần lòi dùng `clamp0(around(d, half))`.
- Kiểm suy biến: diện tích tứ giác < 1% diện tích bounding box hoặc ma trận suy biến → `MeasureError('degenerate_reference')`.

- [ ] **Step 1: Viết test thất bại** (ảnh giả lập: 10 px/cm, không phối cảnh; biển 19×14 cm ở góc (500, 600) px):

```ts
const plate: Reference = { kind: 'plate', cornersPx: [{x:500,y:600},{x:690,y:600},{x:690,y:740},{x:500,y:740}], sizeCm: { w: 19, h: 14 } };
test('identity-scale homography maps 190 px to 19 cm', () => { const H = computeHomography(plate.cornersPx, [{x:0,y:0},{x:19,y:0},{x:19,y:14},{x:0,y:14}]); expect(applyH(H, {x:690,y:600}).x).toBeCloseTo(19, 6); });
test('perspective H round-trip within 1e-6', () => { /* tạo H đã biết, ánh xạ 4 điểm, tính lại H, so sánh */ });
test('left overhang 40 cm contains 40', () => { const r = measureRear(plate, taps({ rackLeftX: 400, cargoLeftX: 0 })); expect(r.sideLeftCm.min).toBeLessThanOrEqual(40); expect(r.sideLeftCm.max).toBeGreaterThanOrEqual(40); });
test('reversed taps give zero not negative', () => expect(measureRear(plate, taps({ rackLeftX: 400, cargoLeftX: 450 })).sideLeftCm.min).toBe(0));
test('plate wider than aruco uncertainty', () => expect(halfWidthCm(40, plate, 0.1)).toBeGreaterThan(halfWidthCm(40, { ...plate, kind: 'aruco' }, 0.1)));
test('collinear corners throw degenerate_reference', () => expect(() => measureRear({ ...plate, cornersPx: [{x:0,y:0},{x:10,y:0},{x:20,y:0},{x:30,y:0}] }, taps({}))).toThrow(MeasureError));
```

- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** DLT (giải hệ 8×8 bằng khử Gauss có chọn trụ) và các hàm đo.
- [ ] **Step 4: Chạy** `npm test`. Mong đợi: PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(cho-vua): homography-based measurement with uncertainty"`

---

### Task 6: Tự tìm thẻ ArUco + thẻ in

**Files:**
- Create: `cho-vua-app/src/measure/aruco.ts`, `cho-vua-app/public/the-chuan-aruco.svg`
- Test: `cho-vua-app/tests/aruco.test.ts`, `cho-vua-app/tests/helpers/drawMarker.ts`

**Interfaces:**
- Consumes: `Reference` (Task 5).
- Produces:
  - `detectMarker(img: { data: Uint8ClampedArray; width: number; height: number }): Reference | null`
  - Trả `kind: 'aruco'`, `sizeCm: { w: 15, h: 15 }`, góc theo thứ tự TL, TR, BR, BL. Thẻ dùng id 0, từ điển `ARUCO` của `js-aruco2`.

- [ ] **Step 1:** `npm install js-aruco2 && npm install -D pngjs`. Tạo `public/the-chuan-aruco.svg`:
  - viewBox tính theo mm, cạnh **150 mm** (ma trận bit lấy từ từ điển của thư viện);
  - dưới thẻ in dòng chữ "In đúng 15 cm — kiểm bằng thước trước khi dùng; dán đứng, song song biển số".
- [ ] **Step 2: Viết test thất bại.** Helper `drawMarker(id, cellPx, offset)` vẽ ma trận bit (có viền đen) vào buffer RGBA nền trắng.

```ts
test('detects synthetic marker corners within 2 px', () => { const img = drawMarker(0, 20, { x: 100, y: 80 }); const r = detectMarker(img)!; expect(r.cornersPx[0].x).toBeCloseTo(100, -0.5); /* ±2 px cho cả 4 góc */ });
test('blank image returns null', () => expect(detectMarker(blank(640, 480))).toBeNull());
```

- [ ] **Step 3: Chạy.** Mong đợi: FAIL.
- [ ] **Step 4: Cài đặt** `detectMarker`, sắp lại thứ tự góc theo TL, TR, BR, BL. Nếu `js-aruco2` không cài hoặc không dùng được: dừng task, báo lại. Chế độ chạm 4 góc thủ công (Task 7) vẫn đủ cho demo.
- [ ] **Step 5: Chạy** `npm test`. Mong đợi: PASS.
- [ ] **Step 6: Commit** `git commit -m "feat(cho-vua): ArUco auto-detection and printable reference card"`

---

### Task 7: Giao diện luồng kiểm tra (nhập tay và chụp ảnh)

**Files:**
- Create: `cho-vua-app/src/ui/App.tsx`, `src/ui/StepVehicle.tsx`, `src/ui/StepItem.tsx`, `src/ui/StepMeasure.tsx`, `src/ui/PhotoTapper.tsx`, `src/ui/StepChecklist.tsx`, `src/ui/Result.tsx`, `src/ui/check.ts`
- Modify: `cho-vua-app/src/main.tsx`
- Test: `cho-vua-app/tests/ui.test.tsx`, `cho-vua-app/tests/check.test.ts`

**Interfaces:**
- Consumes: Task 2–6.
- Produces:

```ts
interface CheckState { stage: 'pre_load' | 'loaded'; vehicle: VehicleKind; city: 'HCM'|'HN'; km: number;
  itemId: ItemId; qty: number; measured: Partial<{ l: Interval; w: Interval; h: Interval }>;
  photo: { rear?: ReturnType<typeof measureRear>; side?: ReturnType<typeof measureSide>; refKind?: 'aruco'|'plate' };
  answers: Pick<LoadInput, 'plateAndLightsVisible'|'redMarker'|'lashingOk'|'carryingBulky'|'towing'|'looseCovered'|'registered'|'bodyLengthCm'>;
  weightKgManual: Interval | null; vehicleMaxKg: number | null }
interface CheckResult { item: ItemCategory; sizeText: string; sizeSource: 'nhập tay'|'thẻ chuẩn'|'biển số'|'kích thước điển hình (giả định)';
  findings: Finding[]; overall: Light; options: VehicleOption[] }
function runCheck(s: CheckState): CheckResult   // thuần, test được
```

**`runCheck`:**
- `stage = 'pre_load'` và xe máy → dùng `predictMotorbike`.
- `loaded` → lấy số đo ảnh (ưu tiên), rồi đến số nhập tay.
- Không có số đo → E01–E03 yellow, chi tiết "chưa đo".
- Luôn tính `options` từ `requirementFor`.

**Màn hình:**
1. Tình huống (lúc bán / xe đã chất) và loại xe.
2. Loại hàng + số lượng.
3. Kích thước: nhập tay cm, hoặc **Chụp ảnh**. `PhotoTapper` gồm:
   - chọn ảnh qua input `capture`;
   - thử `detectMarker`; không có thì hướng dẫn **chạm 4 góc biển số** (TL→TR→BR→BL);
   - chạm lần lượt các điểm trong `RearTaps` / `SideTaps`, có chữ hướng dẫn từng điểm;
   - nút "Chạm lại".
   - **Xe thô sơ:** chữ hướng dẫn đổi "mép giá" thành "mép bánh xe"; thêm ô nhập tay "phần lòi phía trước" và "chiều dài thân xe" (vào `frontCm` và `bodyLengthCm`).
4. Checklist: mỗi câu có 3 nút Có / Không / Không rõ.
5. Kết quả: 4 khối.
   - **Loại hàng.**
   - **Kích cỡ:** `fmtM` + nguồn.
   - **Luật:** từng `Finding`, gồm đèn, tiêu đề, chi tiết, căn cứ, mức phạt.
   - **Xe phù hợp:** tên, kích thước thùng, giá ước tính hoặc "xem giá trên app", nút **Mở {provider}** (`bookingUrl`, `target=_blank`).
   - Nút **Đo kỹ hơn** quay về bước 3.
   - Không có xe khớp → "Không có xe phù hợp trong bảng cho {city}".
   - Danh mục và giá chở hàng giả định có nhãn "giả định".

- [ ] **Step 1: Viết test thất bại**

```ts
// ống 395–400 cm được làm tròn về 398–402 cm (chuẩn 400). Cận trên 402 > thùng 400 cm của Tải 2000kg → chọn Tải 2500kg (theo cận trên).
test('runCheck: 4 m pipe pre_load motorbike → red and Tải 2500kg', () => { const r = runCheck(state({ itemId: 'ong_nhua', measured: { l: iv(395, 400) } })); expect(r.overall).toBe('red'); expect(r.options[0].vehicle.name).toBe('Xe tải 2500kg'); });
test('runCheck: loaded without measurement → E01–E03 yellow and still options', () => { const r = runCheck(state({ stage: 'loaded' })); expect(['E01','E02','E03'].map(c => r.findings.find(f => f.code === c)!.light)).toEqual(['yellow','yellow','yellow']); expect(r.options.length).toBeGreaterThan(0); });
test('UI shows red light and open-app button', async () => { render(<App initial={state({ itemId: 'ong_nhua', measured: { l: iv(395, 400) } })} startAt="result" />); expect(screen.getByText(/Mở lalamove/i)).toBeInTheDocument(); expect(screen.getAllByLabelText('đèn đỏ').length).toBeGreaterThan(0); });
test('UI never shows forbidden wording', () => { render(<App initial={state({})} startAt="result" />); expect(document.body.textContent).not.toMatch(/thực thi luật|chứng nhận an toàn/i); });
```

- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** `check.ts` rồi các màn hình. Đèn hiển thị là chấm màu kèm `aria-label` "đèn xanh / đèn vàng / đèn đỏ". Bố cục một cột, chạy ở bề ngang 360 px.
- [ ] **Step 4: Chạy** `npm test`. Mong đợi: PASS.
- [ ] **Step 5: Kiểm bằng mắt:** `npm run dev`, mở trên trình duyệt ở cỡ 375×812. Đi hết luồng nhập tay với ống 4 m, và luồng chụp ảnh với một ảnh có biển số.
- [ ] **Step 6: Commit** `git commit -m "feat(cho-vua): check flow UI with manual and photo measurement"`

---

### Task 8: Phiếu QR, nhật ký và chế độ thực địa

**Files:**
- Create: `cho-vua-app/src/record/ticket.ts`, `cho-vua-app/src/record/log.ts`, `cho-vua-app/src/ui/Ticket.tsx`, `cho-vua-app/src/ui/FieldMode.tsx`
- Modify: `cho-vua-app/src/ui/Result.tsx`, `cho-vua-app/src/ui/App.tsx`
- Test: `cho-vua-app/tests/record.test.ts`

**Interfaces:**
- Consumes: `CheckState`, `CheckResult` (Task 7).
- Produces:

```ts
interface CheckRecord { id: string; at: string; vehicle: VehicleKind; itemId: ItemId; refKind: 'aruco'|'plate'|'manual'|'none';
  app: { sideLeft?: Interval; sideRight?: Interval; rear?: Interval; height?: Interval }; overall: Light;
  tape?: { sideLeft?: number; sideRight?: number; rear?: number; height?: number }; note?: string }
function ticketText(r: CheckResult, at: Date): string
function toRecord(s: CheckState, r: CheckResult, at: Date): CheckRecord
function saveRecord(rec: CheckRecord, store?: Storage): void          // key 'chovua.checks.v1'
function loadRecords(store?: Storage): CheckRecord[]
function toCsv(recs: CheckRecord[]): string
```

**`ticketText`:** gồm loại hàng, kích cỡ, đèn tổng, các lỗi đỏ/vàng, thời điểm, và câu miễn trừ đúng như Global Constraints.

**Header CSV** (đúng thứ tự):
```
id,at,vehicle,item,ref_kind,overall,side_left_min,side_left_max,side_right_min,side_right_max,rear_min,rear_max,height_min,height_max,tape_side_left,tape_side_right,tape_rear,tape_height,note
```

**Chế độ thực địa:** danh sách bản ghi; mỗi bản ghi có ô nhập số đo thước (cm) cho 4 kích thước, cùng nút **Xuất CSV** (tải file `chovua_checks.csv`). Không lưu ảnh.

- [ ] **Step 1: Viết test thất bại**

```ts
test('ticket has disclaimer', () => expect(ticketText(result(), new Date('2026-11-20T08:00:00Z'))).toContain('không thay thế việc kiểm tra, xử lý của cơ quan chức năng'));
test('csv header exact', () => expect(toCsv([]).split('\n')[0]).toBe('id,at,vehicle,item,ref_kind,overall,side_left_min,side_left_max,side_right_min,side_right_max,rear_min,rear_max,height_min,height_max,tape_side_left,tape_side_right,tape_rear,tape_height,note'));
test('save/load round-trip', () => { const s = memStorage(); saveRecord(rec(), s); expect(loadRecords(s)).toHaveLength(1); });
test('note with comma is quoted', () => expect(toCsv([rec({ note: 'a,b' })])).toContain('"a,b"'));
```

- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** (`npm install qrcode`; QR mã hóa `ticketText`).
- [ ] **Step 4: Chạy** `npm test`. Mong đợi: PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(cho-vua): ticket QR, local log and field mode CSV export"`

---

### Task 9: Nhận diện loại hàng bằng mô hình đọc ảnh (server)

**Files:**
- Create: `cho-vua-app/server/index.ts`, `cho-vua-app/server/classify.ts`, `cho-vua-app/src/recognize/classify.ts`
- Modify: `cho-vua-app/vite.config.ts` (proxy `/api` → `http://localhost:8787`), `cho-vua-app/package.json` (script `"server": "tsx server/index.ts"`), `src/ui/StepItem.tsx`, `src/ui/StepChecklist.tsx`
- Test: `cho-vua-app/tests/classify.test.ts`

**Trước khi viết code, load skill `claude-api`** để chọn model và cách gọi API có ảnh. Không chọn model từ trí nhớ.

**Interfaces:**
- Consumes: `ItemId`, `VehicleKind`.
- Produces:

```ts
interface ClassifyResult { itemId: ItemId; confidence: 'high'|'medium'|'low'; alternatives: ItemId[];
  vehicle: VehicleKind | null; plateAndLightsVisible: boolean | null; carryingBulky: boolean | null; looksSelfMade: boolean | null }
function parseClassify(raw: unknown): ClassifyResult        // dùng chung client và server
async function classifyImage(file: Blob, fetchFn?: typeof fetch): Promise<ClassifyResult | null>   // thu nhỏ cạnh dài 1024 px; lỗi → null
```

**`parseClassify`:**
- `itemId` không có trong danh sách → `'khac'` với `confidence 'low'`.
- `alternatives` lọc theo danh sách, tối đa 3 mục.
- Trường boolean sai kiểu → `null`.

**Server:**
- `POST /api/classify` nhận `{ imageBase64, mediaType }`.
- Prompt yêu cầu trả JSON đúng các trường trên, `itemId` chỉ lấy trong danh sách `ItemId`.
- Không lưu ảnh, không log ảnh.
- Thiếu `ANTHROPIC_API_KEY` → trả 503.

**Giao diện:**
- `StepItem` gợi ý loại hàng và 3 lựa chọn thay thế; người dùng xác nhận hoặc đổi.
- Kết quả nhận diện điền sẵn các câu checklist, người dùng vẫn sửa được.
- `looksSelfMade` true → hỏi "Xe có đăng ký và biển số không?".

- [ ] **Step 1: Viết test thất bại**

```ts
test('unknown item → khac low', () => expect(parseClassify({ itemId: 'tivi', confidence: 'high', alternatives: [] })).toMatchObject({ itemId: 'khac', confidence: 'low' }));
test('bad boolean → null', () => expect(parseClassify({ itemId: 'nem', confidence: 'high', alternatives: [], plateAndLightsVisible: 'yes' }).plateAndLightsVisible).toBeNull());
test('server down → null', async () => expect(await classifyImage(new Blob(['x']), async () => new Response('', { status: 503 }))).toBeNull());
test('network error → null', async () => expect(await classifyImage(new Blob(['x']), async () => { throw new Error('offline'); })).toBeNull());
```

- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** parse, client và server (`npm install -D tsx`; SDK theo skill `claude-api`).
- [ ] **Step 4: Chạy** `npm test`. Mong đợi: PASS. Sau đó chạy thử `ANTHROPIC_API_KEY=... npm run server` cùng `npm run dev` với 3 ảnh (ống nhựa, tủ lạnh, thùng carton); ghi kết quả vào phần mô tả commit.
- [ ] **Step 5: Commit** `git commit -m "feat(cho-vua): image item recognition via server with manual fallback"`

---

### Task 10: Đánh giá sai số trên ảnh thực địa (Python)

**Files:**
- Create: `traffic-data-research/src/cho_vua_eval.py`
- Test: `traffic-data-research/tests/test_cho_vua_eval.py`

**Interfaces:**
- Consumes: CSV của Task 8.
- Produces:
  - `evaluate(rows: list[dict]) -> dict[str, dict]`, khóa theo `ref_kind`, mỗi giá trị có:
    - `n`;
    - `mae_cm`: theo từng kích thước có cả số đo thước và số đo app;
    - `coverage`: tỷ lệ số đo thước nằm trong khoảng app;
    - `yellow_rate`;
    - `false_green`: số kích thước mà app ra xanh theo ngưỡng (bên 30, sau 50, cao 200, chỉ xe máy) trong khi số đo thước vượt ngưỡng.
  - CLI: `python -X utf8 traffic-data-research/src/cho_vua_eval.py <csv> --out <dir>`, ghi `eval.json` và `eval_vi.md`.

**Quy tắc:**
- Giá trị điểm của app là trung điểm của khoảng.
- Bỏ qua kích thước thiếu dữ liệu, và đếm số dòng bị bỏ.

- [ ] **Step 1: Viết test thất bại** (`unittest`, theo kiểu `tests/test_revalidation.py`):

```python
def test_false_green_counted(self):
    rows = [row(ref_kind='plate', rear_min=40, rear_max=48, tape_rear=55)]
    self.assertEqual(evaluate(rows)['plate']['false_green'], 1)
def test_coverage_and_mae(self):
    rows = [row(ref_kind='aruco', side_left_min=35, side_left_max=45, tape_side_left=42)]
    r = evaluate(rows)['aruco']; self.assertEqual(r['coverage'], 1.0); self.assertAlmostEqual(r['mae_cm'], 2.0)
def test_missing_tape_skipped(self):
    self.assertEqual(evaluate([row(ref_kind='plate', rear_min=10, rear_max=20)])['plate']['skipped'], 1)
```

- [ ] **Step 2: Chạy** `python -m unittest traffic-data-research/tests/test_cho_vua_eval.py -v`. Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** bằng thư viện chuẩn (`csv`, `json`, `statistics`). Không thêm phụ thuộc mới.
- [ ] **Step 4: Chạy lại.** Mong đợi: PASS.
- [ ] **Step 5: Khi có CSV thực địa:**
  - chạy CLI vào `traffic-data-research/reports/track2_2026_11_20/eval_<ngày>/`;
  - cập nhật `TAP_ERR_PX`, `OFF_PLANE_REL` trong `measure.ts` sao cho `coverage ≥ 0.9` trên **nửa mẫu dùng để chỉnh** (tách theo xe hoặc ngày);
  - báo kết quả trên **nửa còn lại**;
  - nếu `false_green` > 0 trên nửa còn lại với chế độ `plate`: ghi lại và cân nhắc chỉ giữ chế độ thẻ (mục 12 của spec).
- [ ] **Step 6: Commit** `git commit -m "feat(cho-vua): field measurement evaluation script"`

---

### Task 11: Chạy trên điện thoại và kịch bản demo

**Files:**
- Create: `cho-vua-app/README.md` (cách chạy, giới hạn, dữ liệu giả định), `cho-vua-app/DEMO_vi.md` (kịch bản quay video)

- [ ] **Step 1:** `npm run build`. Mong đợi: build thành công, không lỗi TypeScript. `npm test`. Mong đợi: PASS hết.
- [ ] **Step 2:** `npm run dev -- --host` và `npm run server`. Mở `http://<IP máy>:5173` trên điện thoại cùng Wi-Fi. Kiểm tra chụp ảnh qua input `capture` mở được camera.
- [ ] **Step 3:** Viết `DEMO_vi.md` với 5 cảnh, mỗi cảnh ghi kết quả mong đợi:
  1. Ống 4 m lúc bán, xe máy → 🔴 E02, gợi ý Tải 2500kg (thùng 400 cm của Tải 2000kg quá sát với ống 4 m cộng sai số), mở Lalamove.
  2. Thùng carton nhỏ trên xe máy, chụp có biển số → 🟢, nhắc chằng buộc.
  3. Tủ lạnh đứng trên xe máy → 🔴 E03.
  4. Hàng che biển số → 🔴 E04.
  5. Xe ba bánh có máy, không có đăng ký → 🔴 E09, gợi ý xe thay thế.
- [ ] **Step 4:** Đi qua 5 cảnh trên điện thoại thật. Ghi vào `DEMO_vi.md` cảnh nào lệch mong đợi.
- [ ] **Step 5: Commit** `git commit -m "docs(cho-vua): run guide and demo script"`

---

## Ngoài phạm vi bản demo

- Bộ quy định theo tỉnh (mục 6, mức "Địa phương" của spec).
- Tự phát hiện biển số bằng mô hình; bản demo dùng chạm 4 góc.
- Khoanh vùng hàng bằng SAM 2; bản demo dùng chạm điểm.
- Mô hình ước độ sâu dùng để kiểm chéo.
- Dự đoán trước cho xe thô sơ.
- Đăng nhập, đồng bộ máy chủ, thống kê nhiều cửa hàng.
- Gọi API đặt xe thật; bản demo chỉ mở trang hoặc app nền tảng.
