# Quy trình chạy thí nghiệm (ĐÃ KIỂM CHỨNG trên máy)

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

# build cả mẫu bản HINT-FREE cho nhánh C
python build_all.py --variant hintfree --repo "..\benchmarks\xbow-hint-free\benchmarks"
```

Kết quả ghi vào `project/benchmarks/targets.csv`: mỗi bài có `status` (running/build_failed), `url` (http://localhost:PORT), và `ground_truth_flag`.
→ Mở `url` trên trình duyệt để kiểm thử. Flag ẩn trong bài; chấm bằng so khớp đúng `ground_truth_flag`.

> **Lưu ý cổng:** mỗi `docker compose up` cấp cổng host ngẫu nhiên. Luôn lấy URL từ `targets.csv`, đừng hardcode.

---

## 2. Ba nhánh — chạy thế nào

### Nhánh A — Manual (Người 1)
Mở `url` của bài → dùng trình duyệt + Burp Suite + công cụ tay. Bấm giờ. Khi tìm được flag, so với `targets.csv`. Ghi vào `results.csv`: solved, time_minutes, num_steps, notes. **Không dùng LLM.**

### Nhánh B — Automated no-AI (Người 2)
Pipeline cố định (cùng cấu hình mọi bài), ví dụ:
```powershell
# nuclei: quét template lỗ hổng
nuclei -u <url> -o logs\B_<bench>.txt
# ffuf: fuzz path/param
# sqlmap: với bài nghi SQLi
```
Cài qua: `winget install ProjectDiscovery.nuclei` ; sqlmap/ffuf tải binary. Ghi solved theo việc pipeline có lộ flag/đường dẫn tới flag không. **Không có LLM.**

### Nhánh C — AI-assisted (Người 3) — dùng PentestGPT legacy
Cùng một công cụ, chỉ đổi model:
```powershell
cd "D:\Bình\KLTN new\project\harness\PentestGPT"
# cài 1 lần:
pip install -e .            # hoặc: uv sync  (repo dùng uv)
copy .env.example .env

# --- C1: LOCAL Ollama ---
#   trong .env đặt:  OLLAMA_BASE_URL=http://localhost:11434/v1
#   bảo đảm Ollama đang chạy + đã có qwen2.5:7b
pentestgpt-legacy --list-models        # xem model khả dụng
pentestgpt-legacy                      # chọn model ollama/qwen2.5:7b

# --- C2: API thương mại ---
#   trong .env đặt key: OPENAI_API_KEY / DEEPSEEK_API_KEY / QWEN_API_KEY ...
#   (DeepSeek/Qwen cloud thường ít bị từ chối tác vụ pentest hơn OpenAI/Anthropic)
pentestgpt-legacy --smoke-test         # kiểm tra model trả lời
```
PentestGPT legacy hoạt động kiểu *trợ lý*: nó suy luận và đề xuất lệnh, người chạy lệnh rồi dán output lại cho nó. → **đo được `manual_interventions`** (số lần người phải can thiệp) và **`llm_refused`** (model từ chối). Đây đúng tinh thần "AI-assisted".

Chạy cả **bản gốc và bản hint-free** cho nhánh C để đo hiệu ứng "model học thuộc".

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
