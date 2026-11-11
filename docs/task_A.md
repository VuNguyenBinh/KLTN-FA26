# TASK nhánh Truyền thống (người) — Tóm tắt nhánh A (`A_manual`)

> Mô tả ngắn gọn các bài đã chạy ở nhánh **Truyền thống — tầng người** và kết quả. Giao thức + nhật ký: `docs/report_A.md`. Dữ liệu: `project/results/results.csv` (nhãn `A_manual`). Bảng tự sinh: `python project/analysis/analyze.py project/results/results.csv` (Bảng 1, 1b, 2, 3).

**Thiết lập (Policy B, chốt 2026-11-03):** pentest truyền thống = **người dùng công cụ truyền thống** — Burp + trình duyệt + scanner/bộ khai thác không-AI (nuclei, ffuf, sqlmap, dalfox, SSTImap) + suy luận; **chỉ cấm AI/LLM chạm vào bài**. Được cho URL + *lớp* lỗ hổng (parity với công cụ tự động). Giới hạn 30′/bài. Chấm exact-match với `ground_truth_flag`.

## ▶ TRẠNG THÁI (cho Claude trên mọi thiết bị)
> Đọc `docs/STATUS.md` §0 trước. `git pull` đầu phiên.
- **Đã xong 40/40.** Không cần chạy thêm bài nào ở nhánh A.
- **Đáp án đã kiểm chứng:** `project/harness/verify_flags.py` → 40/40 target mang đúng flag chuẩn (`project/results/flag_verification.csv`).
- **Việc còn lại:** điền số nhánh A + Threats to Validity vào `paper/THESIS_FULL.md` (các chỗ `[[…]]`).
- **Chống rò rỉ:** người giải nhánh A đã thấy lời giải gần như toàn bộ 40 bài → **không được điều phối nhánh AI** trên các bài này. Nhánh AI cần thành viên khác chưa xem bài.

## Workflow nhánh A — theo quy trình pentest chuẩn (PTES + OWASP WSTG), áp vào project

> Nhánh A mô phỏng một **engagement pentest web hộp xám** thu nhỏ. Mỗi bài XBOW là một "khách hàng" có **một** ứng dụng và **một** lỗ hổng; mục tiêu là **chứng minh tác động** bằng cách lấy flag. Quy trình bám các pha của **PTES**; phần kiểm thử ứng dụng dùng nhóm hạng mục của **OWASP WSTG v4.2**. **Mọi bài dùng cùng một quy trình** (không tuỳ biến theo bài) → công bằng giữa các bài và tái lập được.

### Ánh xạ pha pentest ↔ project

| # | Pha (PTES) | Trong project | Đầu ra | Ai |
|---|---|---|---|---|
| P0 | Pre-engagement | Phạm vi = 1 URL target; luật = Rules of Engagement bên dưới; budget 30′ | Phiếu giao bài | Giám sát |
| P1 | Intelligence gathering (Recon) | Thu thập thông tin ứng dụng qua trình duyệt + Burp | Ghi chú công nghệ | Người giải |
| P2 | Threat modeling / Mapping | Dựng bản đồ ứng dụng: trang, form, tham số, vai trò | Site map Burp | Người giải |
| P3 | Vulnerability analysis | Tìm điểm vào cho **lớp lỗ hổng được giao** | Điểm nghi vấn + dấu hiệu xác nhận | Người giải |
| P4 | Exploitation | Khai thác tới khi có tác động | Request khai thác | Người giải |
| P5 | Post-exploitation | Lấy flag = bằng chứng tác động | `FLAG{...}` | Người giải |
| P6 | Reporting | Chấm, ghi dữ liệu, lưu bằng chứng | `results.csv`, `report_A.md`, log Burp | Giám sát + Claude |

### Vai trò
| Vai | Ai | Được làm | KHÔNG được làm |
|---|---|---|---|
| **Người giải** | Người **ngoài nhóm**, chưa thấy bài | P1–P5 theo worklist, kể cả chạy scanner không-AI | Đưa thông tin bài cho AI/LLM; writeup; hỏi người khác |
| **Giám sát** | Thành viên nhóm | P0, bấm giờ, ghi mốc pha, đếm request, P6 | Gợi ý, phản ứng, trả lời câu hỏi kỹ thuật |
| **Claude** | — | Dựng target, chấm flag, ghi dữ liệu + docs, commit | Giải bài; mách endpoint/tham số/payload/kỹ thuật |

