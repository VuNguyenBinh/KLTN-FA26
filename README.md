# KLTN-FA26 — Comparative Study of AI-assisted and Traditional Web Application Penetration Testing

Đồ án tốt nghiệp: **so sánh có kiểm soát** giữa kiểm thử xâm nhập ứng dụng web theo 3 cách — thủ công, tự động không-AI, và có AI hỗ trợ — trên cùng một bộ benchmark.

## Câu hỏi nghiên cứu
- **RQ1** AI thay đổi *tỷ lệ phát hiện/khai thác* so với thủ công & tự động-không-AI bao nhiêu?
- **RQ2** AI thay đổi *thời gian* và *công sức* (số bước, số lần can thiệp tay) thế nào?
- **RQ3** AI *mạnh/yếu* ở **loại lỗ hổng** nào?
- **RQ4** *Chi phí* so với lợi ích ra sao?

## Thiết kế 3 nhánh
| Nhánh | Mô tả |
|---|---|
| **A — Manual** | Chuyên viên tự tay (Burp, trình duyệt), không LLM |
| **B — Automated no-AI** | Pipeline cố định: nuclei + ffuf + sqlmap + dalfox + SSTImap |
| **C — AI-assisted** | PentestGPT; **C1** = Ollama local, **C2** = API (tùy chọn) |

Benchmark: **XBOW validation-benchmarks** (104 bài CTF web), mẫu 40 bài phân tầng. Nhánh C chạy cả **bản gốc** và **bản hint-free** (đã xóa gợi ý) để **đo hiệu ứng "AI học thuộc"** — benchmark đã bão hòa nên đây là đóng góp chính.

## Cấu trúc repo (chỉ gồm phần việc của nhóm)
```
docs/          PLAN, SETUP, WORKFLOW, ARM_B, RUNBOOK, STATUS  (hướng dẫn)
paper/         OUTLINE.md  (dàn bài báo)
project/
  harness/     build_target.py, build_all.py  (dựng target + vá tương thích)
               run_arm_B.py                    (pipeline nhánh B)
  analysis/    analyze.py                      (bảng + biểu đồ)
  benchmarks/  metadata.csv, sample.csv        (104 bài + mẫu 40 bài)
  results/     results_template.csv            (mẫu ghi số liệu)
```
> Các thư mục nặng (benchmark clones, PentestGPT, binary công cụ nhánh B) **không** được commit — tải lại theo `docs/SETUP.md` và `docs/ARM_B.md`.

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
