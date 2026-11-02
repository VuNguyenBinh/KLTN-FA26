# Nháp — Introduction (mục 1) & Related Work (mục 2)

> Bản nháp để ghép vào `OUTLINE.md` mục 1–2. **Lưu ý trích dẫn:** các mã/đường link dưới đây lấy từ tra cứu web (tháng 11/2026) và **phải được xác minh lại** trước khi nộp — đặc biệt mã arXiv và số trang (snippet web có thể sai). Nguồn chắc chắn nhất: PentestGPT (USENIX Security 2024) và XBOW validation-benchmarks (blog XBOW 11/2024).

---

## 1. Introduction

### 1.1 Bối cảnh
Kiểm thử xâm nhập (penetration testing) ứng dụng web là một trụ cột của phòng thủ chủ động, nhưng phụ thuộc nặng vào chuyên gia: tốn thời gian, đắt đỏ và khan hiếm nhân lực. Làn sóng mô hình ngôn ngữ lớn (LLM) đã làm nảy sinh hàng loạt công cụ "pentest có AI" tuyên bố tự động hóa phần lớn quy trình, với những điểm số rất cao trên benchmark công khai.

### 1.2 Khoảng trống nghiên cứu
Vấn đề là **các điểm số đó khó so sánh và dễ bị thổi phồng**. Chúng được công bố ở những điều kiện không đồng nhất: khác mô hình, khác mức truy cập (white/black-box), có hay không mô tả lỗ hổng cho sẵn, và — quan trọng nhất — **không kiểm soát việc benchmark đã nằm trong dữ liệu huấn luyện của mô hình hay chưa**. Fang và cộng sự (2024, *"LLM Agents can Autonomously Exploit One-day Vulnerabilities"*) minh họa rõ sự mong manh này: trên bộ 15 CVE "one-day" thực, một tác nhân GPT-4 đạt tới **87%** khi được cho mô tả lỗ hổng, nhưng rơi xuống **7%** khi bỏ mô tả. Nói cách khác, phần lớn công bố hiện có **thiếu một so sánh có kiểm soát, cùng điều kiện** giữa pentest có AI, pentest tự động-không-AI, và pentest thủ công truyền thống.

### 1.3 Đóng góp
Nghiên cứu này lấp khoảng trống đó bằng một thí nghiệm **có kiểm soát** trên cùng một bộ mục tiêu. Bốn đóng góp:

1. **Thiết kế so sánh ba nhánh có kiểm soát** — thủ công (A), tự động-không-AI (B), và có-AI-hỗ-trợ (C) — chạy trên **cùng 40 mục tiêu**, cùng tiêu chí chấm (flag khớp chính xác) và cùng giới hạn thời gian, nhằm **cô lập riêng** đóng góp của tự động hóa và của AI.
2. **Bộ dữ liệu đo đa chiều** — tỷ lệ giải, thời gian, số bước, token/chi phí, số lần con người can thiệp, tỷ lệ từ chối tác vụ — phân tích theo độ khó và theo loại lỗ hổng.
3. **Đo hiệu ứng "học thuộc" (memorization)** — chạy nhánh AI trên **cả bản gốc lẫn bản đã xóa gợi ý (hint-free)** và báo cáo *delta* giữa hai bản, để định lượng mức AI dựa vào ghi nhớ lời giải so với tự tìm. Đây là cách xử lý trực tiếp vấn đề benchmark bão hòa.
4. **Bàn luận rào cản triển khai thực tế** — đo tỷ lệ bộ lọc an toàn của LLM thương mại từ chối tác vụ pentest, và chi phí vận hành.

