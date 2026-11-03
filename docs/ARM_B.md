# Công cụ tự động KHÔNG AI — tầng công cụ của nhánh Truyền thống (hướng dẫn chi tiết)

> ⚠️ **Cấu trúc 3 nhánh (2026-11-03):** đây là **tầng công cụ tự động (`B_auto`) của nhánh Truyền thống** (người + công cụ), không còn là một "nhánh B" riêng. Pipeline dưới đây vẫn chạy y nguyên; chỉ cách *gom nhóm phân tích* đổi — kết quả `B_auto` đóng vai "trần tự-động-hoá" bên trong nhánh Truyền thống. Xem `PLAN.md` mục 3 và `STATUS.md`.
>
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

**Vì sao chọn bộ công cụ này.** Trong 40 bài của mẫu, có 20 bài rơi đúng vào ba nhóm lỗ hổng mà các bộ công cụ chuyên biệt nhắm tới: XSS (10 bài — dalfox), SSTI (6 bài — SSTImap) và họ SQL (4 bài, gồm sqli 2, blind-sqli 1, nosqli 1 — sqlmap). 20 bài còn lại thuộc các lớp khác, chủ yếu là IDOR (6), insecure deserialization (3), command injection (2), privilege escalation (2) cùng bảy lớp lẻ. Nếu công cụ tự động chỉ dựa vào nuclei và ffuf, nó gần như không làm được gì trên nhóm XSS/SSTI/SQL, khiến phép so sánh trở thành một *strawman* thiếu công bằng. Bổ sung sqlmap, dalfox và SSTImap — tất cả đều là công cụ **không dùng AI** — giúp công cụ tự động trở thành một baseline "tự động hóa không AI" **đáng tin cậy**, chứ không phải một đối trọng dựng sẵn để thua. Không công cụ nào trong nhánh này dùng mô hình ngôn ngữ.
> Lưu ý: tính theo **mọi** nhãn (không chỉ nhãn đầu), có **21/40** bài được một exploiter chuyên biệt chạy — dư 1 so với 20 ở trên vì 1 bài nhãn-đầu IDOR (XBEN-006) còn mang nhãn phụ SQLi nên sqlmap vẫn chạy. 19/40 bài còn lại chỉ dựa nuclei+ffuf.

## 2. Cách chạy (pipeline cố định — đã viết sẵn script)
Cùng một cấu hình cho MỌI bài (đây là điểm mấu chốt để kết quả tái lập được):

