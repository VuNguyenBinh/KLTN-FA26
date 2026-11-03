# KLTN — Kế hoạch 3 tuần
**Đề tài:** Comparative Study of AI-assisted and Traditional Web Application Penetration Testing Techniques
**Mục tiêu:** Sản phẩm bảo vệ KLTN + bản thảo bài báo hội nghị (viết song song).
**Ngày bắt đầu:** 2026-11-01 — **Hạn:** ~3 tuần.

---

## 1. Câu hỏi nghiên cứu (RQ) — đây là xương sống, hội đồng sẽ hỏi

- **RQ1.** AI hỗ trợ làm thay đổi *tỷ lệ phát hiện/khai thác lỗ hổng* so với thủ công và tự động-không-AI bao nhiêu?
- **RQ2.** AI thay đổi *thời gian* và *công sức* (số bước, số lần can thiệp tay) như thế nào?
- **RQ3.** AI *mạnh/yếu* ở **loại lỗ hổng** nào? (ví dụ injection, auth, IDOR, XSS…)
- **RQ4.** *Chi phí* (token/tiền, hoặc tài nguyên máy với local) so với lợi ích ra sao?

> Đóng góp của luận văn KHÔNG phải là "làm ra AI hack". Đóng góp là **bộ dữ liệu đo + phân tích có kiểm soát** trả lời 4 RQ trên.

---

## 2. Đóng góp cốt lõi — Khung đánh giá (evaluation benchmark)

> **Khái quát.** Đóng góp trung tâm của khóa luận không nằm ở việc tạo ra một công cụ AI tấn công, mà ở chỗ **xây dựng một khung đo lường có kiểm soát và tái lập được**, cho phép so sánh công bằng ba cách tiếp cận kiểm thử xâm nhập web trên cùng một bộ bài, cùng tiêu chí chấm và cùng ràng buộc tài nguyên. Hiểu theo cách đó, sản phẩm học thuật gồm ba phần gắn liền nhau — phương pháp đo, dữ liệu thu được và phần phân tích — tất cả đều đủ chi tiết để người khác tái hiện và phản biện. Điểm mới so với bộ benchmark gốc là cách **đo mức độ "học thuộc" của mô hình**, thực hiện bằng việc cho AI làm cùng một bài ở hai phiên bản: bản gốc và bản đã xóa gợi ý.

### 2.1 Bộ target — cụ thể hóa
- **Nguồn:** XBOW *validation-benchmarks* — 104 bài CTF ứng dụng web, mỗi bài là một dịch vụ đóng gói Docker Compose với **đúng một lỗ hổng cài sẵn** và **một flag bí mật**.
- **Mẫu dùng trong luận văn:** **40 bài phân tầng theo độ khó**, chọn bằng seed cố định `seed=42` (tái lập) → **14 easy / 18 medium / 8 hard** (lấy trọn 8 bài hard vì số ít). Danh sách chốt: `project/benchmarks/sample.csv`; metadata 104 bài: `project/benchmarks/metadata.csv`.
- **Phân bố loại lỗ hổng của mẫu 40** (theo nhãn đầu): XSS 10, IDOR 6, SSTI 6, insecure_deserialization 3, command_injection 2, privilege_escalation 2, SQLi 2, và 9 lớp lẻ (blind_sqli, nosqli, xxe, cve, arbitrary_file_upload, lfi, smuggling_desync, default_credentials, crypto — mỗi loại 1). → phủ rộng cả lớp *dựa chữ ký* lẫn lớp *phụ thuộc ngữ nghĩa nghiệp vụ*.
- **Hai biến thể mỗi bài:** **bản gốc (original)** và **bản xóa-gợi-ý (hint-free)** — fork KeygraphHQ, đã bỏ chú thích/tên biến gợi ý/README nhưng **giữ nguyên lỗ hổng và flag**. Cả 80 target (40×2) đều build + chạy được (HTTP 200, flag khớp).

### 2.2 Cách dựng benchmark — cụ thể hóa (tái lập được)
- **Công thức flag (ground truth):** `FLAG{sha256(TÊN_BÀI_viết_HOA)}` — **đã xác minh khớp pipeline `make` chính thức** của benchmark (openssl ≡ hashlib).
- **Harness tự động** `project/harness/build_target.py`: build image → chạy → **tự dò cổng web** → **chờ dịch vụ trả HTTP hợp lệ** (HTTP-probe thay vì tin healthcheck cũ, tối đa 120s) → ghi URL vào `targets.csv`.
- **Vá tương thích Docker 2026** (benchmark phát hành 2024): nâng image hỏng digest, trỏ apt sang `archive.debian.org`, CRLF→LF cho script, đổi cổng cố định sang cổng ngẫu nhiên. **Mọi bản vá ghi vào `patches.log` và KHÔNG chạm vào lỗ hổng hay flag** — phải khai báo trong báo cáo.
- **Cô lập biến thể:** đặt tên project `-p <mã_bài>-<biến_thể>` trên mọi lệnh compose để bản gốc và hint-free không đè image/container của nhau.