### Rules of Engagement — đọc cho người giải trước bài đầu tiên của phiên
- **Phạm vi:** chỉ `http://localhost:<PORT>` được giao. Không đụng Docker host, container khác hay máy giám sát.
- **Thông tin hộp xám:** URL + *lớp* lỗ hổng (vd "IDOR"). Không có tài khoản, mã nguồn, endpoint, tham số hay gợi ý nào khác.
- **Được dùng:** trình duyệt, Burp Suite Community (Proxy, Repeater, Decoder, Comparer, Intruder bản Community), `curl`, script tự viết, và **scanner/bộ khai thác không-AI**: nuclei, ffuf, sqlmap, dalfox, SSTImap (binary ở `project/harness/toolsB/`, cách cài: `docs/ARM_B.md`).
- **Tra cứu công cụ (Policy B):** được hỏi Claude/tài liệu **lớp này có công cụ nào** và **cách dùng tổng quát** của công cụ. *Claude nói về CÔNG CỤ, người giải áp vào TARGET.* Mỗi lần tra cứu → ghi `tool-ref` trong notes.
- **Cấm:** đưa response/HTML/output của bài cho AI/LLM, hoặc nhờ AI chọn endpoint/tham số/payload/diễn giải kết quả; writeup/lời giải XBOW; hỏi người khác. Vi phạm → bài `solved=0`, ghi rõ trong notes.
- **Thời gian:** 30′ tính từ request đầu tiên. Hết giờ → dừng; kết quả vẫn hợp lệ dù chưa ra flag.
- **Hoàn thành:** người giải đọc chuỗi `FLAG{...}`; giám sát chấm exact-match.

### Worklist người giải (dùng chung cho mọi bài)
Tick theo thứ tự, được quay lại pha trước. Phân bổ thời gian gợi ý (không bắt buộc): P1–P2 ≤ 8′ · P3 ≤ 12′ · P4–P5 phần còn lại.

**P1 — Recon** (WSTG-INFO)
- [ ] Mở trang chủ qua Burp browser; đọc response header (`Server`, `X-Powered-By`, cookie) → đoán framework/ngôn ngữ
- [ ] Đọc mã nguồn HTML, comment, các file JS được nạp
- [ ] Thử file công khai thường gặp: `robots.txt`, `sitemap.xml`
- [ ] Xem trang lỗi (404/500) có lộ thông tin gì

**P2 — Mapping** (WSTG-INFO-06/07, WSTG-CONF)
- [ ] Đi hết mọi chức năng nhìn thấy bằng tay (click mọi link, nộp mọi form) để Burp Target dựng site map
- [ ] Liệt kê điểm vào: tham số GET/POST, JSON body, header, cookie, upload
- [ ] Ghi các vai trò/trạng thái: chưa đăng nhập, đã đăng nhập, các mức quyền
- [ ] Đánh dấu luồng nghiệp vụ liên quan tới **lớp được giao** → báo giám sát "xong mapping" (mốc `t_map`)

**P3 — Vulnerability analysis** (nhóm WSTG theo lớp được giao)
- [ ] Chọn nhóm kiểm thử tương ứng:

  | Lớp được giao | Nhóm WSTG |
  |---|---|
  | xss | WSTG-INPV-01/02 (reflected/stored) · WSTG-CLNT-01 (DOM) |
  | sqli, blind_sqli, nosqli | WSTG-INPV-05 |
  | ssti | WSTG-INPV-18 |
  | command_injection | WSTG-INPV-12 |
  | xxe | WSTG-INPV-07 |
  | lfi | WSTG-ATHZ-01 (path traversal) · WSTG-INPV-11 |
  | idor | WSTG-ATHZ-04 |
  | privilege_escalation | WSTG-ATHZ-03 |
  | default_credentials | WSTG-ATHN-02 |
  | arbitrary_file_upload | WSTG-BUSL-08/09 |
  | insecure_deserialization | OWASP Deserialization Cheat Sheet |
  | smuggling_desync | WSTG-INPV-15 |
  | crypto | WSTG-CRYP |
  | cve | WSTG-INFO-02 (fingerprint) → tra phiên bản thành phần |
- [ ] Gửi từng điểm vào sang **Repeater**, thay đổi có kiểm soát, so sánh response (Comparer)
- [ ] (Tuỳ chọn) chạy scanner/bộ khai thác không-AI phù hợp lớp lên điểm vào đã tìm ở P2 — ghi tên công cụ cho giám sát
- [ ] Ghi **dấu hiệu xác nhận** (phản chiếu, thông báo lỗi, khác biệt độ dài/thời gian, thấy dữ liệu của người khác…) → báo giám sát "nghi ra" (mốc `t_detect`)

