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

### 2b. Chạy cả 40 bài một lượt (orchestrator)
Thay vì bật/hạ từng bài bằng tay, dùng `run_arm_B_all.py` — nó lặp `sample.csv`: bật target → chạy `run_arm_B.py --out-csv` → hạ target, ghi thẳng vào `results.csv`:
```powershell
cd "D:\Bình\KLTN new\project\harness"
python run_arm_B_all.py                 # cả 40 bài, bản gốc
python run_arm_B_all.py --budget 1800   # 30 phút/bài
python run_arm_B_all.py --only XBEN-071-24 XBEN-083-24   # chạy lại vài bài
```
Chạy lâu (vài giờ) → nên chạy nền. Nhánh B chỉ chạy **bản gốc** (scanner không đọc gợi ý như LLM).

### 2c. Hai chỉ số: *phát hiện* vs *bắt flag*
`run_arm_B.py` ghi 2 thứ vào cột `notes`:
- `solved` (cột chuẩn) = **bắt được flag** đúng `ground_truth_flag` → tiêu chí giải của benchmark.
- `detected=yes/no` = công cụ **có báo lỗ hổng** không (dựa trên dấu hiệu `[POC]`/`[V]`/`is vulnerable`/`injectable`/`back-end dbms`/`ssti`/mức `[medium|high|critical]`).

Phân biệt này là **cốt lõi** của nhánh B: tự-động-không-AI thường *thấy* lỗ hổng nhưng không tự khai thác nhiều bước tới flag.

## 3. Kết quả (chạy 2026-11-02, 40 bài gốc, budget 30′/bài)

| Chỉ số | Kết quả |
|---|---|
| **Bắt được flag** (`solved`) | **2/40 = 5%** — XBEN-071, XBEN-083 (đều SQLi, sqlmap dump DB) |
| **Phát hiện lỗ hổng** (`detected`) | **22/40 = 55%** |

Theo độ khó (bắt / phát hiện): easy 2/14=14.3% / 9/14=64%; medium 0% / 10/18=56%; hard 0% / 3/8=37.5%.

Phát hiện theo loại (đáng chú ý): **SSTI 6/6=100% phát hiện nhưng 0 bắt flag**; **XSS 8/10 phát hiện, 0 bắt**; **IDOR 0/6 phát hiện** (logic nghiệp vụ, scanner mù); **SQLi 2/2 bắt flag 100%**.

**Diễn giải:** khoảng cách *phát hiện (55%) ≫ bắt flag (5%)* cho thấy tự-động-không-AI nhận ra **lớp** lỗ hổng nhưng gần như không tự xâu chuỗi các bước khai thác để lấy đúng flag — trừ SQLi vì sqlmap tự dump DB ra flag. Đây chính là khoảng trống *phát hiện → khai thác* mà nhánh C (AI) được kỳ vọng lấp.

> **Ghi chú tái lập (bug đã sửa):** lần chạy đầu cũng ra 2/40 nhưng vì lý do SAI, không phải đúng. 3 lỗi đo: (1) nuclei coi `localhost` là unresponsive → nay mọi công cụ dùng `127.0.0.1`; (2) dalfox 3.2.4 crash với `--no-spinner` → nay dùng `-S`; (3) exploiter chỉ quét URL gốc → nay nạp thêm các path ffuf tìm được. Thêm: giới hạn `--budget` ép theo từng bước, và cột `detected`. Sau khi sửa, 2/40 là con số thật.

## 4. Lưu ý quan trọng (phương pháp)
- **Cấu hình cố định = không tinh chỉnh theo từng bài.** Không được "giúp" scanner bằng cách thêm payload riêng cho bài khó — như vậy là lén đưa trí tuệ người vào, hỏng tính "tự động". Nếu muốn mạnh hơn, đổi cấu hình **cho cả 40 bài** rồi chạy lại hết.
- Nhánh B dự kiến **solve-rate thấp hơn** A và C, nhất là ở IDOR/logic/deserialization. Đó là kết quả mong đợi, minh họa giá trị của con người/AI.
- Chạy nhánh B trên **bản gốc** là đủ (không cần hint-free — scanner không đọc gợi ý trong mã như LLM).

## 5. Cài lại (máy khác)
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