```powershell
cd "D:\Bình\KLTN new\project\harness"

# B1) bật target (lấy URL + cổng)
python build_target.py XBEN-006-24
#   -> xem targets.csv để lấy url, vd http://localhost:52714

# B2) chạy pipeline công cụ tự động
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

> **Giới hạn thời gian:** mặc định tổng 30 phút/bài (`--budget 1800`). Giữ nguyên cho công bằng với nhánh Truyền thống (người).

### 2b. Chạy cả 40 bài một lượt (orchestrator)
Thay vì bật/hạ từng bài bằng tay, dùng `run_arm_B_all.py` — nó lặp `sample.csv`: bật target → chạy `run_arm_B.py --out-csv` → hạ target, ghi thẳng vào `results.csv`:
```powershell
cd "D:\Bình\KLTN new\project\harness"
python run_arm_B_all.py                 # cả 40 bài, bản gốc
python run_arm_B_all.py --budget 1800   # 30 phút/bài
python run_arm_B_all.py --only XBEN-071-24 XBEN-083-24   # chạy lại vài bài
```
Chạy lâu (vài giờ) → nên chạy nền. Công cụ tự động chỉ chạy **bản gốc** (scanner không đọc gợi ý như LLM).

### 2c. Hai chỉ số: *phát hiện* vs *bắt flag*
`run_arm_B.py` ghi 2 thứ vào cột `notes`:
- `solved` (cột chuẩn) = **bắt được flag** đúng `ground_truth_flag` → tiêu chí giải của benchmark.
- `detected=yes/no` = công cụ **có báo lỗ hổng** không (dựa trên dấu hiệu `[POC]`/`[V]`/`is vulnerable`/`injectable`/`back-end dbms`/`ssti`/mức `[medium|high|critical]`).

Sự phân biệt này là điểm **cốt lõi** của công cụ tự động: công cụ tự động không-AI thường *thấy* được lỗ hổng, nhưng hiếm khi tự đi hết chuỗi nhiều bước để lấy ra flag.

## 3. Kết quả (chạy 2026-11-02, 40 bài gốc, budget 30′/bài)

| Chỉ số | Kết quả |
|---|---|
| **Bắt được flag** (`solved`) | **2/40 = 5,0%** — XBEN-071, XBEN-083 (đều SQLi, sqlmap dump DB) |
| **Phát hiện lỗ hổng** (`detected`) | **11/40 = 27,5%** |

Theo độ khó (bắt / phát hiện): easy 2/14=14,3% / 7/14=50,0%; medium 0% / 2/18=11,1%; hard 0% / 2/8=25,0%.

Phát hiện theo loại: **XSS 8/10=80% phát hiện (dalfox báo `[POC]`) nhưng 0 bắt flag**; **SQLi 2/2=100% phát hiện VÀ bắt flag**; **CVE 1/1** (nuclei template đúng, không phải generic). Mọi lớp còn lại **0 phát hiện** — gồm **SSTI 0/6** (SSTImap chạy `--crawl` nhưng không tự tìm được injection point), **IDOR 0/6**, deserialization 0/3, command_injection 0/2…

**Diễn giải.** Khoảng cách giữa *phát hiện* (27,5%) và *bắt flag* (5%) là rõ rệt — chênh nhau khoảng 5,5 lần. Bộ công cụ cố định chỉ nhận ra lỗ hổng ở đúng hai nhóm. Với XSS phản chiếu, dalfox báo được dấu hiệu nhưng không tự dựng tiếp ngữ cảnh để lấy flag; chỉ SQLi là trọn vẹn, vì sqlmap tự đi hết chuỗi từ phát hiện đến trích xuất dữ liệu nên vừa phát hiện vừa bắt được flag. Ngược lại, những lớp đòi hỏi suy luận theo ngữ cảnh hoặc nhiều bước — SSTI, IDOR, lỗi logic — thì scanner cố định không nhận ra nổi ngay từ khâu phát hiện. Nói cách khác, công cụ tự động hụt ở cả hai đầu, *phát hiện* lẫn *khai thác*; đó chính là hai khoảng trống mà nhánh AI (có AI hỗ trợ) được kỳ vọng lấp.

> **Ghi chú tái lập (các bug đo đã sửa):** (A) nuclei coi `localhost` là unresponsive → mọi công cụ dùng `127.0.0.1`; (B) dalfox 3.2.4 crash với `--no-spinner` → dùng `-S`; (C) exploiter chỉ quét URL gốc → nạp thêm path ffuf; (D) SSTImap crash vì cờ `-B` → bỏ, chỉ `--crawl`; (E) heuristic cũ thổi phồng detection 22/40=55% do (i) chuỗi con "ssti" khớp tên tool "SSTImap" trong banner lỗi và (ii) token trần `injectable` khớp cả "not injectable" → nay chỉ đếm tín hiệu DƯƠNG rõ ràng theo lớp. Detection đúng = **11/40**; cột `detected` được chấm lại từ log đã lưu bằng heuristic sửa (output công cụ không đổi). Capture 2/40 là thật từ đầu.

## 4. Lưu ý quan trọng (phương pháp)
- **Cấu hình cố định = không tinh chỉnh theo từng bài.** Không được "giúp" scanner bằng cách thêm payload riêng cho bài khó — như vậy là lén đưa trí tuệ người vào, hỏng tính "tự động". Nếu muốn mạnh hơn, đổi cấu hình **cho cả 40 bài** rồi chạy lại hết.
- Công cụ tự động dự kiến **solve-rate thấp hơn** A và C, nhất là ở IDOR/logic/deserialization. Đó là kết quả mong đợi, minh họa giá trị của con người/AI.
- Chạy công cụ tự động trên **bản gốc** là đủ (không cần hint-free — scanner không đọc gợi ý trong mã như LLM).

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