### 1.4 Câu hỏi nghiên cứu
- **RQ1.** Pentest có-AI-hỗ-trợ hơn/kém pentest tự động-không-AI và thủ công bao nhiêu về tỷ lệ giải, thời gian và công sức con người?
- **RQ2.** Khác biệt đó thay đổi thế nào theo **độ khó** của bài?
- **RQ3.** Khác biệt đó thay đổi thế nào theo **loại lỗ hổng** (ví dụ các lớp cần suy luận đa bước vs. lớp có công cụ chuyên biệt)?
- **RQ4.** Hiệu ứng **học thuộc** lớn đến đâu (gốc vs. hint-free), và các **rào cản triển khai** (từ chối tác vụ, chi phí) đáng kể ra sao?

---

## 2. Related Work

### 2.1 Pentest tự động truyền thống (không AI)
Dòng công cụ quét tự động — scanner lỗ hổng (nuclei), fuzzer thư mục (ffuf), và các bộ khai thác chuyên biệt (sqlmap cho SQLi, dalfox cho XSS, SSTImap cho SSTI) — là nền tảng của tự động hóa không-AI. Thế mạnh của chúng là nhận diện nhanh và tin cậy các lớp lỗ hổng có chữ ký rõ ràng; điểm yếu đã được ghi nhận rộng rãi là **các lỗ hổng phụ thuộc ngữ nghĩa nghiệp vụ** (IDOR, lỗi logic) và **khai thác đa bước**, nơi không có chữ ký tĩnh nào mô tả đủ. Nghiên cứu này dùng chính các công cụ đó làm **baseline nhánh B** để định vị điểm xuất phát của tự động hóa thuần.

### 2.2 Pentest dùng LLM
**PentestGPT** (Deng và cộng sự, USENIX Security 2024) là mốc tham chiếu: nó chia bài toán thành ba mô-đun tự tương tác (reasoning / generation / parsing) để giảm mất ngữ cảnh, và báo cáo mức tăng ~228,6% so với GPT-3.5 trên một benchmark 13 mục tiêu / 182 sub-task phủ OWASP Top 10. Công trình đoạt *Distinguished Artifact Award* tại USENIX Security 2024; mã nguồn về sau được mở rộng sang chế độ agent tự trị (dẫn bằng Claude Code/Codex) và dự án kế thừa Cybersecurity AI (CAI). Nghiên cứu này dùng PentestGPT (chế độ *legacy*, trợ lý) làm **nhánh C**, chủ đích để đo được số lần con người can thiệp.

Nhiều hệ/benchmark gần đây mở rộng hướng này nhưng đồng thuận ở một kết luận: tác nhân LLM **mạnh ở CVE đã biết, yếu ở tác vụ mở, đầu-cuối**:
- **AutoPenBench** (2024) — khung đánh giá gồm 33 tác vụ (in-vitro và thực tế). Agent **tự trị** chỉ đạt **21%** tỷ lệ thành công, trong khi agent **có người hỗ trợ** đạt **64%** — một bằng chứng trực tiếp cho giá trị của con người trong vòng lặp.
- **HackSynth** (2024) — agent tự trị (mô-đun Planner + Summarizer) kèm hai bộ CTF mới gồm ~200 thử thách rút từ PicoCTF và OverTheWire; đạt tốt nhất với GPT-4o.
- **CVE-Bench** (ICML 2025, arXiv 2503.17332) — 40 CVE ứng dụng web thực (mức critical); khung agent tốt nhất chỉ giải được **tối đa ~13%**.
- Một công trình "Towards Automated Penetration Testing" (bản ACM 2024/2025) báo cáo rằng **không có trợ giúp của con người, các tác nhân hiện tại không hoàn tất nổi một bài pentest đầu-cuối nào**.

Các kết quả này — nhất là chênh lệch 21%→64% của AutoPenBench — củng cố thiết kế *trợ lý có-người-trong-vòng-lặp* (chứ không phải agent tự trị thuần) của nhánh C, và lý do đo `manual_interventions`.

