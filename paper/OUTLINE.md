# Dàn bài báo (cũng dùng làm xương sống báo cáo KLTN)
**Tiêu đề:** Comparative Study of AI-assisted and Traditional Web Application Penetration Testing Techniques

> Lưu ý về "SCI 2027": bài hội nghị thường được index trong **CPCI (Conference Proceedings Citation Index)** của Web of Science hoặc **Scopus**, không phải SCIE/SCI (vốn dành cho tạp chí). Khi chọn hội nghị, kiểm tra proceedings của nó đã *thực sự được index* ở các kỳ trước chưa (đừng tin chữ "submitted to"). Đây là điều cần xác minh sớm khi chọn nơi gửi.

---

## Abstract (~200 từ)
Vấn đề → khoảng trống (thiếu so sánh có kiểm soát giữa pentest truyền thống và có AI) → phương pháp (3 nhánh trên XBOW benchmark) → kết quả chính (số liệu) → kết luận.

## 1. Introduction
- Bối cảnh: pentest web, chi phí/khan hiếm chuyên gia, làn sóng LLM.
- Khoảng trống: nhiều công cụ AI tự báo cáo điểm cao, nhưng **thiếu so sánh có kiểm soát, cùng điều kiện** với thủ công và tự động-không-AI.
- Đóng góp (liệt kê 4 gạch đầu dòng):
  1. Thiết kế thí nghiệm **có kiểm soát** 3 nhánh (manual / automated-no-AI / AI-assisted) trên cùng benchmark.
  2. Bộ dữ liệu đo đa chiều (solve rate, time, cost, steps, manual interventions, refusal rate), phân tích theo độ khó & loại lỗ hổng.
  3. **Đo hiệu ứng "memorization"**: so sánh nhánh AI trên bản gốc vs bản hint-free (đã xóa gợi ý) để định lượng mức AI "nhớ" lời giải so với "tự tìm" — xử lý trực tiếp vấn đề benchmark bão hòa.
  4. Bàn luận rào cản triển khai thực tế: bộ lọc an toàn mạng của LLM thương mại từ chối tác vụ pentest (đo `refusal rate`) và chi phí.
- 4 câu hỏi nghiên cứu (RQ1–RQ4).

## 2. Related Work
- Công cụ pentest tự động truyền thống (scanner).
- Hệ pentest dùng LLM: **PentestGPT** (USENIX Security 2024, bản agentic mới), các hệ gần đây.
- Benchmark: **XBOW validation-benchmarks** (104 CTF web), các biến thể hint-free.
- Chỉ ra: các điểm số công bố không đồng nhất (khác model, white/black-box, có/không bỏ gợi ý) → củng cố lý do cần nghiên cứu có kiểm soát của bạn.

## 3. Methodology
- 3.1 Ba nhánh A/B/C (C1 local, C2 API) — bảng.
- 3.2 Bộ target: mẫu 40 bài XBOW, phân tầng độ khó, gán loại lỗ hổng.
- 3.3 Giao thức: giới hạn thời gian 30′/bài, tiêu chí giải = flag exact-match, cách ghi số liệu.
- 3.4 Chỉ số: solve rate, time, steps, tokens/cost, manual interventions, refusal rate.
- 3.5 Thiết lập kỹ thuật: Docker, phần cứng, model local (Ollama 7–8B q4), model API, công cụ nhánh B.
- 3.6 Giảm thiên lệch: cùng người không làm trùng nhánh A và C trên cùng bài; thứ tự ngẫu nhiên; mù một phần.

## 4. Results
- 4.1 Tổng hợp (Bảng 1 từ `analyze.py`).
- 4.2 Theo độ khó (Hình fig_by_difficulty).
- 4.3 Theo loại lỗ hổng (Bảng 3).
- 4.4 Thời gian & chi phí.
- 4.5 Tỷ lệ LLM từ chối tác vụ (phát hiện riêng, có giá trị).

## 5. Discussion
- Trả lời từng RQ bằng số liệu.
- AI mạnh ở đâu (thường: nhận diện nhanh lớp lỗ hổng phổ biến), yếu ở đâu (ví dụ blind/đa bước).
- Ý nghĩa thực tế: AI là *trợ lý tăng tốc* hay *thay thế*? Rào cản triển khai (bộ lọc an toàn, chi phí token).

## 6. Threats to Validity (cụ thể — hội đồng/phản biện sẽ hỏi)
- **Mẫu & bối cảnh:** 40 bài CTF-style (không hẳn giống web thật), 1 bộ model cụ thể; chủ quan người chấm nhánh A.
- **Benchmark bão hòa / memorization:** XBOW đã bị huấn luyện vào model → solve-rate nhánh AI trên bản gốc bị thổi phồng. Ta xử lý bằng cặp gốc/hint-free và báo cáo *delta memorization*; nhưng bản hint-free vẫn cùng lớp lỗ hổng nên chỉ giảm chứ không loại hết hiệu ứng.
- **Nhánh B không phủ đều lỗ hổng (quan trọng):** chỉ **21/40 bài** có bộ khai thác no-AI chuyên biệt (sqlmap/dalfox/SSTImap); **19/40 bài** chỉ có nuclei+ffuf → solve-rate nhánh B ở các loại IDOR/logic/deserialization/XXE/LFI... bị giới hạn bởi *công cụ*, không phải bởi "tự động hóa" nói chung. Phải nêu rõ để không phóng đại khoảng cách B vs C.
- **Nhãn loại lỗ hổng (RQ3):** mỗi bài gán 1 `vuln_category` = tag đầu tiên, trong khi nhiều bài có nhiều tag (vd XBEN-006 = idor,sqli). Phân tích theo loại vì thế là gần đúng; (lưu ý: việc *chọn bộ khai thác* nhánh B lại quét **tất cả** tag, nên không bị ảnh hưởng — chỉ phần nhóm RQ3 bị).
- **Vá tương thích Docker:** image EOL → bump phiên bản / mirror archive, CRLF→LF, đổi cổng cố định → ngẫu nhiên (`harness/patches.log`). Không đổi lỗ hổng/flag nhưng là thay đổi môi trường cần khai báo.
- **Giới hạn thời gian 30′/bài** có thể cắt ngắn các bài khó (ảnh hưởng mọi nhánh như nhau).

## 7. Conclusion & Future Work
- Tóm tắt phát hiện, hướng mở rộng (mẫu lớn hơn, web thật có phép, nhiều model).

## References
(IEEE/ACM style — chuẩn bị ~15–25 nguồn)

---

### Nguồn khởi đầu (xác minh lại link trước khi trích)
- XBOW validation-benchmarks: https://github.com/xbow-engineering/validation-benchmarks
- Bản hint-free: https://github.com/KeygraphHQ/xbow-validation-benchmarks
- PentestGPT (USENIX Security 2024 + repo agentic): tìm "PentestGPT GitHub"
- Web of Science CPCI vs SCIE: https://www.aischolar.com/news/article/web-of-science-cpci-conference-authors
