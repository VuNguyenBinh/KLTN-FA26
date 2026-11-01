# RUNBOOK — Hướng dẫn từng bước, từng lệnh (có chú thích terminal)

## Quy ước terminal
- **Tất cả lệnh chạy trong PowerShell trên Windows.** Mở bằng: VS Code → menu **Terminal → New Terminal** (mặc định là PowerShell), hoặc gõ "PowerShell" ở Start Menu.
- Ký hiệu 🖥️ **PS [thư mục]** = mở PowerShell và `cd` vào thư mục đó trước khi chạy.
- ⚠️ **Terminal bị chiếm:** khi một lệnh mở **công cụ tương tác** (PentestGPT, sqlmap hỏi đáp…), terminal đó bị giữ cho tới khi thoát tool. Muốn làm việc khác → **mở terminal MỚI** (VS Code cho phép nhiều terminal: bấm dấu **+** ở panel Terminal).
- 3 người chạy 3 nhánh song song → **mỗi người 1 terminal riêng**.

---

## BƯỚC 0 — Chuẩn bị (làm 1 lần mỗi khi mở terminal mới)

🖥️ **PS (thư mục nào cũng được)** — nạp PATH cho git/ollama/ffuf (docker & python đã có sẵn):
```powershell
$env:PATH += ";C:\Program Files\Git\cmd;C:\Users\Admin\AppData\Local\Programs\Ollama;C:\Users\Admin\AppData\Local\Programs\DockerDesktop\resources\bin"
```
> Mẹo: để khỏi gõ lại mỗi lần, dán dòng trên vào file `$PROFILE` (chạy `notepad $PROFILE`).

Kiểm tra sẵn sàng:
```powershell
docker info --format '{{.ServerVersion}}'    # phải in ra số phiên bản (Docker đang chạy)
ollama list                                  # phải thấy qwen2.5:7b
```
Nếu `docker info` lỗi → mở **Docker Desktop**, chờ icon xanh.
Nếu `ollama list` lỗi → chạy: `Start-Process "C:\Users\Admin\AppData\Local\Programs\Ollama\ollama app.exe"` rồi chờ 5 giây.

---

## BƯỚC 1 — Bật 1 target (chung cho MỌI nhánh)

🖥️ **PS [D:\Bình\KLTN new\project\harness]**

Bản gốc:
```powershell
python build_target.py XBEN-023-24
```
Bản hint-free (chỉ dùng cho nhánh C):
```powershell
python build_target.py XBEN-023-24 --variant hintfree --repo "..\benchmarks\xbow-hint-free\benchmarks"
```
→ Dòng cuối in ra URL, ví dụ `web OK: http://localhost:52714`. **Ghi lại URL này.**
(Image đã build sẵn nên bật rất nhanh. KHÔNG dùng `--down` ở đây — ta cần target chạy live.)

> Danh sách 40 bài + độ khó + loại lỗ hổng: xem `project\benchmarks\sample.csv`.

---

## BƯỚC 2 — NHÁNH A (Manual, không AI) — Người 1

1. 🖥️ Bật target (Bước 1), lấy URL.
2. Mở **Burp Suite Community** → cấu hình trình duyệt qua proxy Burp (127.0.0.1:8080).
3. Mở URL target trong trình duyệt. **Bấm giờ bắt đầu.**
4. Kiểm thử bằng tay: xem request/response trong Burp, thử sửa tham số, v.v. (tuỳ loại lỗ hổng).
5. Khi tìm được flag `FLAG{...}`, so với flag chuẩn:
   🖥️ **PS [...\project\benchmarks]**
   ```powershell
   Import-Csv targets.csv | Where-Object { $_.benchmark_id -eq "XBEN-023-24" } | Select-Object ground_truth_flag
   ```
6. **Bấm giờ kết thúc.** Ghi vào `results.csv`: `arm=A_manual, variant=original, solved=1/0, time_minutes, num_steps, notes`.
7. Hạ target: 🖥️ **PS [thư mục bài đó]** → `docker compose down` (đường dẫn bài: `project\benchmarks\validation-benchmarks\benchmarks\XBEN-023-24`).

> Giới hạn 30 phút/bài để công bằng với nhánh khác.

---

## BƯỚC 3 — NHÁNH B (Automated, không AI) — Người 2

🖥️ **PS [D:\Bình\KLTN new\project\harness]** (dùng terminal riêng của Người 2)

