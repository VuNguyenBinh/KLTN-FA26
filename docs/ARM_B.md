# Nhánh B — Công cụ quét tự động KHÔNG AI (hướng dẫn chi tiết)

> Claude ĐÃ CÀI SẴN toàn bộ công cụ vào `project/harness/toolsB/`. Phần dưới giải thích từng công cụ, cách đã cài, và cách chạy pipeline cố định. Nếu cần cài lại trên máy khác, làm theo mục "Cài lại".

## 1. Công cụ đã cài (trạng thái)
| Công cụ | Vai trò | Đường dẫn | Phiên bản |
|---|---|---|---|
| **nuclei** | Quét template lỗ hổng/expose/CVE | `toolsB\nuclei\nuclei.exe` | 3.11.1 |
| **ffuf** | Fuzz path/thư mục ẩn | cài qua winget (`ffuf` trên PATH) | 2.3.0 |
| **sqlmap** | Tự động khai thác SQL injection | `toolsB\sqlmap\sqlmap.py` (python) | 1.10.11 |
| **dalfox** | Phát hiện XSS | `toolsB\dalfox\...\dalfox.exe` | 3.2.4 |
| **SSTImap** | Khai thác SSTI (template injection) | `toolsB\SSTImap\sstimap.py` (python) | 1.4.0 |
| wordlist | từ điển fuzz cho ffuf | `toolsB\wordlists\common.txt` (4752 mục) | SecLists |

**Vì sao chọn bộ này:** mẫu 40 bài nhiều XSS (10) + SSTI (6) + SQLi (4). Nếu chỉ dùng nuclei+ffuf thì nhánh B sẽ ~0% trên các loại này → so sánh thành *strawman* không công bằng. Thêm sqlmap/dalfox/SSTImap (các bộ khai thác **không-AI** chuyên biệt) giúp nhánh B là baseline "tự động hóa không AI" **đáng tin**. Không công cụ nào dùng LLM.

## 2. Cách chạy (pipeline cố định — đã viết sẵn script)
Cùng một cấu hình cho MỌI bài (đây là điểm mấu chốt để kết quả tái lập được):

```powershell
cd "D:\Bình\KLTN new\project\harness"

# B1) bật target (lấy URL + cổng)
python build_target.py XBEN-006-24
#   -> xem targets.csv để lấy url, vd http://localhost:52714

# B2) chạy pipeline nhánh B
python run_arm_B.py XBEN-006-24 --url http://localhost:52714
```

`run_arm_B.py` tự làm theo thứ tự cố định:
1. **nuclei** quét toàn bộ template.
2. **ffuf** fuzz path bằng `common.txt`.
3. **Bộ khai thác theo loại lỗ hổng** (ánh xạ cố định từ `metadata.csv` tags):
   - `sqli / blind_sqli / nosqli` → **sqlmap** `--batch --dump-all`
   - `xss` → **dalfox**
   - `ssti` → **SSTImap**
   - loại khác (idor, lfi, cmdinj, deserialization, xxe...) → chỉ nuclei+ffuf *(thường KHÔNG ra flag — và đó chính là một kết quả nghiên cứu: tự động-không-AI bất lực với lỗ hổng cần suy luận nhiều bước)*.
4. Gom toàn bộ log, so khớp `ground_truth_flag` → in `solved=0/1`, thời gian, đường log (`logs/B_<bench>.txt`).

Ghi kết quả vào `results.csv` (nhánh=`B_auto`, variant=`original`).

> **Giới hạn thời gian:** mặc định tổng 30 phút/bài (`--budget 1800`). Giữ nguyên cho công bằng với nhánh A.

## 3. Lưu ý quan trọng (phương pháp)
- **Cấu hình cố định = không tinh chỉnh theo từng bài.** Không được "giúp" scanner bằng cách thêm payload riêng cho bài khó — như vậy là lén đưa trí tuệ người vào, hỏng tính "tự động". Nếu muốn mạnh hơn, đổi cấu hình **cho cả 40 bài** rồi chạy lại hết.
- Nhánh B dự kiến **solve-rate thấp hơn** A và C, nhất là ở IDOR/logic/deserialization. Đó là kết quả mong đợi, minh họa giá trị của con người/AI.
- Chạy nhánh B trên **bản gốc** là đủ (không cần hint-free — scanner không đọc gợi ý trong mã như LLM).

## 4. Cài lại (máy khác)
```powershell
# ffuf
winget install --id ffuf.ffuf -e --silent
# nuclei + dalfox: tải binary windows tu GitHub releases, giai nen vao toolsB\
#   https://github.com/projectdiscovery/nuclei/releases  (nuclei_*_windows_amd64.zip)
#   https://github.com/hahwul/dalfox/releases            (dalfox-*-windows-x86_64.zip)
# sqlmap + SSTImap (python, clone)
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git toolsB\sqlmap
git clone --depth 1 https://github.com/vladko312/SSTImap.git  toolsB\SSTImap
# templates cho nuclei (1 lan)
toolsB\nuclei\nuclei.exe -update-templates
# wordlist
#   tai Discovery/Web-Content/common.txt tu SecLists -> toolsB\wordlists\
```