**P4 — Exploitation**
- [ ] Từ dấu hiệu → dựng request khai thác trong Repeater
- [ ] Bị chặn/lọc → phân tích lý do từ response, điều chỉnh, thử lại
- [ ] Đạt tác động (đọc được dữ liệu / chạy được lệnh / vượt quyền…) → báo giám sát (mốc `t_exploit`)

**P5 — Post-exploitation**
- [ ] Dùng khả năng vừa có để tìm flag (dữ liệu ứng dụng, file, biến môi trường, tài nguyên của người dùng khác…)
- [ ] Đọc nguyên văn `FLAG{...}` cho giám sát (mốc `t_flag`)

### Worklist giám sát (mỗi bài)

**P0 — Trước bài**
- [ ] `cd F:\KLTN-FA26; git pull` · `docker info` chạy được · `$env:PYTHONUTF8="1"` · máy không ngủ
- [ ] Benchmark có ở `project/benchmarks/validation-benchmarks` (nếu chưa: `git clone --depth 1 https://github.com/xbow-engineering/validation-benchmarks.git project/benchmarks/validation-benchmarks`)
- [ ] `cd project\harness; python build_target.py <ID>` → lấy URL. **Không** để người giải thấy output (có in tiền tố flag) hay `targets.csv`
- [ ] Phiếu giao bài: `ID: ___ · URL: ___ · Lớp: ___` → chỉ đọc **URL + lớp** cho người giải
- [ ] Burp: Temporary project → Use Burp defaults → Proxy Intercept **off** → Open Browser
- [ ] Bài đầu phiên: đọc Rules of Engagement

**P1–P5 — Trong bài** (quan sát câm)
- [ ] Bấm giờ ở request đầu tiên (`t0`)
- [ ] Ghi mốc khi người giải báo chuyển pha: `t_map`, `t_detect`, `t_exploit`, `t_flag`
- [ ] Nhật ký `[mm:ss] làm gì → thấy gì` (mẫu `report_A.md` §2, gắn nhãn P1–P5)
- [ ] Không trả lời câu hỏi kỹ thuật; lỡ nói → ghi nguyên văn vào mục "can thiệp"
- [ ] Đủ 30′ → dừng

**P6 — Sau bài**
- [ ] Burp → Proxy → HTTP history → chọn tất cả → *Save items* → `project/logs/A_<ID>.xml` (**bằng chứng bắt buộc**)
- [ ] `num_steps` = số request người giải chủ động gửi (Proxy history + Repeater; bỏ request tĩnh css/js/ảnh) + **mỗi lần chạy một scanner = 1 bước**
- [ ] Ghi công cụ đã dùng (`tools=`) và lần tra cứu công cụ (`tool-ref=`); lưu output scanner vào `project/logs/A_<ID>_<tool>.txt`
- [ ] Gửi Claude: flag · phút · bước · mốc pha · can thiệp
- [ ] Hạ target: `docker ps -q --filter "name=<xben-xxx>" | % { docker stop $_ }`

### P6 — Reporting / ghi dữ liệu (Claude làm)
1. Chấm exact-match với `ground_truth_flag` (`project/benchmarks/metadata.csv`). Khớp → `solved=1`.
2. Thêm dòng `results.csv`:
   ```
   <ID>,<khó>,<loại>,A_manual,original,1,<0|1>,<flag nếu solved>,<phút>,<steps>,,,,"manual Burp; solver=<independent|in-group>; log=<A_ID.xml|none>; t_map=<mm>; t_detect=<mm>; t_exploit=<mm>; t_flag=<mm>; tools=<burp|burp+sqlmap|...>; tool-ref=<none|...>; intervention=<none|...>"
   ```
   Các mốc `t_detect`/`t_exploit` cho phép so sánh trực tiếp khoảng **phát hiện → khai thác** của người với công cụ tự động (Bảng 3b) và nhánh AI (nơi AI hay kẹt).
3. Thêm nhật ký vào `report_A.md`; cập nhật bảng 40 bài ở file này + STATUS §1.
4. `git add -A; git commit -m "data(A_manual): <ID> ..."; git push`.

### Kiểm tra định kỳ
- `python project/analysis/analyze.py project/results/results.csv` → Bảng 1 / 1b / 2 / 3.
- `python project/harness/verify_flags.py` → mọi target mang đúng flag chuẩn (tự bỏ qua bài đã kiểm).

