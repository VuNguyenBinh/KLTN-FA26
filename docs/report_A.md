# REPORT nhánh Truyền thống (người) — Nhật ký kiểm thử thủ công (tái lập được)

> Ghi lại nhánh Truyền thống (người) (con người làm tay, **KHÔNG AI**) để tái lập và để người giám sát chép lại quá trình. Người giải là **người độc lập ngoài nhóm, không biết trước lỗ hổng**; người trong nhóm chỉ **giám sát + bấm giờ + chấm**, tuyệt đối không gợi ý. Bắt đầu: 2026-11-03.

---

## 0. Nguyên tắc giữ nhánh Truyền thống (người) sạch (đọc trước)
- **Người giải:** độc lập, ngoài nhóm, chưa từng xem bài. Chỉ dùng **Burp + trình duyệt + suy luận**. KHÔNG mở AI/LLM, KHÔNG chạy scanner tự động (sqlmap/nuclei/dalfox…).
- **Được cung cấp:** URL target + **lớp lỗ hổng** của bài (parity với công cụ tự động — B cũng biết lớp). KHÔNG cho endpoint, tham số, payload hay bất cứ gì về cách giải.
- **Người giám sát:** quan sát câm, bấm giờ 30′, đếm số request/lần thử, chấm flag. **Không phản ứng, không gợi ý.** Nếu lỡ buột miệng → ghi rõ "có can thiệp" và đánh dấu bài đó kém tin cậy (trung thực).
- **Giới hạn:** 30 phút/bài. Hết giờ chưa ra → `solved=0` (vẫn là số liệu hợp lệ).

## 1. Thiết lập mỗi bài
1. Bật target (nhờ harness): `python build_target.py <ID>` trong `project/harness` → lấy URL `http://localhost:PORT`.
2. Mở Burp Suite Community → **Temporary project** → **Use Burp defaults** → Start.
3. Tab **Proxy** → Intercept **off** → **Open Browser** → vào URL target.
4. **Bấm giờ bắt đầu.**
5. Chấm flag khi người giải báo có `FLAG{...}`:
   ```powershell
   Set-Location "D:\Bình\KLTN new\project\benchmarks"
   Import-Csv targets.csv | Where-Object { $_.benchmark_id -eq "<ID>" -and $_.variant -eq "original" } | Select-Object ground_truth_flag
   ```
   Khớp đúng → `solved=1`.

## 2. Mẫu nhật ký từng bài (giám sát điền mốc thời gian)
```
### Bài <n> — <ID> (<loại>, <độ khó>) — <ngày>
- Cấp cho người giải: URL + lớp = <loại>
- Mốc thời gian:
  [00:30] <người giải làm gì> → <kết quả họ thấy>
  [mm:ss] ...
  [mm:ss] *lần đầu nghi ra lỗ hổng*
  [mm:ss] *khai thác thành công*
  [mm:ss] lấy được FLAG{...}
- Kết quả: solved=<0|1> · time=<phút> · num_steps=<số request> · can thiệp của giám sát=<không/﻿có: mô tả>
- Ghi chú: <người giải kẹt đâu, thử hướng nào>
```
> Nếu không kịp ghi mốc chi tiết thì tối thiểu ghi: solved, phút, số bước, một câu quan sát.

## 3. Bảng theo dõi 40 bài (điền dần)
`[C]` = bài cũng nằm trong bộ 12 của nhánh AI (cho cặp so sánh người↔AI).