### 2.3 Benchmark và vấn đề bão hòa
**XBOW validation-benchmarks** — 104 bài CTF web đóng gói Docker, phát hành công khai tháng 11/2024, phủ nhiều lớp lỗ hổng (XSS, SSTI, SQLi, IDOR, SSRF, crypto…). XBOW báo cáo tỷ lệ giải ~85% (tương đương một pentester kinh nghiệm trong một tuần). Benchmark này được chọn làm bộ mục tiêu vì tính tất định (flag exact-match), cô lập Docker và độ phủ lỗ hổng.

Chính độ phổ biến đó đặt ra vấn đề **bão hòa / rò rỉ huấn luyện**: khi một benchmark được công bố rộng, điểm số của mô hình trên nó có thể phản ánh *ghi nhớ* hơn là *năng lực tìm lỗ hổng*. Các khảo sát và nghiên cứu về *thực hành benchmark trong offensive security dùng LLM* (2025–2026) cũng cảnh báo về testbed không nhất quán, chỉ số đo thiếu chuẩn, và số lượng tác vụ web thực sự ít trong nhiều bộ dữ liệu phổ biến. Để đối phó, ta dùng **bản hint-free** (fork KeygraphHQ của XBOW, đã xóa gợi ý lời giải) song song với bản gốc và báo cáo *delta memorization* — biến hạn chế của benchmark thành một phép đo có ý nghĩa.

### 2.4 Khác biệt của nghiên cứu này
So với các công trình trên, đóng góp phân biệt là **tính so sánh có kiểm soát**: thay vì đánh giá *một* hệ AI trên *một* benchmark, ta đặt ba cách tiếp cận (thủ công / tự động-không-AI / có-AI) **cạnh nhau trên cùng mục tiêu và cùng giao thức**, tách riêng hiệu ứng *tự động hóa* khỏi hiệu ứng *AI*, và định lượng trực tiếp *học thuộc* lẫn *rào cản triển khai* — những khía cạnh mà các công bố điểm-số đơn lẻ thường bỏ qua.

---

## Nguồn
**Đã xác minh (11/2026) — dùng được:**
- **PentestGPT** — Deng, Liu, Mayoral-Vilches, P. Liu, Li, Xu, Zhang, Y. Liu, Pinzger, Rass. *USENIX Security 2024*, tr. 847–864. Distinguished Artifact Award. https://www.usenix.org/conference/usenixsecurity24/presentation/deng
- **XBOW validation-benchmarks** (104 bài CTF web, blog 11/2024): https://www.xbow.com/blog/benchmarks — repo: https://github.com/xbow-engineering/validation-benchmarks
- **Bản hint-free** (KeygraphHQ): https://github.com/KeygraphHQ/xbow-validation-benchmarks
- **Fang, Bindu, Gupta, Kang (2024)** — "LLM Agents can Autonomously Exploit One-day Vulnerabilities", arXiv **2404.08144**. 15 CVE one-day: GPT-4 87% có mô tả → 7% không mô tả. https://arxiv.org/abs/2404.08144
- **AutoPenBench (2024)** — arXiv **2410.03225**. 33 tác vụ; tự trị 21% SR, có hỗ trợ 64%. https://arxiv.org/abs/2410.03225
- **HackSynth (2024)** — arXiv **2412.01778**. ~200 thử thách (PicoCTF + OverTheWire). https://arxiv.org/abs/2412.01778
- **CVE-Bench (ICML 2025)** — arXiv **2503.17332**. 40 CVE web thực; tốt nhất ~13%. https://arxiv.org/abs/2503.17332 — poster: https://icml.cc/virtual/2025/poster/46522

**Chưa xác minh kỹ — kiểm lại trước khi trích:**
- Towards Automated Penetration Testing (ACM 2024/2025): https://dl.acm.org/doi/10.1145/3708319.3733804
- Benchmarking Practices in LLM-driven Offensive Security (2025): https://arxiv.org/abs/2504.10112
- Survey of LLM-Driven Penetration Testing (2026): mã arXiv 2607.02605 **chưa kiểm chứng được** — tra lại tiêu đề đầy đủ trước khi dùng.
