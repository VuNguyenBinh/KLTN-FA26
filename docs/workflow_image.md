# Flowchart — Quy trình chạy thí nghiệm (tổng thể)

> Sơ đồ toàn bộ pipeline thí nghiệm, từ chọn bài → chạy 2 nhánh → chấm → phân tích → so sánh. Mermaid (GitHub tự render). Chi tiết lệnh từng bước: `docs/WORKFLOW.md`. Định nghĩa nhánh + 6 phép so + thuật ngữ: `docs/PLAN.md §Thiết kế so sánh`.
>
> 🖊️ **Bản draw.io sửa được (vẽ bằng drawio-skill):** `docs/workflow.drawio` — mở bằng draw.io desktop hoặc extension VS Code `hediet.vscode-drawio`. Đã qua `validate.py` (0 lỗi, 0 giao cắt/chồng lấp).
>
> **Khung nhánh:** **Truyền thống** = người + *mọi* công cụ không-AI (gồm scanner); **tầng công cụ tự thân** (`B_auto`) là *baseline nội bộ* của Truyền thống (không phải nhánh so sánh riêng); **AI** = C1 local (qwen) / C2 API (DeepSeek + Opus đối chiếu).

```mermaid
flowchart TD
    A["104 bài XBOW (validation-benchmarks)"] --> B["Chọn mẫu phân tầng 40 bài<br/>seed=42 · 14 easy / 18 med / 8 hard"]
    B --> C["build_target.py<br/>áp patch tương thích → ghi targets.csv<br/>URL + ground_truth_flag"]
    C --> D{"Biến thể"}
    D -->|"original (mọi nhánh)"| E["Target chạy · budget 30 phút/bài"]
    D -->|"hint-free (chỉ nhánh AI)"| E

    E --> F["Nhánh TRUYỀN THỐNG"]
    E --> G["Nhánh AI (PentestGPT + model)"]

    subgraph TT["Truyền thống = người + mọi công cụ không-AI"]
        F --> F1["Người giải: Burp + scanner/exploiter<br/>(nuclei/ffuf/sqlmap/dalfox/SSTImap)<br/>theo PTES/WSTG · Policy B"]
        F1 --> F2[("A_manual")]
        F3["Tầng công cụ tự thân<br/>pipeline tự động, KHÔNG người"] -. "baseline" .-> F4[("B_auto")]
    end

    subgraph AIA["AI = PentestGPT + model (người trong vòng lặp)"]
        G --> G1["Prompt grey-box: chỉ cho LỚP lỗ hổng<br/>(không endpoint/tham số/payload)"]
        G1 --> G2["Model đề xuất 1 lệnh"]
        G2 --> G3["Người chạy lệnh → dán kết quả thô<br/>đếm redirect/exec · KHÔNG mớm kỹ thuật"]
        G3 --> G4{"Bắt flag? hoặc hết 30 phút?"}
        G4 -->|"chưa"| G2
        G4 -->|"rồi"| G5[("C1 local qwen / C2 API DeepSeek + Opus ref")]
    end

    F2 --> H["Chấm flag EXACT-MATCH<br/>so với FLAG sha256(bench-id) → solved 0/1"]
    F4 --> H
    G5 --> H
    H --> I["Ghi 1 dòng results.csv<br/>solved · time · steps · tokens · interventions · refused"]
    I --> J["analyze.py"]
    J --> K["Bảng theo nhánh / độ khó / lớp<br/>detect-vs-capture · Δ học thuộc<br/>+ biểu đồ paper/figures"]
    K --> L["So sánh PAIRED trên bài chung<br/>6 phép so · Truyền thống vs AI"]
```

## Chú giải các bước

| Bước | Ý nghĩa |
|---|---|
| **Chọn mẫu 40 bài** | Rút phân tầng từ 104 bài XBOW, seed=42 (tái lập), 14 easy/18 med/8 hard. |
| **build_target.py** | Dựng Docker target, áp bản-vá-tương-thích (không đổi lỗ hổng/flag), ghi URL + flag chuẩn vào `targets.csv`. |
| **Biến thể** | `original` chạy cho mọi nhánh; `hint-free` (xóa gợi ý) chỉ chạy nhánh AI để đo Δ học thuộc. |
| **Nhánh Truyền thống** | Người giải dùng Burp + scanner/exploiter không-AI (PTES/WSTG, Policy B) → `A_manual`. Pipeline tự động không-người chạy riêng = baseline `B_auto`. |
| **Nhánh AI** | PentestGPT + model; vòng lặp *model đề xuất lệnh ↔ người chạy & dán kết quả ↔ đếm redirect/exec*, không mớm kỹ thuật; tới flag hoặc hết 30′ → `C_ai_local`/`C_ai_api`. |
| **Chấm flag** | Exact-match với `FLAG{sha256(UPPER(bench-id))}`, không điểm bộ phận → `solved` 0/1. |
| **results.csv → analyze.py** | Mỗi lượt 1 dòng; sinh bảng (theo nhánh/độ khó/lớp, detect-vs-capture, Δ học thuộc) + biểu đồ. |
| **So sánh paired** | Chỉ so trên **bài chung**, trục = bắt flag; 6 phép so ở `PLAN.md §Thiết kế so sánh`. |
