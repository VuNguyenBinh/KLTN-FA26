# Các bài báo / nguồn liên quan và đóng góp cho đồ án

> **Dành cho:** nhóm làm KLTN + phần Related Work của bài báo.
> **Nguồn:** danh mục [1]–[10] đã xác minh trong `paper/THESIS_FULL.md` (References) và `paper/draft_intro_relatedwork.md`. File này bổ sung **tổ chức/đại học** và **đóng góp cụ thể cho đồ án**.
> ✅ **Affiliation đã tra cứu web (2026-11-06)** từ trang USENIX/ACL/arXiv/trang trường. Chỗ còn "(cần xác minh)" là đồng tác giả lẻ chưa rõ đơn vị — tên bài/tác giả/nơi đăng khớp References đã xác minh.

---

## A. Công cụ & bộ benchmark nền (hạ tầng trực tiếp của đồ án)

### [1] PentestGPT — *Evaluating and Harnessing Large Language Models for Automated Penetration Testing*
- **Tác giả:** G. Deng, Y. Liu, V. Mayoral-Vilches, P. Liu, Y. Li, Y. Xu, T. Zhang, Y. Liu, M. Pinzger, S. Rass.
- **Tổ chức:** **Nanyang Technological University (NTU, Singapore)** — nhóm chính (Deng, Yi Liu, Tianwei Zhang, Yang Liu…); **Alias Robotics** + **Alpen-Adria-Universität Klagenfurt (Áo)** (Mayoral-Vilches, Pinzger); **Johannes Kepler University Linz (Áo)** (Stefan Rass). *(Xác nhận qua trang USENIX + A*STAR OAR.)*
- **Nơi đăng:** Proc. 33rd USENIX Security Symposium, 2024, pp. 847–864.
- **Đóng góp cho đồ án:** là **scaffold (khung chạy AI) chính** của cả hai nhánh AI (C1 local + C2 API) — chế độ trợ lý, cây nhiệm vụ PTT, lệnh `discuss`. Đồ án **giữ nguyên PentestGPT, chỉ đổi model** để tách hiệu ứng *quy mô model*. Cũng là nguồn gốc câu hỏi "LLM hỗ trợ pentest tới đâu".

### [2] XBOW Validation Benchmarks
- **Tác giả/tổ chức:** XBOW Engineering (công ty, Hoa Kỳ).
- **Loại:** bộ benchmark mã nguồn mở (không phải paper học thuật). 2024. https://github.com/xbow-engineering/validation-benchmarks
- **Đóng góp cho đồ án:** **bộ bài mục tiêu** — 104 thử thách CTF web đóng gói Docker, mỗi bài 1 lỗ hổng + 1 flag theo công thức `FLAG{sha256(UPPER(bench-id))}`. Đồ án lấy **mẫu phân tầng 40 bài** (seed=42) từ đây làm nền cho mọi nhánh.

### [3] KeygraphHQ — XBOW Validation Benchmarks (bản fork xóa gợi ý / hint-free)
- **Tác giả/tổ chức:** **Keygraph** — công ty đứng sau trình pentest AI mã nguồn mở "Shannon" (bản fork dùng cho Shannon Lite, chế độ white-box). *(Xác nhận qua GitHub KeygraphHQ.)*
- **Loại:** fork dữ liệu (xóa tên biến/chú thích/đường dẫn/tiêu đề app/cấu hình Dockerfile). 2025. https://github.com/KeygraphHQ/xbow-validation-benchmarks
- **Đóng góp cho đồ án:** cung cấp **biến thể hint-free** (bỏ chú thích/tên gợi ý/README, giữ nguyên lỗ hổng + flag) → là công cụ **đo Δ học thuộc (memorization)** cho RQ4 — đóng góp cốt lõi chống benchmark bão hòa.

---

## B. Bằng chứng & động lực (năng lực LLM pentest, khoảng trống)

### [4] *LLM Agents can Autonomously Exploit One-day Vulnerabilities*
- **Tác giả:** R. Fang, R. Bindu, A. Gupta, D. Kang.
- **Tổ chức:** University of Illinois Urbana-Champaign (UIUC), Hoa Kỳ.
- **Nơi đăng:** arXiv:2404.08144, 2024.
- **Đóng góp cho đồ án:** bằng chứng sớm rằng tác tử LLM **có thể** khai thác lỗ hổng thật khi được cho mô tả CVE → vừa tạo động lực đề tài, vừa nêu **rủi ro nhiễm dữ liệu/học thuộc** (vì sao cần hint-free).

### [5] AutoPenBench — *A Vulnerability Testing Benchmark for Generative Agents*
- **Tác giả:** L. Gioacchini, A. Delsanto, I. Drago, M. Mellia, G. Siracusano, R. Bifulco.
- **Tổ chức:** **Università di Torino (University of Turin, Ý)** — Gioacchini, Mellia, Drago (⚠️ **KHÔNG phải** Politecnico di Torino như ghi nhầm trước đó); **NEC Laboratories Europe** — Siracusano, Bifulco. *(Turin xác nhận qua arXiv PDF; NEC theo affiliation đã biết của 2 đồng tác giả.)*
- **Nơi đăng:** EMNLP 2025 (Industry Track), pp. 1615–1624 (arXiv:2410.03225).
- **Đóng góp cho đồ án:** nguồn con số **~21%** cho tác tử tự trị, và — quan trọng nhất — phát hiện **biến thể có-người-hỗ-trợ vượt xa biến thể tự trị**. Đây là **điểm tựa thiết kế** cho lựa chọn *human-in-the-loop* của đồ án.

