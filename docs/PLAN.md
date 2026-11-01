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

## 2. Thiết kế thí nghiệm

**Biến độc lập:** phương pháp kiểm thử (3 nhánh).
**Biến phụ thuộc:** tỷ lệ giải, thời gian/bài, số bước, chi phí, loại lỗ hổng.
**Kiểm soát:** cùng bộ target, cùng giới hạn thời gian/bài, cùng tiêu chí "giải được" = tìm đúng flag.

### Ba nhánh
| Nhánh | Mô tả | Người phụ trách |
|---|---|---|
| **A — Manual** | Thành viên tự tay kiểm thử (Burp/trình duyệt/sqlmap thủ công), không dùng LLM | Người 1 |
| **B — Automated (no AI)** | Pipeline/scanner cố định, không LLM | Người 2 |
| **C — AI-assisted** | Trợ lý pentest dùng LLM. **C1 = LLM local (Ollama)**, **C2 = LLM API thương mại** | Người 3 (+ Người 2 hỗ trợ) |

### Bộ target (benchmark)
- **XBOW validation-benchmarks**: 104 bài CTF web, mỗi bài 1 Docker Compose, 1 flag, chấm exact-match.
- Chọn **mẫu phân tầng 40 bài** theo độ khó (dễ/trung/khó) để chạy kịp. Danh sách chốt lưu ở `project/benchmarks/sample.csv`.
- Giới hạn mỗi bài: **30 phút** (manual & AI), scanner tự dừng theo cấu hình.

---

## 3. Lịch chi tiết

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

## 4. Rủi ro & phương án dự phòng
| Rủi ro | Dự phòng |
|---|---|
| API thương mại từ chối tác vụ pentest (bộ lọc an toàn) | Dựa chính vào **C1 local Ollama**; C2 chỉ chạy các bài không bị chặn, báo cáo trung thực tỷ lệ bị từ chối (bản thân nó là một **kết quả nghiên cứu**). |
| Bài build lỗi trên Docker mới | Dùng bản vá tương thích tối thiểu, ghi rõ bài nào bị loại. |
| Không kịp 40 bài | Giảm còn 20–25 bài vẫn đủ ý nghĩa thống kê mô tả. |
| Máy yếu khi chạy LLM local | Dùng model 7–8B lượng tử hóa (q4); chạy tuần tự, không song song. |

---

## 5. Tiêu chí "xong" cho mỗi bài
- Flag tìm được? (Y/N) + chuỗi flag.
- Thời gian (phút), số bước/lượt tương tác.
- (Nhánh C) số token / số lần người can thiệp tay / có bị LLM từ chối không.
- Loại lỗ hổng của bài (lấy từ metadata benchmark).
- Ghi chú định tính (AI gợi ý đúng/sai chỗ nào).
