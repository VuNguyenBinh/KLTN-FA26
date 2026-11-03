# STATUS — Trung tâm điều phối (cập nhật 2026-11-03)

> **File này là nguồn sự thật dùng chung.** Bộ nhớ của Claude là **cục bộ từng máy** — Claude trên thiết bị khác KHÔNG có nó. Vì vậy mọi ngữ cảnh + ràng buộc + cách tiếp tục được ghi ở đây và trên GitHub (`VuNguyenBinh/KLTN-FA26`). **Claude trên MỌI thiết bị đọc file này + `task_C1.md` + `report_A.md` trước khi làm.**

---

## 0. ĐỌC TRƯỚC — dành cho Claude (bất kỳ thiết bị nào)

**Đề tài:** KLTN (FPT) — *Comparative Study of AI-assisted and Traditional Web App Penetration Testing*. Thí nghiệm có kiểm soát trên **40 bài CTF web (XBOW)**, chấm exact-match flag, budget **30′/bài**.

**Cấu trúc 3 nhánh (đã chốt):**
1. **Truyền thống** = con người + công cụ, KHÔNG AI. Hai tầng, giữ nhãn riêng: tầng người `A_manual`, tầng công cụ `B_auto` (trần tự-động-hoá).
2. **AI local** = PentestGPT + Ollama `qwen2.5:7b` → nhãn `C_ai_local`.
3. **AI API** = PentestGPT + model thương mại → nhãn `C_ai_api` (hoãn).

**⛔ RÀNG BUỘC CỨNG cho Claude (không được vi phạm — đây là lý do kết quả có giá trị):**
- Claude **KHÔNG đóng vai người giải** nhánh Truyền thống, **KHÔNG giải hộ CTF**. Nhánh người do **người độc lập ngoài nhóm** làm; người trong nhóm chỉ giám sát/bấm giờ/chấm.
- Nhánh AI: Claude **chỉ hướng dẫn tooling/đếm chỉ số/ghi dữ liệu**, **KHÔNG mách** endpoint/tham số/payload/kỹ thuật khai thác. Prompt grey-box: chỉ cho *lớp* lỗ hổng (parity với công cụ tự động), không cho cách giải.
- **Đếm can thiệp:** `manual_interventions` = chỉ **redirect** (chỉnh hướng khi AI đi sai); `exec` (chạy lệnh AI đề xuất) ghi trong `notes`, không tính. Lằn ranh cứng: lỡ mách kỹ thuật → bài đó `solved=0` + đánh dấu.
- **Giữ dữ liệu**: không xoá nhãn `B_auto`/bài nào. Không bịa số nhánh nào.
- **Chống rò rỉ:** ai đã *thấy lời giải* một bài (giải hoặc giám sát nhánh Truyền thống) thì **không** chạy nhánh AI bài đó (biết trước = thiên lệch).
- **Git:** commit + push sau mỗi bài/đổi lớn để các máy đồng bộ. Luôn `git pull` đầu phiên.

**Cách tiếp tục nhanh:** xem §2 (từng nhánh) + §3 (môi trường/lệnh).

---

## 1. TRẠNG THÁI SỐNG (standing)

| Nhánh | n đã chạy | solve | Nguồn chi tiết |
|---|---|---|---|
| Truyền thống — người (`A_manual`) | **3/40** | **100%** (3/3) | `docs/report_A.md` |
| Truyền thống — công cụ (`B_auto`) | 40/40 | 5% (2/40) · phát hiện 27,5% | §5 + `docs/ARM_B.md` |
| AI local (`C_ai_local`) | **4/12** | **0%** (0/4) | `docs/task_C1.md` + `docs/report_C.md` |
| AI API (`C_ai_api`) | 0 | — | hoãn |

**Câu chuyện đang hình thành:** người 3/3 · công cụ 5% · AI-local 0/4 → ủng hộ "trong khung này, con người lấp được khoảng cách *phát hiện→khai thác* mà cả tự-động lẫn AI-local chưa lấp". (Lập luận đầy đủ: đầu `docs/report_C.md`.)

---

## 2. CÁCH TIẾP TỤC TỪNG NHÁNH

### 2a. Nhánh Truyền thống — phần người (manual)
- Người giải độc lập + Burp. Giao thức + bảng 40 bài + nhật ký: **`docs/report_A.md`**.
- Còn 37/40. Ưu tiên **12 bài [C]** (có cặp với AI) + các bài công cụ thất bại.
- Claude làm gì: bật target, đưa URL + *lớp* lỗ hổng cho người giải, chấm flag, ghi `results.csv` (`arm=A_manual`) + điền `report_A.md`. **KHÔNG gợi ý cách giải.**

### 2b. Nhánh AI local (C1)
- Giao thức đầy đủ: **`docs/arm_C_protocol.md`**. Tiến độ + kết quả: **`docs/task_C1.md`**.
- Đã xong 4/12 (061, 064, 080, 037 — tất cả solved=0). Bài **còn sạch với người điều phối đã giám sát A trên 005/006/032**: **093, 011, 041, 014, 083** + hint-free (061/064 + 2 bài).
- Quy trình 1 phiên: §3 (lệnh khởi động) → prompt grey-box (lớp) → vòng `discuss`↔`curl.exe` → đếm redirect/exec → chốt `solved` → ghi `results.csv` (`C_ai_local`) + `report_C.md` + `task_C1.md`.

### 2c. Nhánh AI API (C2) — hoãn
- Cùng PentestGPT, đổi `--reasoning-model`/`--parsing-model` sang model API + key trong `PentestGPT/.env`. Nhãn `C_ai_api`. Khuyến nghị DeepSeek/Qwen (ít từ chối). `llm_refused` là một kết quả.

---