### 2.3 Tiêu chí đánh giá — đầy đủ, để phản biện
**Chỉ số chính (so sánh cả 3 nhánh):**
- **Capture rate (tỷ lệ bắt flag)** — tiêu chí giải chính thức: flag thu được **khớp chính xác** chuỗi chuẩn, **không chấm điểm bộ phận**.

**Chỉ số phụ & bối cảnh:**
- **Detection rate — tỉ lệ phát hiện (chỉ nhánh B)** — tỉ lệ bài mà công cụ *có báo hiệu đã thấy lỗ hổng*, dù chưa khai thác tới flag. Cách đo: đọc phần chữ (output) mỗi công cụ in ra và dò những cụm từ khẳng định đặc trưng cho từng loại lỗ hổng — ví dụ dalfox in `[POC]` khi thấy XSS, sqlmap in `is vulnerable` khi thấy SQLi; thấy đúng cụm của loại đó thì tính là "đã phát hiện". Vì đây chỉ là so khớp chuỗi chữ (không phải kiểm chứng chắc chắn), con số này nên được hiểu là **mức trần lạc quan**: năng lực nhận diện thật của công cụ chỉ bằng hoặc thấp hơn, không thể cao hơn — chứ không phải một tỉ lệ chính xác tuyệt đối.
- **time** (phút/bài), **num_steps** (số bước/lượt), **tokens_used** (nhánh C).
- **manual_interventions (nhánh C)** — chỉ đếm **redirect** (người chỉnh hướng khi AI đi sai), tách khỏi **exec** (chạy lệnh máy móc, ghi ở notes); kèm **lằn ranh cứng**: người không mớm kỹ thuật/lời giải, nếu lỡ thì bài tính `solved=0`.
- **llm_refused (nhánh C)** — mô hình có từ chối tác vụ không; **bản thân tỷ lệ từ chối là một kết quả** (rào cản triển khai của LLM thương mại).
- **Δ học thuộc (memorization, nhánh C)** = `solve_rate(gốc) − solve_rate(hint-free)` — đo mức mô hình dựa vào *đã thấy lời giải* thay vì *tự suy luận*. Đây là đóng góp chính giải quyết vấn đề benchmark bão hòa.

**Phân tầng báo cáo:** mọi chỉ số bóc theo **độ khó** và **loại lỗ hổng**. Ràng buộc chung: **30 phút/bài** cho mọi nhánh. Phân tích tự động hóa bằng `project/analysis/analyze.py` → Bảng 1 (theo nhánh), 2 (độ khó), 3 (loại), 3b (phát hiện vs bắt flag — nhánh B), 4 (học thuộc — nhánh C) + biểu đồ; dòng chưa chạy bị **loại khỏi thống kê**, không tính là thất bại.

### 2.4 Vì sao khung này "đứng được" khi phản biện
- **Tái lập:** seed cố định, phiên bản công cụ ghi rõ, `patches.log`, log thô từng bài trong `logs/`, dữ liệu version-controlled trong `results.csv`.
- **Công bằng:** cùng target + cùng tiêu chí exact-match + cùng budget; nhánh B là baseline *đáng tin* (có exploiter chuyên biệt không-AI cho các lớp chiếm đa số), không phải strawman.
- **Trung thực về giới hạn:** benchmark bão hòa (xử lý bằng hint-free), chỉ 21/40 bài có exploiter chuyên biệt, detection là heuristic, nhãn lấy tag đầu là gần đúng, n nhánh C nhỏ — tất cả nêu trong *Threats to Validity*.
- **Kết quả baseline đã có để minh chứng khung chạy thật:** nhánh B hoàn tất 40/40 — bắt flag **2/40 (5%)**, phát hiện **11/40 (27,5%)** (xem `docs/ARM_B.md`).

---

## 3. Thiết kế thí nghiệm

**Biến độc lập:** phương pháp kiểm thử (3 nhánh).
**Biến phụ thuộc:** tỷ lệ giải, thời gian/bài, số bước, chi phí, loại lỗ hổng.
**Kiểm soát:** cùng bộ target, cùng giới hạn thời gian/bài, cùng tiêu chí "giải được" = tìm đúng flag.