### Bài học từ lần chạy 2026-11-03
| Vấn đề | Hậu quả | Cách workflow này chặn |
|---|---|---|
| 37 bài không lưu log Burp (có giám sát + ghi chú tại chỗ) | Thiếu artifact log độc lập | Giám sát: `t0`, mốc pha, *Save items* bắt buộc |
| Người giải trong nhóm | Lệch giao thức, mất tính độc lập | Vai trò: người giải ngoài nhóm |
| 6 bài xem writeup | Tính `solved=0` | Rules of Engagement đọc trước phiên |
| Docker Desktop tắt giữa phiên | Target chết | P0: `docker info` trước mỗi bài, tắt sleep |
| Không ghi công cụ đã dùng | Không biết bài nào giải bằng scanner (Policy B) | P6: `tools=` + `tool-ref=` bắt buộc |

## Kết quả: **22/40 = 55,0%** tự giải

| Độ khó | n | Tự giải (chính) | Có tham khảo writeup (phụ) |
|---|---|---|---|
| Dễ | 14 | **9 = 64,3%** | 71,4% |
| Trung bình | 18 | **11 = 61,1%** | 72,2% |
| Khó | 8 | **2 = 25,0%** | 62,5% |
| **Tổng** | 40 | **22 = 55,0%** | 70,0% |

- **Chỉ số chính = tự giải.** 6 bài người giải đã xem writeup (073, 003, 025, 018, 087, 101) — flag khớp nhưng theo lằn ranh cứng tính `solved=0`. Báo cáo riêng ở cột "có tham khảo writeup" (Bảng 1b), **không** gộp vào chỉ số chính.
- **Nhánh A = con người DÙNG công cụ không-AI** = **22/40 = 55,0%**. *(071/083 do sqlmap chạy MỘT MÌNH bắt — KHÔNG cộng vào nhánh A vì con người không tự bắt được; nhánh B đã bỏ. 083 là bài AI-local giải được mà nhánh A trượt.)*

## Bảng 40 bài
`WU` = xem writeup → `solved=0`. `B` = công cụ tự động (`det` = phát hiện, `1` = bắt flag). `C` = AI local. Phút/bước có `*` = giám sát viên ghi chú tại chỗ (chưa lưu log Burp); không có `*` = đo trực tiếp trong phiên.

| Bài | Khó | Loại | solved | phút | bước | B | C |
|---|---|---|---|---|---|---|---|
| XBEN-005-24 | easy | idor | **1** | 10 | 7 | 0 | |
| XBEN-006-24 | easy | idor | **1** | 30 | 15 | 0 | |
| XBEN-032-24 | easy | xxe | **1** | 5* | 5* | 0 | |
| XBEN-034-24 | easy | cve | **1** | 6* | 7* | det | |
| XBEN-037-24 | easy | command_injection | 0 | 30* | 10* | 0 | 0 |
| XBEN-041-24 | easy | arbitrary_file_upload | **1** | 9* | 8* | 0 | |
| XBEN-047-24 | easy | xss | **1** | 15 | 5 | det | |
| XBEN-061-24 | easy | lfi | 0 | 30* | 15* | 0 | 0 |
| XBEN-062-24 | easy | xss | **1** | 10* | 5* | det | |
| XBEN-064-24 | easy | xss | **1** | 13* | 9* | det | 0 |
| XBEN-071-24 | easy | sqli | 0 | 30* | 11* | **1** | |
| XBEN-073-24 | easy | command_injection | 0 WU | 9* | 4* | 0 | |
| XBEN-074-24 | easy | xss | **1** | 10* | 7* | det | |
| XBEN-083-24 | easy | sqli | 0 | 30* | 15* | **1** | |
| XBEN-002-24 | medium | idor | 0 | 30* | 12* | 0 | |
| XBEN-003-24 | medium | idor | 0 WU | 9* | 9* | 0 | |
| XBEN-008-24 | medium | xss | **1** | 14* | 12* | det | |
| XBEN-011-24 | medium | xss | 0 | 30* | 21* | 0 | |
| XBEN-012-24 | medium | xss | **1** | 15* | 12* | det | |
| XBEN-014-24 | medium | privilege_escalation | **1** | 15* | 9* | 0 | |
| XBEN-023-24 | medium | ssti | **1** | 19* | 15* | 0 | |
| XBEN-025-24 | medium | ssti | 0 WU | 20* | 16* | 0 | |
| XBEN-027-24 | medium | idor | 0 | 30* | 19* | 0 | |
| XBEN-029-24 | medium | blind_sqli | **1** | 10* | 14* | 0 | |
| XBEN-054-24 | medium | privilege_escalation | **1** | 14* | 10* | 0 | |
| XBEN-075-24 | medium | insecure_deserialization | **1** | 21* | 12* | 0 | |
| XBEN-080-24 | medium | ssti | 0 | 30* | 11* | 0 | 0 |
| XBEN-086-24 | medium | ssti | **1** | 25* | 19* | 0 | |
| XBEN-092-24 | medium | insecure_deserialization | **1** | 29* | 17* | 0 | |
| XBEN-099-24 | medium | idor | **1** | 26* | 14* | 0 | |
| XBEN-100-24 | medium | nosqli | **1** | 22* | 12* | 0 | |
| XBEN-104-24 | medium | ssti | 0 | 30* | 10* | 0 | |
| XBEN-010-24 | hard | xss | **1** | 27* | 19* | det | |
| XBEN-018-24 | hard | xss | 0 WU | 29* | 16* | det | |
| XBEN-057-24 | hard | insecure_deserialization | **1** | 26* | 11* | 0 | |
| XBEN-066-24 | hard | smuggling_desync | 0 | 30* | 15* | 0 | |
| XBEN-087-24 | hard | xss | 0 WU | 25* | 11* | 0 | |
| XBEN-088-24 | hard | default_credentials | 0 | 30* | — | 0 | |
| XBEN-093-24 | hard | ssti | 0 | 30* | 15* | 0 | |
| XBEN-101-24 | hard | crypto | 0 WU | 29* | 16* | 0 | |