## 3. MÔI TRƯỜNG & LỆNH (máy Windows chính — máy khác chỉnh đường dẫn)

**Đường dẫn công cụ (prepend vào PATH khi cần):**
- Docker bin: `C:\Users\Admin\AppData\Local\Programs\DockerDesktop\resources\bin` — exe mở app: `...\DockerDesktop\Docker Desktop.exe`
- Ollama: `C:\Users\Admin\AppData\Local\Programs\Ollama`
- Git: `C:\Program Files\Git\cmd`
- Burp: `C:\Users\Admin\AppData\Local\Programs\BurpSuiteCommunity\BurpSuiteCommunity.exe`

**Kiểm tra sẵn sàng:** `docker info --format '{{.ServerVersion}}'` (29.8.1) · `ollama list` (thấy `qwen2.5:7b`).

**Bật 1 target (lấy URL):**
```powershell
cd "D:\Bình\KLTN new\project\harness"
python build_target.py <XBEN-xxx-24>          # gốc
python build_target.py <XBEN-xxx-24> --variant hintfree --repo "..\benchmarks\xbow-hint-free\benchmarks"
```
**Khởi động PentestGPT (nhánh AI local) — PowerShell riêng:**
```powershell
cd "D:\Bình\KLTN new\project\harness\PentestGPT"
$env:PYTHONIOENCODING="utf-8"
.\.venv\Scripts\python.exe -m pentestgpt_legacy.main --reasoning-model "ollama:qwen2.5:7b" --parsing-model "ollama:qwen2.5:7b" --base-url "http://localhost:11434/v1"
```
**Chấm flag:** `Import-Csv project\benchmarks\targets.csv | ? {$_.benchmark_id -eq "<ID>" -and $_.variant -eq "original"} | select ground_truth_flag`
**Phân tích:** `cd project\analysis; python analyze.py ..\results\results.csv`
**Hạ target:** `docker ps -q --filter "name=<xben-xxx>" | % { docker stop $_ }`

**Cột `results.csv`:** `benchmark_id,difficulty,vuln_category,arm,variant,run_id,solved,flag_found,time_minutes,num_steps,tokens_used,manual_interventions,llm_refused,notes`

---

## 4. CHỈ MỤC TÀI LIỆU
| File | Nội dung |
|---|---|
| `docs/STATUS.md` | **File này** — trung tâm điều phối, trạng thái sống, ràng buộc |
| `docs/PLAN.md` | Kế hoạch, RQ, đóng góp cốt lõi, định nghĩa 3 nhánh |
| `docs/arm_C_protocol.md` | Giao thức nhánh AI (bộ 12 bài, prompt, đếm can thiệp) |
| `docs/task_C1.md` | Tiến độ + kết quả nhánh AI local (bảng từng phiên) |
| `docs/report_C.md` | Nhật ký từng lượt nhánh AI + khung lập luận kết quả âm |
| `docs/report_A.md` | Giao thức + bảng 40 bài + nhật ký nhánh người |
| `docs/ARM_B.md` | Tầng công cụ tự động (pipeline cố định, kết quả) |
| `docs/RUNBOOK.md` | Hướng dẫn lệnh từng bước |
| `docs/WORKFLOW.md`, `SETUP.md` | Quy trình + cài đặt |
| `paper/THESIS_FULL.md` | **Bản thảo thesis hoàn chỉnh (bản chốt, 3 nhánh)** |
| `paper/draft_*.md`, `OUTLINE.md` | Nháp từng mục (đã có banner ánh xạ 3 nhánh) |
| `project/results/results.csv` | **Dữ liệu** (version-controlled) |

---

## 5. KẾT QUẢ CÔNG CỤ TỰ ĐỘNG (`B_auto`, 40/40, budget 30′)
| Chỉ số | Kết quả |
|---|---|
| **Bắt flag** | **2/40 = 5%** — XBEN-071, 083 (SQLi, sqlmap dump) |
| **Phát hiện** | **11/40 = 27,5%** |

Theo độ khó (bắt/phát hiện): easy 14,3%/50,0% · medium 0%/11,1% · hard 0%/25,0%.
Theo loại (phát hiện): XSS 8/10=80% (dalfox POC, 0 bắt) · SQLi 2/2 (phát hiện+bắt) · CVE 1/1 · còn lại 0 (SSTI 0/6, IDOR 0/6…).
**Cốt lõi:** phát hiện (27,5%) ≫ bắt flag (5%). Chi tiết + lịch sử sửa lỗi đo (55%→27,5%): `docs/ARM_B.md`.

---

## 6. NHÁP BÀI BÁO
Bản chốt: **`paper/THESIS_FULL.md`** (6 chương, 3 nhánh, chừa `[[…]]` cho số người/AI). Nháp nguồn: `paper/draft_*.md`. Khi có đủ số nhánh người + AI → `analyze.py` sinh Bảng 1 (3 nhánh) + Bảng 4 (memorization) để điền.

---

## 7. GHI CHÚ QUAN TRỌNG
- **Benchmark XBOW bão hoà** (AI ~100% vì học thuộc) → xử lý bằng cặp gốc/hint-free, đo *Δ memorization*. Nêu trong *Threats to Validity*.
- **Bản vá Docker** ghi `harness/patches.log` — không đổi lỗ hổng/flag. Khai báo trong bài.
- Chỉ **21/40 bài** có exploiter chuyên biệt (19/40 chỉ nuclei+ffuf) → yếu kém công cụ ở IDOR/logic một phần do *công cụ*, không phải "tự động hoá" nói chung.
- **Cần làm tiếp:** nhánh người (37 bài) + nhánh AI (8 bài + hint-free) + (tuỳ) AI API. Đây là phần **con người thật**, Claude không thay được.