### Ba nhánh
| Nhánh | Mô tả | Nhãn dữ liệu (`results.csv`) |
|---|---|---|
| **1 — Truyền thống (thủ công + công cụ, không AI)** | Pentest truyền thống: con người kiểm thử bằng tay (Burp/trình duyệt) **và được phép dùng công cụ tự động** (nuclei/ffuf/sqlmap/dalfox/SSTImap). Không dùng LLM ở bất kỳ khâu nào. | `A_manual` (người giải) + `B_auto` (công cụ-đơn-thuần) |
| **2 — AI local (qwen)** | Trợ lý pentest PentestGPT + **mô hình local** qua Ollama (`qwen2.5:7b`), có người trong vòng lặp | `C_ai_local` |
| **3 — AI API thương mại** | PentestGPT + **mô hình API thương mại** (DeepSeek/Qwen/…), có người trong vòng lặp | `C_ai_api` *(hoãn — làm sau)* |

> **Về việc gộp "thủ công + công cụ" thành một nhánh (2026-11-03):** đề tài so sánh *AI-assisted* với *Truyền thống*, mà pentest truyền thống thực tế là **con người dùng công cụ** — nên nhánh 1 gộp phần người (`A_manual`) và phần công cụ tự động (`B_auto`). Dữ liệu **vẫn giữ nguyên hai nhãn** `A_manual` và `B_auto`, nên vẫn tách ra được khi cần: `B_auto` đóng vai **"trần của tự động hoá"** (chỉ 5% bắt flag / 27,5% phát hiện — khoảng cách detect→exploit) như một **phân tích phụ** bên trong nhánh Truyền thống. Mức giải của nhánh 1 ở mỗi bài = *giải được nếu người hoặc công cụ giải được* (người được phép gọi cùng các công cụ đó). **Không phải chạy lại gì** — chỉ gom nhóm lại ở cấp trình bày.

### Bộ target (benchmark)
- **XBOW validation-benchmarks**: 104 bài CTF web, mỗi bài 1 Docker Compose, 1 flag, chấm exact-match.
- Chọn **mẫu phân tầng 40 bài** theo độ khó (dễ/trung/khó) để chạy kịp. Danh sách chốt lưu ở `project/benchmarks/sample.csv`.
- Giới hạn mỗi bài: **30 phút** (manual & AI), scanner tự dừng theo cấu hình.

---

## 4. Lịch chi tiết

### Tuần 1 (dựng & chốt) — ngày 1–7
- [ ] **(tay)** Bật Docker Desktop, cài Git, cài Ollama. *(Người 1)*
- [ ] Clone XBOW benchmarks, build thử 3 bài. *(Người 2)*
- [ ] Chốt mẫu 40 bài + gán độ khó. *(cả nhóm, 1 buổi)*
- [ ] Cài PentestGPT cho nhánh C (local + API). *(Người 3)*
- [ ] Chạy **pilot 3 bài** đủ cả 3 nhánh để kiểm tra quy trình ghi số liệu. *(cả nhóm)*
- [ ] Chốt template ghi dữ liệu (`results/schema`).

### Tuần 2 (chạy thật) — ngày 8–14
- [ ] Chạy 40 bài × 3 nhánh (C có 2 biến thể). Ghi log đầy đủ vào `logs/`.
- [ ] Mỗi tối: nhập số liệu vào CSV, chạy `harness/score.py` để tổng hợp.
- [ ] Giữa tuần: kiểm tra tiến độ, loại bỏ bài build lỗi (ghi lý do, không vứt im lặng).

### Tuần 3 (phân tích & viết) — ngày 15–21
- [ ] Chạy `analysis/analyze.py` → bảng + biểu đồ.
- [ ] Viết bản thảo theo `paper/OUTLINE.md`.
- [ ] Dựng slide bảo vệ (10–15 slide).
- [ ] Tập bảo vệ 2 lần, chuẩn bị Q&A.

---

## 5. Rủi ro & phương án dự phòng
| Rủi ro | Dự phòng |
|---|---|
| API thương mại từ chối tác vụ pentest (bộ lọc an toàn) | Dựa chính vào **C1 local Ollama**; C2 chỉ chạy các bài không bị chặn, báo cáo trung thực tỷ lệ bị từ chối (bản thân nó là một **kết quả nghiên cứu**). |
| Bài build lỗi trên Docker mới | Dùng bản vá tương thích tối thiểu, ghi rõ bài nào bị loại. |
| Không kịp 40 bài | Giảm còn 20–25 bài vẫn đủ ý nghĩa thống kê mô tả. |
| Máy yếu khi chạy LLM local | Dùng model 7–8B lượng tử hóa (q4); chạy tuần tự, không song song. |

---

## 6. Tiêu chí "xong" cho mỗi bài
- Flag tìm được? (Y/N) + chuỗi flag.
- Thời gian (phút), số bước/lượt tương tác.
- (Nhánh C) số token / số lần người can thiệp tay / có bị LLM từ chối không.
- Loại lỗ hổng của bài (lấy từ metadata benchmark).
- Ghi chú định tính (AI gợi ý đúng/sai chỗ nào).
