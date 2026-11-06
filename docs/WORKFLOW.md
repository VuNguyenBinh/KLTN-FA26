# Quy trình chạy thí nghiệm (ĐÃ KIỂM CHỨNG trên máy)

> 📊 **Sơ đồ tổng thể (flowchart):** `docs/workflow_image.md`.


Trạng thái hạ tầng (tính đến 2026-11-01, Claude đã dựng & test):
- Docker Desktop: chạy (engine 29.8.1). ✓
- Git, Ollama: đã cài. Model `qwen2.5:7b` (4.7GB) đã pull. ✓
- Benchmark gốc: `project/benchmarks/validation-benchmarks` (104 bài). ✓
- Benchmark hint-free: `project/benchmarks/xbow-hint-free` (104 bài, đã xóa gợi ý). ✓
- Metadata + mẫu 40 bài: `project/benchmarks/metadata.csv`, `sample.csv`. ✓
- **Bài mẫu XBEN-001-24 đã build+chạy, web HTTP 200, flag khớp SHA ground-truth.** ✓
- PentestGPT: đã clone ở `project/harness/PentestGPT`. (chưa cài deps)

---

## 1. Build target (tự động, đã có harness)

Harness tự áp các **bản vá tương thích** (ghi log vào `harness/patches.log`):
- `mysql:5.7.15` → `mysql:5.7` (image 2016 hỏng với Docker mới).
- Debian **bullseye/buster EOL** → mirror `archive.debian.org` + bỏ check Valid-Until.
- `expose: "A:B"` (cú pháp cũ) → `expose: "A"`.

Các bản vá này **không đổi lỗ hổng hay flag** — chỉ sửa để build được trên Docker 2026. Phải khai báo trong mục *Threats to Validity* của bài báo (file `patches.log` là bằng chứng tái lập).

```powershell
cd "D:\Bình\KLTN new\project\harness"

# build 1 bài (bản gốc)
python build_target.py XBEN-001-24

# build cả mẫu 40 bài (chạy qua đêm, bài lỗi vẫn tiếp tục)
python build_all.py

# build cả mẫu bản HINT-FREE cho nhánh AI
python build_all.py --variant hintfree --repo "..\benchmarks\xbow-hint-free\benchmarks"
```

Mỗi bài build xong được ghi một dòng vào `project/benchmarks/targets.csv`, gồm trạng thái (`running` hoặc `build_failed`), địa chỉ `url` (dạng `http://localhost:PORT`) và `ground_truth_flag`. Người kiểm thử mở `url` trên trình duyệt để làm bài; một bài tính là giải được khi lấy ra đúng chuỗi `ground_truth_flag`.

> **Lưu ý về cổng:** mỗi lần `docker compose up` cấp một cổng host ngẫu nhiên, nên hãy luôn đọc URL từ `targets.csv` thay vì ghi cứng trong lệnh.

---

## 2. Ba nhánh — chạy thế nào

### Nhánh Truyền thống — người + công cụ (Người 1)
Mở `url` của bài → **người kết hợp công cụ truyền thống không-AI**: trình duyệt + Burp Suite + scanner/bộ khai thác (nuclei/ffuf/sqlmap/dalfox/SSTImap) + suy luận. Bấm giờ. Khi tìm được flag, so với `targets.csv`. Ghi vào `results.csv` (`arm=A_manual`): solved, time_minutes, num_steps, notes. **Chỉ cấm AI/LLM.**

### Công cụ tự động — Automated no-AI (Người 2)
Pipeline cố định (cùng cấu hình mọi bài), ví dụ:
```powershell
# nuclei: quét template lỗ hổng
nuclei -u <url> -o logs\B_<bench>.txt
# ffuf: fuzz path/param
# sqlmap: với bài nghi SQLi
```
Cài qua: `winget install ProjectDiscovery.nuclei` ; sqlmap/ffuf tải binary. Ghi solved theo việc pipeline có lộ flag/đường dẫn tới flag không. **Không có LLM.**

### Nhánh AI — AI-assisted (Người 3) — dùng PentestGPT legacy
Cùng một công cụ, chỉ đổi model:
```powershell
cd "D:\Bình\KLTN new\project\harness\PentestGPT"
# cài 1 lần:
pip install -e .            # hoặc: uv sync  (repo dùng uv)
copy .env.example .env

# --- AI local: LOCAL Ollama ---
#   trong .env đặt:  OLLAMA_BASE_URL=http://localhost:11434/v1
#   bảo đảm Ollama đang chạy + đã có qwen2.5:7b
pentestgpt-legacy --list-models        # xem model khả dụng
pentestgpt-legacy                      # chọn model ollama/qwen2.5:7b

# --- AI API: API thương mại ---
#   trong .env đặt key: OPENAI_API_KEY / DEEPSEEK_API_KEY / QWEN_API_KEY ...
#   (DeepSeek/Qwen cloud thường ít bị từ chối tác vụ pentest hơn OpenAI/Anthropic)
pentestgpt-legacy --smoke-test         # kiểm tra model trả lời
```
PentestGPT ở chế độ *legacy* hoạt động như một trợ lý: nó suy luận rồi đề xuất lệnh, còn người vận hành chạy lệnh và dán kết quả trở lại cho nó. Chính vòng lặp này cho phép đo hai chỉ số quan trọng của nhánh AI — `manual_interventions` (số lần người phải can thiệp) và `llm_refused` (mô hình có từ chối tác vụ hay không) — và cũng là lý do nhánh AI được xem là "có AI hỗ trợ" chứ không phải AI tự trị.

Nhánh AI cần chạy trên **cả bản gốc lẫn bản hint-free** của mỗi bài, để từ chênh lệch kết quả giữa hai bản mà đo mức độ mô hình "học thuộc" lời giải.

---

## 3. Chấm điểm & phân tích
Nhập liệu vào `project/results/results.csv` (mẫu: `results_template.csv`). Rồi:
```powershell
cd "D:\Bình\KLTN new\project\analysis"
python analyze.py ..\results\results.csv
```
→ Bảng tổng hợp + biểu đồ trong `paper/figures/`.

---

## 4. Dọn dẹp
```powershell
# hạ 1 bài:
cd <bench_dir>; docker compose down
# hạ tất cả + xóa image để lấy lại ổ đĩa:
docker ps -q | % { docker stop $_ }
docker system prune -af
```