| # | Bài | Khó | Loại | [C] | solved | phút | steps |
|---|---|---|---|---|---|---|---|
| 1 | XBEN-005-24 | easy | idor | C | **1** | **10** | **7** |
| 2 | XBEN-006-24 | easy | idor | C | **1** | **30** | **15** |
| 3 | XBEN-032-24 | easy | xxe | C | | | |
| 4 | XBEN-034-24 | easy | cve | | | | |
| 5 | XBEN-037-24 | easy | command_injection | C | | | |
| 6 | XBEN-041-24 | easy | arbitrary_file_upload | C | | | |
| 7 | XBEN-047-24 | easy | xss | | **1** | **15** | **5** |
| 8 | XBEN-061-24 | easy | lfi | C | | | |
| 9 | XBEN-062-24 | easy | xss | | | | |
| 10 | XBEN-064-24 | easy | xss | C | | | |
| 11 | XBEN-071-24 | easy | sqli | | | | |
| 12 | XBEN-073-24 | easy | command_injection | | | | |
| 13 | XBEN-074-24 | easy | xss | | | | |
| 14 | XBEN-083-24 | easy | sqli | C | | | |
| 15 | XBEN-002-24 | medium | idor | | | | |
| 16 | XBEN-003-24 | medium | idor | | | | |
| 17 | XBEN-008-24 | medium | xss | | | | |
| 18 | XBEN-011-24 | medium | xss | C | | | |
| 19 | XBEN-012-24 | medium | xss | | | | |
| 20 | XBEN-014-24 | medium | privilege_escalation | C | | | |
| 21 | XBEN-023-24 | medium | ssti | | | | |
| 22 | XBEN-025-24 | medium | ssti | | | | |
| 23 | XBEN-027-24 | medium | idor | | | | |
| 24 | XBEN-029-24 | medium | blind_sqli | | | | |
| 25 | XBEN-054-24 | medium | privilege_escalation | | | | |
| 26 | XBEN-075-24 | medium | insecure_deserialization | | | | |
| 27 | XBEN-080-24 | medium | ssti | C | | | |
| 28 | XBEN-086-24 | medium | ssti | | | | |
| 29 | XBEN-092-24 | medium | insecure_deserialization | | | | |
| 30 | XBEN-099-24 | medium | idor | | | | |
| 31 | XBEN-100-24 | medium | nosqli | | | | |
| 32 | XBEN-104-24 | medium | ssti | | | | |
| 33 | XBEN-010-24 | hard | xss | | | | |
| 34 | XBEN-018-24 | hard | xss | | | | |
| 35 | XBEN-057-24 | hard | insecure_deserialization | | | | |
| 36 | XBEN-066-24 | hard | smuggling_desync | | | | |
| 37 | XBEN-087-24 | hard | xss | | | | |
| 38 | XBEN-088-24 | hard | default_credentials | | | | |
| 39 | XBEN-093-24 | hard | ssti | C | | | |
| 40 | XBEN-101-24 | hard | crypto | | | | |

**Tiến độ: 3/40.** Ưu tiên nếu thiếu thời gian: 12 bài `[C]` trước (để đủ cặp người↔AI), rồi tới phần còn lại (cho so sánh người↔công cụ đủ 40).

## 4. Ghi vào results.csv
Mỗi bài một dòng (`arm=A_manual`; cột tokens/manual_interventions/llm_refused để trống):
```
<ID>,<khó>,<loại>,A_manual,original,1,<solved>,<flag nếu có>,<phút>,<steps>,,,,"manual Burp; <ghi chú>"
```
Đọc số cho Claude để ghi giúp cũng được.

---

## Nhật ký các bài đã chạy

### Bài 1 — XBEN-047-24 (XSS, easy) — 2026-11-03
- Cấp cho người giải: URL `http://localhost:56798` + lớp = XSS.
- Kết quả: **solved=1** · time=**15′** · num_steps=**5** · can thiệp của giám sát=**không**.
- Flag khớp `ground_truth_flag` (verify exact-match).
- Ghi chú: người giải độc lập ngoài nhóm, không AI, không scanner. (Lần này chưa ghi mốc thời gian chi tiết — từ bài sau nên ghi theo mẫu mục 2.)
- Đối chiếu: công cụ tự động *phát hiện* XSS (dalfox `[POC]`) nhưng **không bắt flag**; người giải bắt được trong 15′ → minh hoạ con người lấp khoảng cách phát-hiện→khai-thác.

### Bài 2 — XBEN-005-24 (IDOR, easy) — 2026-11-03
- Cấp cho người giải: URL `http://localhost:49686` + lớp = IDOR.
- Kết quả: **solved=1** · time=**10′** · num_steps=**7** · can thiệp của giám sát=**không**.
- Flag khớp `ground_truth_flag` (exact-match).
- Ghi chú: người giải độc lập, không AI, không scanner. (Chưa ghi mốc thời gian chi tiết.)
- Đối chiếu đắt giá: IDOR là lớp **công cụ tự động mù hoàn toàn (0/6 phát hiện)** — scanner tĩnh không nhận ra lỗi logic chủ-sở-hữu/tài-nguyên; người giải tìm ra và bắt flag trong 10′. Đây là bằng chứng mạnh cho "con người thấy được thứ tự-động không thấy".

### Bài 3 — XBEN-006-24 (IDOR, easy) — 2026-11-03
- Cấp cho người giải: URL `http://localhost:64215` + lớp = IDOR.
- Kết quả: **solved=1** · time=**30′ (sát trần)** · num_steps=**15** · can thiệp của giám sát=**không**.
- Flag khớp `ground_truth_flag` (exact-match).
- Ghi chú: cũng là IDOR (công cụ tự động mù), nhưng khó hơn 005 rõ rệt — mất trọn 30′ và 15 request mới ra, so với 10′/7 request ở 005. Cho thấy ngay trong cùng một lớp lỗ hổng, độ khó khai thác dao động mạnh; người vẫn bắt được nhưng sát trần thời gian.
