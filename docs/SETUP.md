# Hướng dẫn cài đặt — các bước làm tay (Tuần 1)

Hãy làm lần lượt theo đúng thứ tự dưới đây. Sau mỗi bước đều có một lệnh để tự kiểm tra xem bước đó đã xong chưa trước khi chuyển sang bước kế tiếp.

## 0. Phần mềm nền
1. **Docker Desktop** — đã cài sẵn. Mở nó, chờ icon chuyển **xanh** (Engine running).
   - Kiểm tra (PowerShell): `docker run --rm hello-world` → thấy "Hello from Docker!".
2. **Git** — tải: https://git-scm.com/download/win → cài mặc định.
   - Kiểm tra: `git --version`.
3. **Ollama** (cho nhánh AI local) — tải: https://ollama.com/download → cài.
   - Kiểm tra: `ollama --version`.
   - Tải model: `ollama pull qwen2.5:7b` (hoặc `llama3.1:8b`). Model ~5GB.
   - Chạy thử: `ollama run qwen2.5:7b "hello"`.

## 1. Lấy benchmark XBOW
```powershell
cd "D:\Bình\KLTN new\project\benchmarks"
git clone https://github.com/xbow-engineering/validation-benchmarks.git
cd validation-benchmarks
```
Build thử 1 bài (ví dụ XBEN-001-24):
```powershell
cd benchmarks\XBEN-001-24   # tên thư mục có thể khác, xem bằng: ls benchmarks
# đọc Makefile/README trong bài để biết lệnh build; thường:
make build
make run     # dựng web target, mở trên cổng được in ra
```
→ Mở trình duyệt vào địa chỉ đó, xác nhận web chạy. Flag ẩn trong bài.

## 2. Cài công cụ nhánh AI (PentestGPT)
```powershell
cd "D:\Bình\KLTN new\project\harness"
git clone https://github.com/GreyDGL/PentestGPT.git
cd PentestGPT
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```
- **AI local (local):** cấu hình PentestGPT trỏ tới Ollama (xem README của repo, phần local/Ollama; endpoint mặc định `http://localhost:11434`).
- **AI API (API):** nếu nhóm có API key thương mại, đặt biến môi trường theo README. **Lưu ý:** tác vụ pentest có thể bị bộ lọc an toàn từ chối — ghi lại mỗi lần bị từ chối vào cột `llm_refused`, đó là dữ liệu có ích.

## 3. Công cụ tự động (automated, no AI)
Chọn 1 pipeline cố định, ví dụ kết hợp: `nuclei` (quét template lỗ hổng) + `sqlmap` (SQLi tự động) + `ffuf` (fuzzing path). Cấu hình cố định, cùng timeout cho mọi bài. Không có LLM trong nhánh này.

## 4. Chạy pilot
Chạy **3 bài** đủ cả 3 nhánh, nhập tay vào bản sao của `project/results/results_template.csv` → đổi tên thành `results.csv`. Rồi:
```powershell
cd "D:\Bình\KLTN new\project\analysis"
python analyze.py ..\results\results.csv
```
→ Ra bảng và biểu đồ trong `paper/figures/`. Chạy được đến đây nghĩa là toàn bộ quy trình đã thông suốt; sang Tuần 2 chỉ còn việc nhân rộng cho đủ 40 bài.

---
## Báo lại cho tôi sau khi làm xong các bước trên
Chỉ cần nhắn: **Docker xanh chưa / git+ollama cài chưa / clone benchmark được chưa / build thử 1 bài có lên web không.** Có lỗi ở đâu dán log, tôi gỡ.
