# Nháp — Results & Discussion (phần nhánh B)

> Bản nháp để ghép vào `OUTLINE.md` mục 4 (Results) và 5 (Discussion). Số liệu lấy từ `project/results/results.csv` (nhánh B, 40 bài gốc, chạy 2026-11-02) và `analyze.py` (Bảng 1, 2, 3, 3b). Chỗ `[[chờ A/C]]` là nơi điền số nhánh A và C khi có — hiện chỉ có nhánh B nên các câu so sánh để ở dạng khung.

---

## 4. Results (phần nhánh B)

### 4.1 Tổng quan nhánh B
Nhánh B (tự động, không AI) được chạy với **cùng một cấu hình cố định** trên toàn bộ 40 bài mẫu, giới hạn 30 phút/bài. Pipeline gồm nuclei (quét template) → ffuf (fuzz path) → bộ khai thác chuyên biệt theo loại lỗ hổng (sqlmap cho SQLi/NoSQLi, dalfox cho XSS, SSTImap cho SSTI). Không công cụ nào dùng mô hình ngôn ngữ.

Ta báo cáo **hai chỉ số tách biệt**:
- **Tỷ lệ bắt flag (capture rate)** — tiêu chí giải chính thức của benchmark (flag khớp chính xác). Đây là chỉ số dùng để so sánh với nhánh A và C.
- **Tỷ lệ phát hiện (detection rate)** — công cụ có phát tín hiệu về sự tồn tại của lỗ hổng hay không, dù không khai thác được đến flag. Chỉ số này chỉ áp dụng cho nhánh B (nhánh thủ công và AI không có tín hiệu scanner tách rời) và được đo bằng heuristic khớp chuỗi trên output công cụ.

**Bảng 2 (nhánh B).** Trên 40 bài, nhánh B **bắt được flag 2/40 (5,0%)** nhưng **phát hiện lỗ hổng 22/40 (55,0%)**. Thời gian trung bình 3,1 phút/bài.

| | n | Bắt flag | Phát hiện |
|---|---|---|---|
| Nhánh B (toàn mẫu) | 40 | 5,0% | 55,0% |

### 4.2 Theo độ khó
Khoảng cách phát hiện–bắt flag tồn tại ở mọi mức độ khó (Hình `fig_detect_vs_capture`):

| Độ khó | n | Bắt flag | Phát hiện |
|---|---|---|---|
| Easy | 14 | 14,3% | 64,3% |
| Medium | 18 | 0,0% | 55,6% |
| Hard | 8 | 0,0% | 37,5% |

Toàn bộ 2 lần bắt flag đều nằm ở nhóm easy; nhánh B không giải được bài medium hay hard nào. Tỷ lệ phát hiện giảm đều theo độ khó (64% → 56% → 38%), phù hợp giả thuyết: bài khó che giấu điểm vào tốt hơn nên scanner tín hiệu yếu hơn.

### 4.3 Theo loại lỗ hổng
**Bảng 3 / 3b (nhánh B).** Sắp theo tỷ lệ phát hiện:

| Loại lỗ hổng | n | Phát hiện | Bắt flag |
|---|---|---|---|
| SQLi | 2 | 100% | **100%** |
| SSTI | 6 | 100% | 0% |
| Blind SQLi | 1 | 100% | 0% |
| LFI / CVE / File-upload | mỗi loại 1 | 100% | 0% |
| XSS | 10 | 80% | 0% |
| Privilege escalation | 2 | 50% | 0% |
| Insecure deserialization | 3 | 33% | 0% |
| IDOR | 6 | 0% | 0% |
| Command injection | 2 | 0% | 0% |
| NoSQLi / XXE / crypto / default-creds / smuggling | mỗi loại 1 | 0% | 0% |

Chỉ **SQLi** cho tỷ lệ bắt flag khác 0: sqlmap tự liệt kê và dump cơ sở dữ liệu nên lấy được flag trọn gói trong một bước. Mọi lớp còn lại có tỷ lệ bắt flag 0%, kể cả những lớp được phát hiện 100% (SSTI) hoặc 80% (XSS).