1. Bật target (Bước 1), lấy URL (ví dụ http://localhost:8000).
2. Chạy pipeline cố định (nuclei → ffuf → sqlmap/dalfox/SSTImap theo loại lỗ hổng):
   ```powershell
   python run_arm_B.py XBEN-023-24 --url http://localhost:8000
   ```
   ⚠️ Lệnh này chạy vài phút và **chiếm terminal** tới khi xong. Nó tự in `solved=0/1`, thời gian, và đường log.
3. Xem log chi tiết (nếu cần): `project\logs\B_XBEN-023-24.txt`.
4. Ghi `results.csv`: `arm=B_auto, variant=original, solved, time_minutes` (lấy từ output), `notes`.
5. Hạ target: `docker compose down` trong thư mục bài.

> KHÔNG tinh chỉnh công cụ theo từng bài. Nếu đổi cấu hình thì đổi cho **cả 40 bài** rồi chạy lại hết (xem `docs\ARM_B.md`).

---

## BƯỚC 4 — NHÁNH C1 (AI local: PentestGPT + Ollama) — Người 3

Cần **2 terminal** (một cho PentestGPT tương tác, một để chạy lệnh nó đề xuất).

**Terminal #1 — PentestGPT** 🖥️ **PS [D:\Bình\KLTN new\project\harness\PentestGPT]**
1. Bật target ở terminal khác trước (Bước 1), lấy URL.
2. Khởi động PentestGPT với model local:
   ```powershell
   python -m uv run pentestgpt-legacy --reasoning-model "ollama:qwen2.5:7b" --parsing-model "ollama:qwen2.5:7b" --base-url "http://localhost:11434/v1"
   ```
   ⚠️ Terminal này bị PentestGPT chiếm (giao diện hỏi-đáp). Nhập mô tả mục tiêu + URL khi nó hỏi.
   > Nếu báo lỗi model: kiểm tra `ollama list` có `qwen2.5:7b` và Ollama đang chạy. Chạy `... --list-models` để xem danh sách.

**Terminal #2 — chạy lệnh PentestGPT đề xuất** 🖥️ **PS (thư mục bất kỳ)**
3. PentestGPT (trợ lý) sẽ đề xuất lệnh (curl, sqlmap…). **Người 3 chạy lệnh ở Terminal #2**, rồi dán kết quả trở lại Terminal #1. → Mỗi lần người can thiệp như vậy, **đếm vào `manual_interventions`**.
4. Nếu model **từ chối** tác vụ → ghi `llm_refused=1` (hiếm với local, nhưng ghi nếu có).
5. Khi ra flag → so với `ground_truth_flag` (như Bước 2.5). Ghi `results.csv`: `arm=C_ai_local, variant=original`.
6. **Lặp lại toàn bộ với bản hint-free**: bật target bằng `--variant hintfree ...` (Bước 1), chạy lại, ghi `variant=hintfree`.

> So sánh `original` vs `hintfree` của nhánh C chính là phần đo "AI học thuộc" — đừng bỏ bước hint-free.

---

## BƯỚC 5 — Nhập dữ liệu & phân tích

1. Mở `project\results\results_template.csv`, lưu thành `results.csv`, điền từng dòng (mỗi lượt chạy 1 dòng).
   Cột: `benchmark_id,difficulty,vuln_category,arm,variant,run_id,solved,flag_found,time_minutes,num_steps,tokens_used,manual_interventions,llm_refused,notes`
2. 🖥️ **PS [D:\Bình\KLTN new\project\analysis]**
   ```powershell
   python analyze.py ..\results\results.csv
   ```
   → In bảng tổng hợp + xuất biểu đồ vào `paper\figures\`.

---

## BƯỚC 6 — Dọn dẹp (cuối buổi)

🖥️ **PS [D:\Bình\KLTN new\project\harness]**
```powershell
# ha tat ca container dang chay
docker ps -q | ForEach-Object { docker stop $_ }
```
Lấy lại dung lượng (chỉ khi cần, sẽ phải build lại): `docker system prune -af`

---

## Bảng tra nhanh: lệnh nào ở terminal nào
| Việc | Thư mục (PowerShell) | Chiếm terminal? |
|---|---|---|
| Bật/ hạ target | `project\harness` / thư mục bài | Không (trả control ngay) |
| Nhánh B pipeline | `project\harness` | **Có** (vài phút) |
| PentestGPT (nhánh C) | `project\harness\PentestGPT` | **Có** (tới khi thoát) |
| Chạy lệnh C đề xuất | bất kỳ (terminal #2) | Không |
| Phân tích | `project\analysis` | Không |
