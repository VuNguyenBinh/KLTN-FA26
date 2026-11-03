# Nháp — Results & Discussion (phần công cụ tự động của nhánh Truyền thống)

> Bản nháp để ghép vào `OUTLINE.md` mục 4 (Results) và 5 (Discussion). Số liệu lấy từ `project/results/results.csv` (nhãn `B_auto`, 40 bài gốc) và `analyze.py` (Bảng 1, 2, 3, 3b).
>
> ⚠️ **Cấu trúc 3 nhánh (2026-11-03) — bản chốt ở `THESIS_FULL.md`:** "nhánh B" trong văn dưới = **tầng công cụ tự động của nhánh Truyền thống** (`B_auto`, trần tự-động-hoá); "nhánh A" = tầng người; "nhánh C" = nhánh AI. Chỗ `[[chờ A/C]]` = chờ số nhánh người và nhánh AI.

---

## 4. Results (phần nhánh B)

### 4.1 Tổng quan nhánh B
Nhánh B (tự động, không AI) được chạy với **cùng một cấu hình cố định** trên toàn bộ 40 bài mẫu, giới hạn 30 phút/bài. Pipeline gồm nuclei (quét template) → ffuf (fuzz path) → bộ khai thác chuyên biệt theo loại lỗ hổng (sqlmap cho SQLi/NoSQLi, dalfox cho XSS, SSTImap cho SSTI). Không công cụ nào dùng mô hình ngôn ngữ.

Ta báo cáo **hai chỉ số tách biệt**:
- **Tỷ lệ bắt flag (capture rate)** — tiêu chí giải chính thức của benchmark (flag khớp chính xác). Đây là chỉ số dùng để so sánh với nhánh A và C.
- **Tỷ lệ phát hiện (detection rate)** — công cụ có phát tín hiệu về sự tồn tại của lỗ hổng hay không, dù không khai thác được đến flag. Chỉ số này chỉ áp dụng cho nhánh B (nhánh thủ công và AI không có tín hiệu scanner tách rời) và được đo bằng heuristic khớp chuỗi trên output công cụ.

**Bảng 2 (nhánh B).** Trên 40 bài, nhánh B **bắt được flag 2/40 (5,0%)** nhưng **phát hiện lỗ hổng 11/40 (27,5%)**. Thời gian trung bình 2,7 phút/bài.

| | n | Bắt flag | Phát hiện |
|---|---|---|---|
| Nhánh B (toàn mẫu) | 40 | 5,0% | 27,5% |

### 4.2 Theo độ khó
Khoảng cách phát hiện–bắt flag tồn tại ở mọi mức độ khó (Hình `fig_detect_vs_capture`):

| Độ khó | n | Bắt flag | Phát hiện |
|---|---|---|---|
| Easy | 14 | 14,3% | 50,0% |
| Medium | 18 | 0,0% | 11,1% |
| Hard | 8 | 0,0% | 25,0% |

Toàn bộ 2 lần bắt flag đều nằm ở nhóm easy; nhánh B không giải được bài medium hay hard nào. Tỷ lệ phát hiện tập trung ở nhóm easy (50%) rồi tụt mạnh ở medium (11,1%); con số hard (25%) nhỉnh hơn medium chỉ vì mẫu hard nhỏ (2/8, đều là XSS mà dalfox bắt được `[POC]`) chứ không phản ánh scanner mạnh hơn ở bài khó.

### 4.3 Theo loại lỗ hổng
**Bảng 3 / 3b (nhánh B).** Sắp theo tỷ lệ phát hiện:

| Loại lỗ hổng | n | Phát hiện | Bắt flag |
|---|---|---|---|
| SQLi | 2 | 100% | **100%** |
| CVE | 1 | 100% | 0% |
| XSS | 10 | 80% | 0% |
| SSTI | 6 | 0% | 0% |
| IDOR | 6 | 0% | 0% |
| Insecure deserialization | 3 | 0% | 0% |
| Command injection | 2 | 0% | 0% |
| Privilege escalation | 2 | 0% | 0% |
| Blind SQLi | 1 | 0% | 0% |
| LFI / XXE / NoSQLi / crypto / default-creds / file-upload / smuggling | mỗi loại 1 | 0% | 0% |

Chỉ **ba lớp** cho tín hiệu phát hiện khác 0: SQLi (sqlmap), XSS (dalfox báo `[POC]`) và CVE (một template nuclei đúng, không phải banner generic). Trong đó chỉ **SQLi** bắt được flag — sqlmap tự liệt kê và dump cơ sở dữ liệu nên lấy flag trọn gói trong một bước. Đáng chú ý: **SSTI phát hiện 0/6** — sau khi sửa lỗi crash cờ `-B`, SSTImap chạy `--crawl` thật nhưng không tự tìm được injection point ở bài nào; IDOR cũng 0/6. Các lớp phụ thuộc ngữ nghĩa/đa bước gần như vô hình với bộ công cụ cố định.