---

## 5. Discussion (phần nhánh B)

### 5.1 Phát hiện cốt lõi: khoảng cách phát hiện ≫ khai thác
Kết quả nổi bật nhất của nhánh B là **khoảng cách lớn giữa phát hiện (55%) và bắt flag (5%)**. Tự-động-không-AI *nhận ra lớp lỗ hổng* ở hơn một nửa số bài, nhưng gần như không tự *xâu chuỗi các bước khai thác* để đạt tiêu chí giải. Ngoại lệ duy nhất là SQLi, nơi công cụ chuyên biệt (sqlmap) đã đóng gói sẵn chuỗi "phát hiện → dump → lấy dữ liệu" thành một quy trình tự động.

Điều này định hình lại cách đọc con số 5%: nó **không** có nghĩa scanner "mù" với 95% số bài, mà là scanner *thấy nhưng không với tới*. Với SSTI (phát hiện 6/6 nhưng bắt 0/6) và XSS (8/10 nhưng 0/10), rào cản không phải nhận diện mà là bước khai thác sau đó — xây payload thoát sandbox template, hoặc dàn dựng ngữ cảnh để đánh cắp token/thực thi trong trình duyệt — vốn cần suy luận theo ngữ cảnh từng ứng dụng.

### 5.2 Vì sao một số lớp phát hiện 0%
Nhóm IDOR (0/6), command injection (0/2), XXE, NoSQLi, logic/crypto có tỷ lệ phát hiện 0%. Đây là các lỗ hổng **phụ thuộc ngữ nghĩa nghiệp vụ**: để lộ IDOR cần hiểu quan hệ chủ sở hữu–tài nguyên và thử định danh của người khác; signature tĩnh của nuclei/ffuf không mô tả được. Kết quả này củng cố ranh giới năng lực của tự động hóa dựa-chữ-ký, và là điểm đối chiếu tự nhiên cho nhánh C (AI) — nơi suy luận ngữ cảnh được kỳ vọng tạo khác biệt.

### 5.3 Ý nghĩa cho so sánh ba nhánh
`[[chờ A/C]]` Khi có số nhánh A (thủ công) và C (AI), diễn giải dự kiến:
- Nếu nhánh C bắt flag ở các lớp mà B *phát hiện nhưng không khai thác được* (SSTI, XSS), thì giá trị tăng thêm của AI nằm đúng ở **bước khai thác đa bước**, không phải ở khâu nhận diện — một thông điệp thực tiễn rõ ràng cho đội vận hành.
- Nếu nhánh C cũng kẹt ở các lớp phụ thuộc ngữ nghĩa (IDOR, logic) giống B, kết luận sẽ là AI *tăng tốc* chứ chưa *thay thế* được kiểm thử thủ công.
- Chênh lệch bắt flag giữa B và C ở riêng nhóm SQLi dự kiến nhỏ (cả hai đều mạnh), nên khác biệt thật sự sẽ lộ ở các lớp khác.

### 5.4 Tính công bằng của baseline nhánh B
Nhánh B được thiết kế là baseline *đáng tin*, không phải strawman: ngoài scanner tổng quát (nuclei/ffuf) còn có bộ khai thác chuyên biệt không-AI (sqlmap/dalfox/SSTImap) cho đúng các lớp chiếm đa số mẫu (XSS, SSTI, SQLi). Dù vậy, cần nêu rõ hai giới hạn khi diễn giải khoảng cách B–C (xem Threats to Validity): (i) chỉ 21/40 bài có bộ khai thác chuyên biệt, 19/40 chỉ dựa nuclei+ffuf, nên tỷ lệ bắt flag thấp ở IDOR/logic/deserialization một phần do *giới hạn công cụ* chứ không hoàn toàn do bản chất "tự động hóa"; (ii) chỉ số phát hiện là heuristic khớp chuỗi, nên đọc như *cận trên lạc quan* của năng lực nhận diện.
