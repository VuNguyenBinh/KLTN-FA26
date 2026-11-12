# KLTN-FA26 — Comparative Study of AI-assisted and Traditional Web Application Penetration Testing

Đồ án tốt nghiệp: **so sánh có kiểm soát** giữa kiểm thử xâm nhập ứng dụng web **thủ công (con người + công cụ)** và **có AI hỗ trợ** (model nhỏ chạy local + model mạnh qua API), trên cùng một bộ benchmark. Pipeline công cụ tự-chạy không-AI được giữ làm **mốc tham chiếu**, không phải một nhánh so sánh.

## 🎥 Demo video
Một phiên chạy nhánh AI (**C2 — PentestGPT + DeepSeek V4 Pro**) tự khai thác lỗ hổng **SSTI** tới khi bắt được flag: **https://youtu.be/sYW8kPi0vfQ**

## Câu hỏi nghiên cứu
- **RQ1** Cùng điều kiện, AI-assisted so với thủ công & công cụ tự động khác nhau thế nào về *bắt flag, thời gian, công sức*?
- **RQ2** Khác biệt đó thay đổi ra sao theo **độ khó** của bài?
- **RQ3** Khác biệt theo **lớp lỗ hổng** (lớp cần suy luận đa bước vs lớp đã có công cụ chuyên trị)?
- **RQ4** Rào triển khai: **học thuộc (memorisation)**, tỉ lệ **từ chối**, và **chi phí** vận hành?

## Thiết kế 3 nhánh so sánh
Ba cách tiếp cận chạy trên **cùng 40 bài**, cùng luật (grey-box chỉ cho *lớp* lỗ hổng, 30′/bài, chấm flag **exact-match**):

| Nhánh | Nhãn dữ liệu | Mô tả |
|---|---|---|
| **A — Truyền thống** | `A_manual` | Con người + mọi công cụ KHÔNG-AI (Burp, nuclei, ffuf, sqlmap, dalfox, SSTImap) |
| **C1 — AI local** | `C_ai_local` | PentestGPT + Ollama `qwen2.5:7b` (model nhỏ 7B, chạy tại máy) |
| **C2 — AI API** | `C_ai_api` | PentestGPT + `deepseek-v4-pro` (model mạnh, qua APIVN) |

> **Tầng công cụ tự-chạy (`B_auto`)** = pipeline KHÔNG-người-KHÔNG-AI (nuclei + ffuf + sqlmap + dalfox + SSTImap), chỉ là **mốc tham chiếu** bên trong nhánh A để thấy công cụ tự thân làm được tới đâu — **KHÔNG phải một nhánh so sánh riêng**, không cộng vào điểm nhánh A.

Benchmark: **XBOW validation-benchmarks** (104 bài CTF web), mẫu 40 bài phân tầng. Nhánh AI chạy cả **bản gốc** và **bản hint-free** (đã xóa gợi ý) để đo **"AI học thuộc"** (memorisation).

## Kết quả chính
- Công cụ tự-chạy (`B_auto`): **phát hiện 27,5% / bắt flag 5%** → khoảng cách phát hiện→khai thác mà *con người* lấp.
- Nhánh A (người + công cụ): **55% (22/40)**.
- So **theo cặp trên 12 bài chung**: Người **6** / AI-local **3** / AI-API **8** → "AI yếu" phần lớn là do *model nhỏ*, không phải do *AI*.
- Trên 24 bài (lệch khó): AI-API **13** ≈ Người **12**, nhưng **bổ sung nhau** (mỗi bên thắng ~6 bài bên kia trượt).
- Chi tiết: bài báo `paper/paper_ieee.tex`, tổng hợp `docs/STATUS.md` + `docs/results_summary.md`.

## Cấu trúc repo (chỉ gồm phần việc của nhóm)
```
docs/          STATUS (điều phối + kết quả), results_summary, task_C1/C2,
               report_A/C1/C2 (nhật ký từng lượt), C2_ai_findings_24,
               So_tay_phan_bien_KLTN (sổ tay phản biện), SETUP, RUNBOOK
paper/         paper_ieee.tex/.docx (bản IEEE 2 cột), paper_sci2027.tex/.docx,
               THESIS_FULL.md, figures/
project/
  harness/     build_target.py (dựng target + vá tương thích), raw.py (HTTP thô
               cho smuggling), run_arm_B*.py (pipeline công cụ tham chiếu)
  analysis/    analyze.py                      (bảng + biểu đồ)
  benchmarks/  metadata.csv, sample.csv        (104 bài + mẫu 40 bài)
  results/     results.csv                     (dữ liệu thí nghiệm)
```
> Các thư mục nặng (benchmark clones, PentestGPT, binary bộ công cụ tham chiếu `B_auto`) **không** được commit — tải lại theo `docs/SETUP.md` và `docs/ARM_B.md`.

## Tái lập môi trường
Xem **[docs/SETUP.md](docs/SETUP.md)** (cài Docker/Git/Ollama, clone benchmark) và **[docs/RUNBOOK.md](docs/RUNBOOK.md)** (chạy từng bước). Tóm tắt:
```powershell
# 1) clone 2 bo benchmark vao project/benchmarks/
git clone https://github.com/xbow-engineering/validation-benchmarks.git project/benchmarks/validation-benchmarks
git clone https://github.com/KeygraphHQ/xbow-validation-benchmarks.git project/benchmarks/xbow-hint-free
# 2) dung target (tu va tuong thich Docker 2026, inject flag chuan)
cd project/harness; python build_target.py XBEN-001-24
# 3) chay 3 nhanh theo docs/RUNBOOK.md -> nhap results.csv -> python analysis/analyze.py
```

## Ghi chú học thuật
- Mọi bản vá tương thích Docker (image EOL, CRLF, port) được log ở `harness/patches.log` — **không đổi lỗ hổng/flag**, khai báo trong *Threats to Validity*.
- "SCI 2027": bài hội nghị index ở **CPCI (Web of Science)** hoặc **Scopus**, không phải SCIE/SCI — kiểm tra proceedings hội nghị đã thực sự index ở kỳ trước.