### [6] HackSynth — *LLM Agent and Evaluation Framework for Autonomous Penetration Testing*
- **Tác giả:** L. Muzsai, D. Imolai, A. Lukács.
- **Tổ chức:** **Eötvös Loránd University (ELTE), Budapest, Hungary** — AI Research Group, Institute of Mathematics. *(Xác nhận qua arXiv + email tên miền ttk.elte.hu.)*
- **Nơi đăng:** arXiv:2412.01778, 2024.
- **Đóng góp cho đồ án:** một tác tử + **khung đánh giá** pentest tự trị → điểm đối chiếu về cách dựng scaffold và cách chấm, củng cố lựa chọn giao thức/chỉ số của đồ án.

### [7] CVE-Bench — *A Benchmark for AI Agents' Ability to Exploit Real-World Web Application Vulnerabilities*
- **Tác giả:** Y. Zhu, A. Kellermann, D. Bowman, P. Li, A. Gupta, A. Danda, R. Fang, C. Jensen, E. Ihli, J. Benn, et al.
- **Tổ chức:** **University of Illinois Urbana-Champaign (UIUC), Hoa Kỳ** — lab của Daniel Kang (`uiuc-kang-lab`). *(Xác nhận qua Illinois Experts + GitHub org.)*
- **Nơi đăng:** ICML 2025 (spotlight), PMLR vol. 267, pp. 79850–79867 (arXiv:2503.17332).
- **Đóng góp cho đồ án:** benchmark lỗ hổng web thật với **tỉ lệ thành công thấp** của tác tử (≈13% zero-day, ≈25% one-day) → dùng để **định vị kết quả thấp của nhánh AI local** là *phù hợp xu hướng tài liệu*, không phải lỗi bố trí thí nghiệm. ⚠️ **Lưu ý:** `THESIS_FULL.md` đang trích "tốt nhất 12,5%" cho CVE-Bench — **đối chiếu lại** với con số web (13%/25%) trước khi nộp (có thể là setting/model cụ thể khác).

---

## C. Khảo sát & benchmark liên quan (định vị đóng góp, so sánh phương pháp)

### [8] *A Survey of LLM-Driven Penetration Testing: Taxonomy, Co-Evolution, and Open Challenges*
- **Tác giả:** Z. He, J. Dong, Z. Li, T. Chen, G. Deng, F. Luo, J. Ji, Y. Cao, X. Luo.
- **Tổ chức:** nhiều đơn vị; **Gelei Deng ở NTU Singapore** (xác nhận). Các đồng tác giả (Ting Chen, Xiapu Luo, Yuanlong Cao…) thuộc các đại học TQ/Hong Kong *(cần xác minh từng đơn vị)*.
- **Nơi đăng:** arXiv:2607.02605, 2026.
- **Đóng góp cho đồ án:** **phân loại (taxonomy)** mảng LLM-pentest → giúp **định vị đóng góp** của đồ án trong bức tranh chung và nêu "open challenges" mà đồ án chạm tới (bão hòa, đánh giá).

### [9] CTFusion — *A CTF-based Benchmark for LLM Agent Evaluation*
- **Tác giả:** D. Lee, G.-e. Bae, I. Yun.
- **Tổ chức:** **KAIST (Hàn Quốc)** — Hacking Lab của Insu Yun (`kaist-hacking/CTFusion`). *(Xác nhận qua trang Hacking Lab KAIST.)*
- **Nơi đăng:** arXiv:2605.11504; nhận tại workshop "Agents in the Wild" (ICML '26).
- **Đóng góp cho đồ án:** benchmark dựa trên CTF cho tác tử LLM → điểm so sánh về **thiết kế benchmark + vấn đề bão hòa/chấm điểm**, hỗ trợ lập luận chọn CTF web + chấm exact-match.

### [10] PentestEval — *Benchmarking LLM-based Penetration Testing with Modular and Stage-level Design*
- **Tác giả:** R. Yang, M. Cheng, G. Deng, T. Zhang, J. Wang, X. Xie.
- **Tổ chức:** **Singapore Management University (SMU)** — Yang, Cheng, Xie; **Nanyang Technological University (NTU)** — Deng, Zhang. *(Xác nhận qua arXiv; Junjie Wang chưa rõ đơn vị.)*
- **Nơi đăng:** arXiv:2512.14233, 2025.
- **Đóng góp cho đồ án:** đánh giá pentest LLM theo **từng giai đoạn (stage-level)** → củng cố cách đồ án **bóc chỉ số theo nấc** (phát hiện → khai thác → bắt flag) thay vì chỉ một tỉ lệ cuối.

---

## Ghi chú cho người viết Related Work
- **Nhóm A** = hạ tầng trực tiếp (dùng trong thí nghiệm) → trích ở Chương 3 (Phương pháp).
- **Nhóm B** = động lực + con số đối chiếu (21%, 12,5%) → trích ở Chương 2 + Chương 5 (Thảo luận, định vị kết quả).
- **Nhóm C** = định vị học thuật + so sánh thiết kế → trích ở Chương 2 (Related Work).
- **Đã tra web (2026-11-06):** affiliation chính của [1][5][6][7][9][10] + Gelei Deng ([8]) đã xác nhận. Còn **cần xác minh**: các đồng tác giả lẻ của [8] (Ting Chen, Xiapu Luo, Yuanlong Cao…), Junjie Wang ([10]), phân bổ NEC của [5].
- ⚠️ **Sửa khi dùng:** [5] AutoPenBench là **University of Turin** (KHÔNG phải Politecnico) — kiểm xem `THESIS_FULL.md`/draft có ghi nhầm không. [7] CVE-Bench: đối chiếu con số 12,5% (THESIS) với 13%/25% (web).
