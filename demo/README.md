# Demo console — nhánh C2 (PentestGPT + DeepSeek V4 Pro)

Giao diện trực quan để demo nhánh AI API: chọn bài → tự dựng Docker lên localhost (gọi lại `build_target.py` của nhóm) → sinh lệnh khởi động PentestGPT + prompt grey-box → chạy vòng lặp PentestGPT↔operator, đếm bước/redirect, chấm flag, tổng hợp kết quả.

PentestGPT và PowerShell vẫn **chạy thật bên ngoài** — console chỉ điều phối và ghi nhận, nên demo minh bạch.

## Chạy
```powershell
# Yêu cầu: Docker Desktop đang chạy; benchmark repo đã có (như build_target.py).
python demo/server.py
# Mở trình duyệt: http://127.0.0.1:8765
```
Không cần cài thêm gì — backend dùng thư viện chuẩn Python.

## Luồng demo
1. **① Chọn bài** (mẫu 40, tick để xem đủ 104) + biến thể original/hint-free.
2. **② Dựng target** → backend gọi `build_target.py <ID> --variant …` (chạy nền, log trực tiếp). Xong sẽ hiện **Target URL** đang chạy.
3. **③ Khởi động PentestGPT** → copy **lệnh** (sửa 1 lần, tự lưu) và **prompt mô tả** (tự sinh theo lớp lỗ hổng + URL) sang terminal PentestGPT ngoài.
4. **Khung chat** — mỗi lượt: dán câu trả lời PentestGPT (+lệnh, tính +1 bước) → chạy lệnh ở PowerShell ngoài → dán output lại (tick *redirect* khi bẻ lái). Đồng hồ 30′ và bộ đếm tự chạy.
5. **Chấm flag** (dưới cùng): tính `FLAG{sha256(UPPER(mã-bài))}` ngay trên máy, so khớp chính xác.
6. **Tổng hợp**: tải **nhật ký `.md`** (kiểu report_C2) và **dòng `results.csv`**; nút **Hạ target** để dọn container.

## File
- `server.py` — backend stdlib (serve UI + `/api/tasks`, `/api/build`, `/api/build_status`, `/api/down`). Chỉ cho id có trong `metadata.csv` (chống chèn lệnh).
- `app.html` — giao diện chính (sidebar + chat).
- `c2_console.html` — bản offline tối giản (không tự dựng Docker), dùng khi không chạy backend.

> Lệnh khởi động PentestGPT ở bước ③ là **mẫu, sửa cho đúng cách bạn chạy** (chế độ legacy + model qua `.env`); phần tự sinh quan trọng là prompt grey-box.
