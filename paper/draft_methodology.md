# Nháp — Methodology (mục 3)

> Bản nháp để ghép vào `OUTLINE.md` mục 3. Mô tả thiết kế và giao thức đúng như đã triển khai trên máy. Nhánh B đã chạy thật (40/40); nhánh A và C mô tả ở mức *giao thức đã chốt* — khi chạy xong chỉ cần bổ sung số, không phải đổi thiết kế. Các hằng số (seed, phiên bản công cụ, model) lấy từ `project/` và `docs/`.

---

## 3. Methodology

Nghiên cứu so sánh **ba cách tiếp cận kiểm thử xâm nhập ứng dụng web** trên cùng một bộ mục tiêu, cùng tiêu chí chấm và cùng giới hạn tài nguyên, nhằm cô lập đóng góp của (i) tự động hóa và (ii) hỗ trợ bằng mô hình ngôn ngữ lớn (LLM). Thiết kế là *within-subject*: mọi nhánh chạy trên đúng cùng 40 mục tiêu.

### 3.1 Ba nhánh A / B / C

| Nhánh | Tên | Con người | Tự động hóa | LLM | Công cụ chính |
|---|---|---|---|---|---|
| **A** | Thủ công | Có (chuyên viên) | Không | Không | Burp Suite Community + thao tác tay |
| **B** | Tự động, không AI | Không (sau khi phát lệnh) | Có | Không | nuclei, ffuf, sqlmap, dalfox, SSTImap |
| **C1** | AI — mô hình local | Có (vòng lặp người) | Một phần | Có (local) | PentestGPT (legacy) + Ollama `qwen2.5:7b` |
| **C2** | AI — mô hình API | Có (vòng lặp người) | Một phần | Có (thương mại) | PentestGPT (legacy) + API |

- **Nhánh A** đại diện pentest truyền thống: chuyên viên tự quan sát request/response qua proxy và thao tác tay, không dùng scanner tự động và không dùng AI.
- **Nhánh B** là baseline *tự động hóa thuần* (không AI): một pipeline **cố định, giống hệt nhau cho mọi bài**, để khác biệt giữa các bài chỉ phản ánh năng lực công cụ chứ không phải tinh chỉnh của người.
- **Nhánh C** là pentest *có AI hỗ trợ* dùng PentestGPT ở chế độ *legacy* (trợ lý đề xuất, con người thực thi lệnh). Tách thành **C1 (mô hình local)** và **C2 (mô hình thương mại qua API)** để so sánh năng lực và, quan trọng hơn, để đo **tỷ lệ từ chối tác vụ** của bộ lọc an toàn thương mại. Trong phạm vi báo cáo này, C1-local được ưu tiên chạy trước; C2-API là tùy chọn mở rộng (xem 3.6).

Việc chọn PentestGPT ở chế độ trợ lý (thay vì chế độ agent tự trị) là có chủ đích: nó cho phép đo `manual_interventions` — số lần con người phải can thiệp — vốn là một chỉ số trung tâm để trả lời câu hỏi "AI *thay thế* hay *tăng tốc*".

### 3.2 Bộ mục tiêu (benchmark)

Ta dùng **XBOW validation-benchmarks** — 104 bài CTF ứng dụng web, mỗi bài là một dịch vụ đóng gói bằng Docker với một lỗ hổng cài sẵn và một flag bí mật. Từ 104 bài, ta rút **mẫu phân tầng 40 bài** theo độ khó bằng seed cố định (`seed=42`) để tái lập: **14 easy, 18 medium, 8 hard** (lấy trọn cả 8 bài hard vì số lượng ít). Mỗi bài được gán một hoặc nhiều nhãn `vuln_category` từ metadata gốc (xss, sqli, ssti, idor, lfi, command_injection, insecure_deserialization, xxe, …).

Để xử lý vấn đề **benchmark bão hòa** (XBOW đã được công bố rộng rãi, nhiều khả năng nằm trong dữ liệu huấn luyện của các LLM), ta chuẩn bị **hai biến thể cho mỗi bài**:
- **Bản gốc (original):** như phát hành.
- **Bản hint-free:** fork của KeygraphHQ đã *xóa các gợi ý lời giải* trong đề (chú thích, tên biến gợi ý, README), giữ nguyên lỗ hổng và flag.

Nhánh C chạy trên **cả hai biến thể** để đo *hiệu ứng học thuộc* (xem 3.4). Nhánh A và B chỉ chạy bản gốc: chuyên viên và scanner không "đọc" gợi ý trong mã nguồn theo cách một LLM có thể đã ghi nhớ, nên biến thể hint-free không làm thay đổi điều kiện của hai nhánh này.

**Tiêu chí giải (ground truth).** Flag mỗi bài tuân theo công thức tất định `FLAG{sha256(TÊN_BÀI_viết_HOA)}`; ta đã xác minh công thức này **khớp với pipeline `make` chính thức** của benchmark. Một bài được tính **giải được (solved) khi và chỉ khi flag thu được khớp chính xác** chuỗi chuẩn — không chấm điểm bộ phận.

### 3.3 Hạ tầng chạy và tính tái lập

Toàn bộ 104 bài (và cả hai biến thể của mẫu 40) được dựng bằng một **harness tự động** (`build_target.py`): nó build image, khởi chạy, dò cổng web, chờ dịch vụ trả HTTP hợp lệ rồi ghi URL vào `targets.csv`. Hai điểm kỹ thuật cần khai báo vì ảnh hưởng tính tái lập:

1. **Vá tương thích Docker 2026.** Benchmark phát hành năm 2024; nhiều image nền đã hết vòng đời (EOL). Harness tự áp một tập bản vá *chỉ về mặt tương thích môi trường* — nâng phiên bản image hỏng digest, trỏ apt sang `archive.debian.org`, chuẩn hóa xuống dòng CRLF→LF cho script khởi động, đổi cổng cố định sang cổng ngẫu nhiên để tránh xung đột — và **ghi lại toàn bộ vào `patches.log`**. Các bản vá **không chạm vào lỗ hổng hay flag**.
2. **Cô lập biến thể.** Vì thư mục bản gốc và hint-free trùng tên, Docker Compose mặc định sinh cùng tên project → đè container/image lẫn nhau. Harness khắc phục bằng cách đặt tên project tường minh `-p <mã_bài>-<biến_thể>` trên mọi lệnh compose, đảm bảo hai biến thể chạy song song với image riêng biệt.
3. **Chấm "sống" theo HTTP thay vì healthcheck.** Nhiều bài cũ khai báo healthcheck đã lỗi thời (mongosh, haproxy, Flask-debug) nên báo *unhealthy* dù web vẫn phục vụ. Harness bỏ qua healthcheck của compose, thay bằng thăm dò HTTP trực tiếp tới khi dịch vụ trả lời (tối đa 120 giây).

**Phần cứng/môi trường:** Docker engine 29.8.1; mô hình local chạy bằng Ollama với `qwen2.5:7b` lượng tử hóa 4-bit trên GPU NVIDIA RTX A1000.

### 3.4 Chỉ số đo

Mỗi lượt chạy (một bài × một nhánh × một biến thể) ghi một dòng vào `results.csv` với các chỉ số:

- **solve rate** — tỷ lệ bắt được flag (tiêu chí chính, so sánh cả ba nhánh).
- **time** — thời gian tới khi giải/tới hạn.
- **num_steps** — số bước thao tác (nhánh A/C).
- **tokens_used** — token tiêu thụ (nhánh C).
- **manual_interventions** — số lần con người can thiệp (nhánh C, để phân biệt *trợ lý* với *tự trị*).
- **llm_refused** — mô hình có từ chối tác vụ không (nhánh C; chỉ số này tự thân là một kết quả, xem 3.6).
- **detected** *(riêng nhánh B)* — công cụ có phát tín hiệu lỗ hổng không, kể cả khi không khai thác tới flag. Đây là chỉ số phụ, đo bằng heuristic khớp chuỗi trên output công cụ; chỉ áp dụng cho nhánh B và được đọc như *cận trên lạc quan* của năng lực nhận diện tự động.

**Hiệu ứng học thuộc (memorization).** Với nhánh C, ta tính `Δ_học_thuộc = solve_rate(gốc) − solve_rate(hint-free)`. Δ lớn cho thấy mô hình dựa vào việc đã *thấy* lời giải hơn là *tự tìm*. Đây là một đóng góp chính, trực tiếp giải quyết vấn đề benchmark bão hòa.

Phân tích được tự động hóa bằng `analyze.py` (pandas): Bảng 1 (tổng hợp theo nhánh), Bảng 2 (theo độ khó), Bảng 3 (theo loại lỗ hổng), Bảng 3b (phát hiện vs bắt flag — nhánh B), Bảng 4 (hiệu ứng học thuộc — nhánh C), cùng các biểu đồ tương ứng. Dòng chưa chạy (ô `solved` để trống) bị loại khỏi thống kê chứ không bị tính là thất bại.

### 3.5 Giao thức chạy

- **Giới hạn thời gian 30 phút/bài** cho mọi nhánh, để công bằng và phản ánh ràng buộc thực tế. Nhánh B thực thi giới hạn này theo ngân sách cộng dồn qua từng bước công cụ.
- **Pipeline cố định của nhánh B:** nuclei → ffuf → bộ khai thác chuyên biệt ánh xạ *cố định* từ nhãn lỗ hổng (SQLi/NoSQLi→sqlmap, XSS→dalfox, SSTI→SSTImap). Không tinh chỉnh theo từng bài; nếu đổi cấu hình thì đổi cho **cả 40 bài** rồi chạy lại toàn bộ. Bộ khai thác quét **tất cả** nhãn của bài (không chỉ nhãn đầu).
- **Nhánh A/C:** chuyên viên bật target, bấm giờ, thao tác tới khi lấy được flag hoặc hết giờ, rồi ghi số liệu. Nhánh C lặp lại toàn bộ trên biến thể hint-free.

### 3.6 Giảm thiên lệch và các ràng buộc triển khai

- **Chống rò rỉ giữa người và AI:** cùng một người **không** làm cả nhánh A và nhánh C trên **cùng một bài** (tránh việc kinh nghiệm từ lần thủ công giúp cho lần có AI). Thứ tự bài được xáo trộn; áp dụng che mù một phần nơi khả thi.
- **Bộ lọc an toàn thương mại (ràng buộc thực tế, không phải sự cố):** mô hình thương mại có thể **từ chối** tác vụ pentest vì phân loại an toàn mạng. Ta không xem đây là lỗi mà **đo như một kết quả** qua cột `llm_refused`. Vì lý do này, C1-local (ít bị từ chối, dữ liệu đảm bảo) là nhánh AI chủ lực; C2-API là mở rộng tùy nguồn lực, và tỷ lệ từ chối của nó là một phát hiện về rào cản triển khai.
- **Chi phí:** token/chi phí của nhánh C được ghi nhận để bàn về tính khả thi vận hành.
