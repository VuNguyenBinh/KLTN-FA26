# STATUS — Chốt ngày 2026-11-02

## ĐÃ XONG (Claude dựng & kiểm chứng trên máy)
- Hạ tầng: Docker (engine 29.8.1 chạy), Git, Ollama + model `qwen2.5:7b`. ✓
- 2 bộ benchmark: gốc (104 bài) + **hint-free** (104 bài, đã xóa gợi ý). ✓
- Metadata 104 bài (độ khó + loại lỗ hổng) + **mẫu 40 bài phân tầng** (seed=42). ✓
- Công thức flag = `FLAG{sha256(TEN_BAI)}`, **đã xác minh khớp pipeline gốc**. ✓
- **Harness build tự động** (`harness/build_target.py`): tự vá tương thích Docker 2026, build, chạy, dò port, health-check (HTTP-probe, không tin healthcheck cũ), ghi `targets.csv`. Cô lập mỗi variant bằng `-p <bench>-<variant>`. ✓
- **CẢ 80 target build + chạy được** (40 gốc + 40 hint-free, HTTP 200, flag khớp). ✓
- Script phân tích + vẽ biểu đồ (`analysis/analyze.py`): bảng solve-rate theo nhánh/độ khó/loại + bảng hiệu ứng memorization (gốc vs hint-free) + **Bảng 3b detection vs capture tự động cho nhánh B** (bóc `detected=` từ cột notes). Đã test. ✓
- **NHÁNH B (auto, không AI) — HOÀN TẤT 40/40 bài gốc.** ✓ (xem kết quả bên dưới)
- Tài liệu hướng dẫn: PLAN, SETUP, WORKFLOW, ARM_B, RUNBOOK, OUTLINE. ✓
- **Nháp bài báo** (trong `paper/draft_*.md`): Methodology (mục 3), Results/Discussion nhánh B (mục 4–5, chừa số A/C), Introduction + Related Work (mục 1–2, nguồn đã xác minh), Abstract + Conclusion (khung, chừa số A/C). ✓
- Đã commit + push lên GitHub (`VuNguyenBinh/KLTN-FA26`), `results.csv` version-controlled. ✓

## NHÁP BÀI BÁO — trạng thái từng mục
| Mục | File | Trạng thái |
|---|---|---|
| 0 Abstract | `paper/draft_abstract_conclusion.md` | khung, chừa số A/C |
| 1 Introduction | `paper/draft_intro_relatedwork.md` | đủ |
| 2 Related Work | `paper/draft_intro_relatedwork.md` | đủ; nguồn đã xác minh (PentestGPT, Fang 2024, AutoPenBench, CVE-Bench, HackSynth, survey 2607.02605, CTFusion, AWE) |
| 3 Methodology | `paper/draft_methodology.md` | đủ |
| 4–5 Results/Discussion | `paper/draft_results_armB.md` | nhánh B xong; chừa `[[…]]` cho A/C |
| 6 Threats to Validity | `paper/OUTLINE.md` §6 | đủ (có caveat detection-heuristic) |
| 7 Conclusion | `paper/draft_abstract_conclusion.md` | khung, chừa số A/C |

> Khi nhóm chạy xong nhánh A/C và điền `results.csv`, chạy `analyze.py` sẽ tự sinh Bảng 1 (so 3 nhánh) và Bảng 4 (memorization) để điền các chỗ `[[…]]`. Nguồn trích "gián tiếp qua survey" (CTFusion, AWE, PentestEval) nên mở bản gốc xác nhận trước khi nộp chính thức.

## KẾT QUẢ NHÁNH B (baseline tự-động-không-AI, 40 bài gốc, budget 30′/bài)
Hai chỉ số (quan trọng — phân biệt *phát hiện* với *bắt flag*):

| Chỉ số | Kết quả |
|---|---|
| **Bắt được flag** (tiêu chí giải) | **2/40 = 5%** — XBEN-071, XBEN-083, đều SQLi (sqlmap dump DB) |
| **Phát hiện lỗ hổng** (tool có báo vuln) | **22/40 = 55%** |

