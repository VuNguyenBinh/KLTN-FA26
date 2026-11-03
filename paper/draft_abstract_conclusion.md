# Nháp — Abstract (mục 0) & Conclusion (mục 7)

> Khung để ghép vào `OUTLINE.md`. Viết **cuối cùng**, sau khi có số nhánh người và nhánh AI. Chỗ `[[…]]` là số/khoảng cần điền; số công cụ tự động đã có nên điền sẵn (bắt flag 5%, phát hiện 27,5%). Giữ Abstract ~200 từ.
>
> ⚠️ **Cấu trúc 3 nhánh (2026-11-03) — bản chốt ở `THESIS_FULL.md`:** Truyền thống (người `A_manual` + công cụ `B_auto`) / AI local (`C_ai_local`) / AI API (`C_ai_api`). Trong văn dưới: "nhánh B/tự-động-không-AI" = tầng công cụ của nhánh Truyền thống; "nhánh C" = nhánh AI.

---

## Abstract

Các công cụ kiểm thử xâm nhập (pentest) ứng dụng web dùng mô hình ngôn ngữ lớn (LLM) thường tự báo cáo điểm số cao, nhưng những điểm số này được công bố ở điều kiện không đồng nhất và hiếm khi so sánh có kiểm soát với pentest thủ công hay tự động-không-AI. Nghiên cứu này trình bày một **thí nghiệm có kiểm soát ba nhánh** — thủ công (A), tự động-không-AI (B), và có-AI-hỗ-trợ (C) — trên cùng **40 mục tiêu CTF web** rút phân tầng từ bộ XBOW validation-benchmarks, với cùng tiêu chí chấm (flag khớp chính xác) và cùng giới hạn thời gian. Ta đo tỷ lệ giải, thời gian, công sức con người, chi phí token và tỷ lệ LLM từ chối tác vụ, phân tích theo độ khó và loại lỗ hổng; đồng thời chạy nhánh AI trên cả bản gốc lẫn bản đã-xóa-gợi-ý để định lượng hiệu ứng "học thuộc".

Nhánh tự động-không-AI phát hiện lỗ hổng ở **27,5%** số bài nhưng chỉ bắt được flag ở **5%**, cho thấy khoảng cách giữa *nhận diện* và *khai thác đa bước* (và nhiều lớp còn không được nhận diện). `[[So với baseline đó, pentest có-AI đạt tỷ lệ giải X% so với Y% của thủ công; delta học thuộc là Z điểm; tỷ lệ từ chối của mô hình thương mại là W%.]]` Kết quả `[[chỉ ra AI là trợ lý tăng tốc hay công cụ thay thế]]`, và làm nổi bật các rào cản triển khai thực tế.

**Từ khóa:** penetration testing, large language models, web security, controlled benchmark, memorization.

---

## 7. Conclusion & Future Work

### 7.1 Kết luận
Nghiên cứu đặt ba cách tiếp cận pentest web cạnh nhau trong cùng điều kiện, tách riêng đóng góp của *tự động hóa* khỏi đóng góp của *AI*. Phát hiện đã vững ở nhánh tự động-không-AI: công cụ truyền thống **nhận ra lớp lỗ hổng (27,5%) nhưng gần như không tự khai thác tới flag (5%)**, ngoại lệ là SQLi nhờ bộ khai thác chuyên biệt đóng gói sẵn chuỗi nhiều bước. `[[Khi so với nhánh thủ công và có-AI: nêu kết luận chính — AI thu hẹp khoảng cách nhận-diện→khai-thác ở đâu, còn bế tắc ở lớp phụ-thuộc-ngữ-nghĩa nào.]]`

`[[Về học thuộc: delta gốc–hintfree cho thấy mức điểm nhánh AI phụ thuộc ghi nhớ đến đâu.]]` `[[Về triển khai: bộ lọc an toàn thương mại từ chối W% tác vụ, cho thấy rào cản thực tế ngoài năng lực kỹ thuật.]]` Tổng hợp lại, dữ liệu `[[ủng hộ/bác bỏ]]` quan điểm xem AI như *trợ lý tăng tốc có-người-trong-vòng-lặp* hơn là công cụ thay thế chuyên gia, ít nhất ở các lớp lỗ hổng cần suy luận ngữ cảnh.

### 7.2 Giới hạn
Kết quả gắn với 40 bài CTF-style (không hẳn giống web sản xuất), một bộ mô hình cụ thể, và chủ quan người chấm nhánh A; chi tiết ở *Threats to Validity*. Đặc biệt, chỉ 21/40 bài có bộ khai thác no-AI chuyên biệt, nên khoảng cách B–C ở các lớp còn lại một phần do giới hạn công cụ.

### 7.3 Hướng mở rộng
- Mở rộng mẫu và thêm **mục tiêu web thực (có phép)** để kiểm chứng ngoài môi trường CTF.
- So sánh nhiều họ mô hình (local và API) và các khung agent tự trị mới.
- Benchmark **sinh-mới / hậu-cutoff** để loại hẳn hiệu ứng học thuộc, thay vì chỉ giảm bằng bản hint-free.
- Nghiên cứu sâu `manual_interventions`: con người bù đắp chính xác những bước nào mà AI thiếu.
