# STATUS — Chốt ngày 2026-11-01

## ĐÃ XONG (Claude dựng & kiểm chứng trên máy)
- Hạ tầng: Docker (engine 29.8.1 chạy), Git, Ollama + model `qwen2.5:7b`. ✓
- 2 bộ benchmark: gốc (104 bài) + **hint-free** (104 bài, đã xóa gợi ý). ✓
- Metadata 104 bài (độ khó + loại lỗ hổng) + **mẫu 40 bài phân tầng** (seed=42). ✓
- Công thức flag = `FLAG{sha256(TEN_BAI)}`, **đã xác minh khớp pipeline gốc**. ✓
- **Harness build tự động** (`harness/build_target.py`, `build_all.py`): tự vá tương thích, build, chạy, dò port, health-check, ghi `targets.csv`. ✓
- 2 bài đã chạy thật (XBEN-001, XBEN-002), web HTTP 200, flag khớp. ✓
- Script phân tích + vẽ biểu đồ (`analysis/analyze.py`), đã test. ✓
- Tài liệu: PLAN, SETUP, WORKFLOW, OUTLINE (bài báo). ✓

## ĐANG CHẠY NỀN
- `uv sync` cài PentestGPT (nhánh C) với Python 3.12.

## CẦN NHÓM LÀM / QUYẾT (không tự động được)
1. **API key cho nhánh C2** — mua/đăng ký 1 key (khuyến nghị **DeepSeek** hoặc **Qwen/DashScope**: rẻ, ít từ chối tác vụ pentest hơn OpenAI/Anthropic). Đặt vào `PentestGPT/.env`.
2. **Chốt chế độ PentestGPT:** legacy (trợ lý, người chạy lệnh — khuyến nghị, đo được manual_interventions) hay agent (tự động). Mặc định dùng **legacy**.
3. **Chạy build cả mẫu** (qua đêm, ~vài giờ): `python build_all.py` và `python build_all.py --variant hintfree --repo "..\benchmarks\xbow-hint-free\benchmarks"`.

## PHÂN CÔNG TUẦN 2 (chạy thí nghiệm)
- **Người 1 — Nhánh A (manual):** Burp + tay, 40 bài gốc. Bấm giờ, ghi `results.csv`.
- **Người 2 — Nhánh B (auto no-AI):** cài nuclei/ffuf/sqlmap, pipeline cố định, 40 bài gốc.
- **Người 3 — Nhánh C (AI):** PentestGPT legacy. Chạy C1 (Ollama) + C2 (API), **mỗi cái trên bản gốc VÀ hint-free**. Ghi tokens, manual_interventions, llm_refused.

## PHÂN CÔNG TUẦN 3 (viết)
- Chạy `analyze.py` → bảng/biểu đồ. Viết theo `paper/OUTLINE.md`. Dựng slide. Tập bảo vệ.

## GHI CHÚ QUAN TRỌNG
- Benchmark XBOW **đã bão hòa** (AI ~100% vì học thuộc). Ta xử lý bằng **so sánh gốc vs hint-free** → biến thành đóng góp "đo hiệu ứng memorization". Phải nêu trong *Threats to Validity*.
- Mọi bản vá tương thích Docker ghi ở `harness/patches.log` — **không đổi lỗ hổng/flag**, chỉ để build được trên Docker 2026. Khai báo trong bài báo.
- "SCI 2027": bài hội nghị index ở **CPCI (Web of Science)** hoặc **Scopus**, không phải SCIE/SCI. Kiểm tra proceedings hội nghị đã thực sự index ở kỳ trước.
- Trước khi chạy batch thật: `git checkout -- benchmarks/` ở mỗi repo để về pristine, xóa `harness/patches.log` cũ → log sạch cho tái lập.