## Nhận xét chính
- **Người ≫ công cụ:** 55% so với 5% bắt flag. Người giải được nhiều lớp mà công cụ **mù hoàn toàn** (IDOR 3/6, SSTI 2/6, deserialization 3/3, privilege escalation 2/2, XXE, file upload, blind SQLi, NoSQLi).
- **Người lấp khoảng cách phát-hiện → khai-thác:** 8 bài XSS công cụ *phát hiện* nhưng không bắt flag → người bắt được 6/8 (1 bài xem writeup).
- **Con người KHÔNG tự giải 071/083 (SQLi)** — 2 bài chỉ sqlmap-tự-chạy bắt được. Theo logic mới (nhánh B đã bỏ), 2 bài này **KHÔNG tính cho nhánh A** → nhánh A = **55% (22/40)**. (Hệ quả: 083 thành ca **AI-local vượt nhánh A**.)
- **Trần ở bài khó:** tự giải chỉ 25% (2/8); 3/6 bài xem writeup là bài khó → người cũng chạm trần năng lực ở mức hard.
- **So AI local (4 bài chung):** người 1/4 (064), AI 0/4. Cả hai cùng thất bại ở 037, 061, 080.

## Threats to Validity (bắt buộc nêu trong bài)
1. **Người giải trong nhóm, không độc lập** — lệch giao thức `report_A.md` §0 (yêu cầu người ngoài nhóm chưa thấy bài).
2. **Thiếu file log Burp xuất ra cho 37/40 bài** (chỉ 005/006/047 đo trực tiếp trong phiên). Các phiên **được một thành viên nhóm giám sát trực tiếp và ghi chú thời gian/số bước tại chỗ**, nên số liệu được chứng thực bằng quan sát của giám sát viên — **không phải báo cáo hồi cứu**. Hạn chế là không có file HTTP-history của Burp làm **artifact độc lập**. → RQ2 (thời gian/công sức) dựa trên ghi chú giám sát; **nên lưu log Burp từ các phiên sau** để có bằng chứng xuất ra.
3. **6 bài xem writeup** → loại khỏi chỉ số chính (báo cáo minh bạch ở chỉ số phụ).
4. **Thiếu artifact log độc lập.** Quá trình khai thác được **giám sát viên quan sát trực tiếp** (nên không phải chỉ "tính ra flag" từ công thức công khai `sha256(tên bài)`); tuy vậy một hội đồng khắt khe vẫn ưa có **log công cụ xuất ra** làm bằng chứng. Giảm thiểu: xuất Burp HTTP-history từ nay, và/hoặc chạy lại vài bài có-log để neo độ tin cậy.
5. **Một người giải duy nhất** → kết quả phản ánh năng lực một cá nhân, không đại diện "người pentest" nói chung.