Theo độ khó (bắt flag / phát hiện): easy 14.3% / 64%; medium 0% / 56%; hard 0% / 37.5%.
Theo loại (phát hiện nổi bật): SSTI 6/6=100% phát hiện nhưng 0 bắt; XSS 8/10 phát hiện, 0 bắt; IDOR 0/6 phát hiện; SQLi 2/2 bắt flag.

**Phát hiện cốt lõi:** khoảng cách lớn *phát hiện (55%) ≫ bắt flag (5%)* — scanner nhận ra **lớp** lỗ hổng nhưng gần như không tự xâu chuỗi nhiều bước để lấy đúng flag (trừ SQLi nhờ sqlmap tự dump DB). Đây là lập luận để chỉ ra giá trị tiềm năng của nhánh C (AI): lấp khoảng trống *phát hiện → khai thác*.

> Ghi chú tái lập: lần chạy đầu cho 2/40 nhưng có **lỗi đo** (nuclei coi `localhost` là chết, dalfox crash cờ `--no-spinner`, exploiter chỉ quét URL gốc). Đã sửa (dùng `127.0.0.1`, `dalfox -S`, nạp path từ ffuf cho exploiter, giới hạn ngân sách mỗi bước, thêm chỉ số detection) và chạy lại — 2/40 là **con số thật** sau khi sửa. Chi tiết: `docs/ARM_B.md` mục "Kết quả".

## ĐANG CHẠY NỀN
- (không có) — `uv sync` cài PentestGPT (nhánh C) đã xong trước đó.

## CẦN NHÓM LÀM / QUYẾT (không tự động được)
1. **Nhánh A (manual):** cài **Burp Suite Community**, kiểm thử tay 40 bài gốc, bấm giờ, ghi `results.csv` (`arm=A_manual`). Xem `docs/RUNBOOK.md` Bước 2.
2. **Nhánh C (AI):** chạy PentestGPT legacy + Ollama (`qwen2.5:7b`), **mỗi bài trên bản gốc VÀ hint-free**, ghi tokens/manual_interventions/llm_refused. Xem RUNBOOK Bước 4. (C2 API đã hoãn — chốt C1 local trước.)
3. **(tùy chọn)** API key cho C2 nếu muốn chạy nhánh API: khuyến nghị **DeepSeek** hoặc **Qwen/DashScope** (rẻ, ít từ chối hơn). Đặt vào `PentestGPT/.env`.

> Lưu ý: Claude KHÔNG thể đóng vai nhánh A (sẽ biến nó thành "có AI"). Nhánh A/C cần người thật.

## PHÂN CÔNG TUẦN 3 (viết)
- Chạy `analyze.py` → bảng/biểu đồ. Viết theo `paper/OUTLINE.md`. Dựng slide. Tập bảo vệ.
- Có thể nhờ Claude viết nháp phần Results/Discussion cho nhánh B từ số liệu trên.

## GHI CHÚ QUAN TRỌNG
- Benchmark XBOW **đã bão hòa** (AI ~100% vì học thuộc). Ta xử lý bằng **so sánh gốc vs hint-free** → đóng góp "đo hiệu ứng memorization". Phải nêu trong *Threats to Validity*.
- Mọi bản vá tương thích Docker ghi ở `harness/patches.log` — **không đổi lỗ hổng/flag**, chỉ để build được trên Docker 2026. Khai báo trong bài báo.
- Chỉ **21/40 bài** có bộ khai thác no-AI chuyên biệt (sqlmap/dalfox/SSTImap); 19/40 chỉ nuclei+ffuf → solve-rate nhánh B ở IDOR/logic/deserialization bị giới hạn bởi *công cụ*, không phải bởi "tự động hóa" nói chung. Đã nêu trong *Threats to Validity*.
- "SCI 2027": bài hội nghị index ở **CPCI (Web of Science)** hoặc **Scopus**, không phải SCIE/SCI. Kiểm tra proceedings hội nghị đã thực sự index ở kỳ trước.