---

## 5. Discussion (phần nhánh B)

### 5.1 Phát hiện cốt lõi: khoảng cách phát hiện ≫ khai thác
Kết quả nổi bật nhất của nhánh B là **khoảng cách giữa phát hiện (27,5%) và bắt flag (5%)** — chênh khoảng 5,5 lần. Tự-động-không-AI *nhận ra lớp lỗ hổng* ở một phần tư số bài, nhưng gần như không tự *xâu chuỗi các bước khai thác* để đạt tiêu chí giải. Ngoại lệ duy nhất là SQLi, nơi công cụ chuyên biệt (sqlmap) đã đóng gói sẵn chuỗi "phát hiện → dump → lấy dữ liệu" thành một quy trình tự động.

Khoảng cách này thể hiện rõ nhất ở **XSS**: dalfox báo `[POC]` ở 8/10 bài nhưng không bắt được flag nào — rào cản không phải nhận diện mà là bước khai thác sau đó (dàn dựng ngữ cảnh để đánh cắp token/thực thi trong trình duyệt), vốn cần suy luận theo ngữ cảnh từng ứng dụng. Mặt khác, nhiều lớp **thậm chí không được phát hiện**: SSTI 0/6 (SSTImap crawl nhưng không tự định vị được điểm tiêm), IDOR 0/6, deserialization 0/3. Như vậy tự-động-không-AI vừa hụt ở *khai thác* (XSS) vừa hụt ở cả *phát hiện* (SSTI/IDOR) — mở ra hai chỗ mà nhánh C (AI) có thể tạo khác biệt.

### 5.2 Vì sao nhiều lớp phát hiện 0%
Phần lớn các lớp có tỷ lệ phát hiện 0%: IDOR (0/6), SSTI (0/6), insecure deserialization (0/3), command injection (0/2), privilege escalation (0/2), cùng XXE, NoSQLi, LFI, crypto, default-creds (mỗi loại 0/1). Chia làm hai nhóm nguyên nhân. (i) **Phụ thuộc ngữ nghĩa nghiệp vụ** — IDOR, privilege escalation, logic: để lộ cần hiểu quan hệ chủ sở hữu–tài nguyên và thử định danh của người khác; signature tĩnh của nuclei/ffuf không mô tả được. (ii) **Giới hạn của công cụ không-AI dù có bộ khai thác chuyên biệt** — SSTI là ví dụ rõ: SSTImap *có* chạy (`--crawl 5`) nhưng không tự định vị được tham số tiêm ở bài nào trong 6 bài, nên phát hiện 0/6. Cả hai nhóm đều củng cố ranh giới năng lực của tự động hóa dựa-chữ-ký và là điểm đối chiếu tự nhiên cho nhánh C (AI) — nơi suy luận ngữ cảnh được kỳ vọng tạo khác biệt ở **cả khâu phát hiện lẫn khai thác**.

### 5.3 Ý nghĩa cho so sánh ba nhánh
`[[chờ A/C]]` Khi có số nhánh A (thủ công) và C (AI), diễn giải dự kiến:
- Nếu nhánh C bắt flag ở lớp mà B *phát hiện nhưng không khai thác được* (XSS), thì giá trị tăng thêm của AI nằm đúng ở **bước khai thác đa bước**, không phải khâu nhận diện.
- Nếu nhánh C *phát hiện và/hoặc khai thác* được các lớp mà B **không hề phát hiện** (SSTI, IDOR, logic), thì AI còn bù cả ở **khâu nhận diện** — một thông điệp thực tiễn mạnh hơn cho đội vận hành.
- Nếu nhánh C cũng kẹt ở các lớp phụ thuộc ngữ nghĩa giống B, kết luận sẽ là AI *tăng tốc* chứ chưa *thay thế* được kiểm thử thủ công.
- Chênh lệch bắt flag giữa B và C ở riêng nhóm SQLi dự kiến nhỏ (cả hai đều mạnh), nên khác biệt thật sự sẽ lộ ở các lớp khác.

### 5.4 Tính công bằng của baseline nhánh B
Nhánh B được thiết kế là baseline *đáng tin*, không phải strawman: ngoài scanner tổng quát (nuclei/ffuf) còn có bộ khai thác chuyên biệt không-AI (sqlmap/dalfox/SSTImap) cho đúng các lớp chiếm đa số mẫu (XSS, SSTI, SQLi). Dù vậy, cần nêu rõ hai giới hạn khi diễn giải khoảng cách B–C (xem Threats to Validity): (i) chỉ 21/40 bài có bộ khai thác chuyên biệt, 19/40 chỉ dựa nuclei+ffuf, nên tỷ lệ bắt flag thấp ở IDOR/logic/deserialization một phần do *giới hạn công cụ* chứ không hoàn toàn do bản chất "tự động hóa"; (ii) chỉ số phát hiện là heuristic khớp chuỗi, nên đọc như *cận trên lạc quan* của năng lực nhận diện.
