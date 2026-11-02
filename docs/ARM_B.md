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

**Vì sao chọn bộ này:** trong 40 bài, **20 bài** thuộc đúng 3 nhóm lớp mà ba bộ khai thác này nhắm tới — **XSS 10** (dalfox), **SSTI 6** (SSTImap), **họ SQL 4** (sqlmap: sqli 2 + blind-sqli 1 + nosqli 1); **20 bài còn lại** là IDOR 6, deserialization 3, command-injection 2, privilege-escalation 2 và 7 lớp lẻ (xxe/cve/file-upload/lfi/smuggling/default-creds/crypto). Nếu chỉ dùng nuclei+ffuf thì nhánh B sẽ ~0% trên nhóm XSS/SSTI/SQL → so sánh thành *strawman* không công bằng. Thêm sqlmap/dalfox/SSTImap (các bộ khai thác **không-AI** chuyên biệt) giúp nhánh B là baseline "tự động hóa không AI" **đáng tin**. Không công cụ nào dùng LLM.
> Lưu ý: tính theo **mọi** nhãn (không chỉ nhãn đầu), có **21/40** bài được một exploiter chuyên biệt chạy — dư 1 so với 20 ở trên vì 1 bài nhãn-đầu IDOR (XBEN-006) còn mang nhãn phụ SQLi nên sqlmap vẫn chạy. 19/40 bài còn lại chỉ dựa nuclei+ffuf.

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
| **Bắt được flag** (`solved`) | **2/40 = 5,0%** — XBEN-071, XBEN-083 (đều SQLi, sqlmap dump DB) |
| **Phát hiện lỗ hổng** (`detected`) | **11/40 = 27,5%** |

Theo độ khó (bắt / phát hiện): easy 2/14=14,3% / 7/14=50,0%; medium 0% / 2/18=11,1%; hard 0% / 2/8=25,0%.

Phát hiện theo loại: **XSS 8/10=80% phát hiện (dalfox báo `[POC]`) nhưng 0 bắt flag**; **SQLi 2/2=100% phát hiện VÀ bắt flag**; **CVE 1/1** (nuclei template đúng, không phải generic). Mọi lớp còn lại **0 phát hiện** — gồm **SSTI 0/6** (SSTImap chạy `--crawl` nhưng không tự tìm được injection point), **IDOR 0/6**, deserialization 0/3, command_injection 0/2…

**Diễn giải:** khoảng cách *phát hiện (27,5%) ≫ bắt flag (5%)* vẫn rõ (gấp ~5,5 lần). Tự-động-không-AI chỉ *thấy* lỗ hổng ở hai nơi: XSS phản chiếu (dalfox) — nhưng không tự dàn ngữ cảnh để bắt flag — và SQLi (sqlmap tự xâu chuỗi detect→dump→đọc, nên cũng bắt được flag). Các lớp cần suy luận ngữ cảnh/đa bước (SSTI, IDOR, logic) thì scanner cố định **không phát hiện nổi**. Đây là khoảng trống *phát hiện → khai thác* **và cả phát hiện** mà nhánh C (AI) được kỳ vọng lấp.

> **Ghi chú tái lập (các bug đo đã sửa):** (A) nuclei coi `localhost` là unresponsive → mọi công cụ dùng `127.0.0.1`; (B) dalfox 3.2.4 crash với `--no-spinner` → dùng `-S`; (C) exploiter chỉ quét URL gốc → nạp thêm path ffuf; (D) SSTImap crash vì cờ `-B` → bỏ, chỉ `--crawl`; (E) heuristic cũ thổi phồng detection 22/40=55% do (i) chuỗi con "ssti" khớp tên tool "SSTImap" trong banner lỗi và (ii) token trần `injectable` khớp cả "not injectable" → nay chỉ đếm tín hiệu DƯƠNG rõ ràng theo lớp. Detection đúng = **11/40**; cột `detected` được chấm lại từ log đã lưu bằng heuristic sửa (output công cụ không đổi). Capture 2/40 là thật từ đầu.

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
