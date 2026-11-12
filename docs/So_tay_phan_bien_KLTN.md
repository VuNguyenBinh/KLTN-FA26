---
title: "Sổ tay phản biện KLTN — Mô tả các thành phần đồ án"
---

# Sổ tay phản biện KLTN — Mô tả các thành phần đồ án

**Mục đích:** văn bản tra cứu nhanh khi trả lời câu hỏi hội đồng. Mỗi thành phần được mô tả theo 5 ý cố định: (1) Là gì, (2) Cơ chế hoạt động, (3) Nguồn gốc (tự viết hay dùng lại của người khác), (4) Nhóm chỉnh sửa hoặc thêm gì, (5) Cách dùng tổng quan.

**Đề tài:** A Comparative Study of AI-Assisted and Traditional Web Application Penetration Testing Techniques — Nhóm GFA261A11, môn FA261A11, GVHD Trần Văn Ninh.

**Nguyên tắc trả lời trung thực:** PentestGPT và các mô hình ngôn ngữ KHÔNG phải do nhóm viết. Đóng góp cốt lõi của nhóm là **thiết kế thí nghiệm so sánh có kiểm soát (3 nhánh)**, bộ **harness tự viết** để dựng và chấm bài, **giao thức đo** (grey-box, đếm can thiệp, chấm exact-match), và **toàn bộ dữ liệu + phân tích**.

---

# 0. Bảng tóm tắt "cái gì của nhóm, cái gì dùng lại"

> Đây là câu hỏi hội đồng hay hỏi nhất. Trả lời thẳng bằng bảng này.

| Thành phần | Nguồn gốc | Nhóm đóng góp gì |
|---|---|---|
| **PentestGPT** (driver nhánh AI) | Bên thứ ba — Deng và cộng sự, USENIX Security 2024 | Dùng làm công cụ đo; cấu hình model qua `.env`; viết prompt grey-box; đếm redirect/exec; KHÔNG sửa mã lõi |
| **qwen2.5:7b** (model local) | Bên thứ ba — Alibaba, chạy qua Ollama | Chỉ chạy suy luận (inference), không huấn luyện/sửa |
| **deepseek-v4-pro** (model API) | Bên thứ ba — DeepSeek, gọi qua cổng APIVN | Chỉ gọi API; ghi lại model id + ngày chạy |
| **XBOW validation-benchmarks** (bộ đề) | Bên thứ ba — XBOW Engineering, 2024 | Rút mẫu phân tầng 40 bài; patch chỉ-môi-trường; chuẩn bị biến thể hint-free |
| **nuclei, ffuf, sqlmap, dalfox, SSTImap** | Bên thứ ba — mã nguồn mở | Dàn thành một pipeline cố định (tầng tham chiếu `B_auto`) |
| `build_target.py` | **TỰ VIẾT (nhóm)** | Toàn bộ: dựng, dò cổng, chờ HTTP, ghi URL, patch tương thích, cô lập biến thể |
| `raw.py` | **TỰ VIẾT (nhóm)** | Toàn bộ: gửi HTTP thô cho payload smuggling (curl không gửi trung thực được) |
| `run_arm_B.py`, `run_arm_B_all.py` | **TỰ VIẾT (nhóm)** | Toàn bộ: điều phối pipeline công cụ-tự-chạy, chấm phát hiện/bắt flag |
| `analyze.py` | **TỰ VIẾT (nhóm)** | Toàn bộ: sinh bảng tổng hợp, theo độ khó, theo lớp, detect-vs-capture, memorisation |
| **Thiết kế thí nghiệm 3 nhánh + giao thức đo** | **TỰ THIẾT KẾ (nhóm)** | Đóng góp phương pháp cốt lõi của đồ án |
| **Dữ liệu `results.csv` + nhật ký từng lượt** | **TỰ THU THẬP (nhóm)** | Toàn bộ số liệu và log hành vi |

**Một câu chốt cho hội đồng:** "Chúng em không phát minh công cụ AI; chúng em xây dựng một *phép đo có kiểm soát* để so sánh công bằng ba cách tiếp cận trên cùng một bộ đề, cộng với toàn bộ hạ tầng tự động để chạy và chấm."

---

# 1. PentestGPT — driver của hai nhánh AI

## 1.1 Là gì
PentestGPT là một công cụ mã nguồn mở giúp mô hình ngôn ngữ (LLM) thực hiện kiểm thử xâm nhập theo kiểu "trợ lý": nó biến LLM thành bộ não lập kế hoạch, còn con người là "tay và mắt" chạy lệnh. Công bố tại USENIX Security 2024 (đạt Distinguished Artifact Award).

## 1.2 Cơ chế hoạt động
PentestGPT chia một phiên tấn công thành ba module tự tương tác để tránh "quên ngữ cảnh" khi hội thoại dài:

- **Reasoning:** giữ một cây nhiệm vụ (Pentesting Task Tree) và quyết định bước tiếp theo.
- **Generation:** biến bước đó thành lệnh/thao tác cụ thể.
- **Parsing:** đọc và tóm tắt output thô (vốn rất dài) trước khi đưa lại cho Reasoning.

Vòng lặp một phiên: model đề xuất một bước → người chạy bước đó → dán output thô trở lại → model đọc, cập nhật kế hoạch, đề xuất bước kế.

## 1.3 Nguồn gốc
**Của người khác, không phải nhóm viết.** Nhóm clone nguyên bản (chế độ "legacy") từ kho công khai của tác giả. Nhóm KHÔNG sửa mã nguồn lõi của PentestGPT.

## 1.4 Nhóm chỉnh sửa hoặc thêm gì
Nhóm không đụng vào thuật toán bên trong PentestGPT, nhưng đã làm phần "bọc ngoài" để biến nó thành một *dụng cụ đo*:

- **Cấu hình model qua `.env`:** trỏ `--reasoning-model` / `--parsing-model` sang hai model khác nhau (qwen2.5:7b local và deepseek-v4-pro qua APIVN) để cô lập "hiệu ứng quy mô model".
- **Prompt grey-box tự viết:** chỉ cung cấp *lớp* lỗ hổng + URL, không cho endpoint/payload/kỹ thuật, kèm mệnh đề chặn port-scan (thông tin môi trường).
- **Quy ước đếm can thiệp:** phân biệt "chạy lệnh model đề xuất" (exec, không tính) với "chỉnh hướng khi model đi sai" (redirect, tính là can thiệp). Đây là chỉ số để trả lời "AI là trợ lý hay tự trị".
- **Lằn ranh cứng:** operator không mách kỹ thuật; lỡ mách thì bài tính solved=0.

## 1.5 Cách dùng tổng quan
```
cd project/harness/PentestGPT
.\.venv\Scripts\python.exe -m pentestgpt_legacy.main \
    --reasoning-model "<model>" --parsing-model "<model>"
```
Khi nó hỏi nhiệm vụ → dán prompt grey-box (lớp lỗ hổng + URL) → bấm giờ → chạy từng lệnh nó đề xuất bằng `curl.exe` (hoặc `raw.py` cho smuggling), dán output lại, lặp đến khi bắt flag hoặc hết 30 phút.

---

# 2. Mô hình ngôn ngữ (qwen2.5:7b và deepseek-v4-pro)

## 2.1 Là gì
Hai mô hình đóng vai "bộ não" cho PentestGPT:

- **qwen2.5:7b** — model nhỏ 7 tỷ tham số, chạy cục bộ (nhánh C1).
- **deepseek-v4-pro** — model thương mại mạnh, gọi qua API (nhánh C2).

## 2.2 Cơ chế hoạt động
Là LLM sinh văn bản; PentestGPT gửi prompt (kế hoạch + output đã tóm tắt) và nhận lại bước/lệnh tiếp theo. qwen2.5:7b chạy qua Ollama ở dạng 4-bit; deepseek-v4-pro chạy trên hạ tầng nhà cung cấp, truy cập qua cổng trung gian APIVN.

## 2.3 Nguồn gốc
**Của bên thứ ba.** qwen2.5:7b là của Alibaba; deepseek-v4-pro là của DeepSeek. Nhóm KHÔNG huấn luyện, KHÔNG tinh chỉnh (fine-tune), KHÔNG sửa trọng số.

## 2.4 Nhóm chỉnh sửa hoặc thêm gì
Không sửa model. Nhóm chỉ: chọn cặp model (một nhỏ-local, một lớn-API) để trả lời câu hỏi "AI yếu là do AI hay do model nhỏ"; chạy ở nhiệt độ mặc định của PentestGPT; ghi lại **model id + ngày chạy** (vì model API có thể đổi ngầm theo thời gian — đã nêu trong Threats).

## 2.5 Cách dùng tổng quan
Local: cài qua Ollama (`ollama pull qwen2.5:7b`), PentestGPT trỏ `--base-url http://localhost:11434/v1`. API: điền `DEEPSEEK_API_KEY` + `DEEPSEEK_BASE_URL=https://apivn.vn/v1` vào `.env` (khoá bị `.gitignore` chặn, không lên Git).

---

# 3. XBOW validation-benchmarks — bộ đề

## 3.1 Là gì
Bộ 104 bài CTF web đóng gói Docker, mỗi bài có đúng một lỗ hổng cài sẵn và một flag bí mật. Phủ các lớp XSS, SSTI, SQLi, IDOR, SSRF, deserialization, v.v.

## 3.2 Cơ chế hoạt động
Mỗi bài là một image Docker chạy một web app có lỗ hổng. Flag theo công thức xác định: `FLAG{sha256(UPPER(mã-bài))}`, nên chấm điểm là so khớp chính xác, không cần người phán xử.

## 3.3 Nguồn gốc
**Của bên thứ ba** (XBOW Engineering, công khai cuối 2024). Nhóm KHÔNG tạo ra các bài này.

## 3.4 Nhóm chỉnh sửa hoặc thêm gì
- **Rút mẫu phân tầng 40 bài** (14 dễ / 18 vừa / 8 khó), seed cố định để tái lập.
- **Patch chỉ-môi-trường:** nhiều image từ 2024 đã hết hạn (EOL) → nhóm sửa ảnh gốc hỏng, trỏ lại kho apt, chuẩn hoá line-ending, ngẫu nhiên hoá cổng. Mọi patch được ghi `patches.log` và **KHÔNG đụng lỗ hổng hay flag**.
- **Biến thể hint-free:** dùng bản fork đã gỡ gợi ý (comment/tên gợi ý/README) để đo "học thuộc" — giữ nguyên lỗ hổng và flag.

## 3.5 Cách dùng tổng quan
Qua script tự viết `build_target.py` (xem mục 4) — không dựng tay từng image.

---

# 4. build_target.py — harness dựng bài (TỰ VIẾT)

## 4.1 Là gì
Script Python của nhóm để dựng một bài target và lấy địa chỉ truy cập.

## 4.2 Cơ chế hoạt động
Biên dịch image → khởi động container → dò cổng web → chờ tới khi có phản hồi HTTP thật → ghi URL (và flag ground-truth) vào `targets.csv`. Áp patch tương thích khi cần. Cô lập hai biến thế (gốc / hint-free) bằng project-name riêng (`-p <id>-<variant>`) để chạy song song không đụng nhau.

## 4.3 Nguồn gốc
**Tự viết hoàn toàn.** Đây là hạ tầng của nhóm.

## 4.4 Nhóm chỉnh sửa hoặc thêm gì
Toàn bộ là của nhóm: logic dò cổng/chờ-HTTP, cơ chế patch-và-log, cô lập biến thể.

## 4.5 Cách dùng tổng quan
```
python build_target.py <XBEN-xxx-24>                 # bản gốc
python build_target.py <ID> --variant hintfree --repo "...xbow-hint-free..."
python build_target.py <ID> --down                   # hạ container
```

---

# 5. raw.py — gửi HTTP thô cho request smuggling (TỰ VIẾT)

## 5.1 Là gì
Script gửi một request HTTP *đúng từng byte* qua raw socket.

## 5.2 Cơ chế hoạt động
Mở socket tới cổng target, ghi đúng chuỗi byte trong file request (CRLF thật, `Content-Length` do người soạn), đọc về mọi response trên cùng kết nối.

## 5.3 Nguồn gốc
**Tự viết.** Lý do cần: `curl` tự chuẩn hoá `Content-Length`/`Transfer-Encoding` nên KHÔNG gửi được payload CL.TE / TE.CL trung thực — bắt buộc phải có công cụ raw-socket để kiểm thử lớp smuggling (bài 066).

## 5.4 Nhóm chỉnh sửa hoặc thêm gì
Toàn bộ của nhóm. Lưu ý quan trọng: payload smuggling do **PentestGPT quyết** (đúng từng byte), nhóm chỉ *gửi hộ* qua `raw.py` — không tự chế payload, giữ đúng lằn ranh đo.

## 5.5 Cách dùng tổng quan
```
python raw.py <reqfile> <port> [timeout] [host]
```

---

# 6. Tầng công cụ KHÔNG-AI (nhãn B_auto) — tham chiếu, KHÔNG phải nhánh so sánh

## 6.1 Là gì
Một pipeline cố định gồm các công cụ mã nguồn mở chạy **tự động, không người, không AI** trên cả 40 bài: nuclei (quét template), ffuf (fuzz thư mục), sqlmap (SQLi), dalfox (XSS), SSTImap (SSTI).

## 6.2 Cơ chế hoạt động
Mỗi bài chạy cùng một chuỗi công cụ trong ngân sách 30′. Ghi hai chỉ số: **phát hiện** (công cụ có báo nghi lỗ hổng không) và **bắt flag** (có lấy được flag không). Điều phối bằng `run_arm_B.py` / `run_arm_B_all.py` (tự viết).

## 6.3 Nguồn gốc
Các công cụ là **bên thứ ba** (mã nguồn mở). Cách **dàn chúng thành pipeline cố định** và script điều phối là **của nhóm**.

## 6.4 Vai trò trong thiết kế (điểm hay bị hỏi)
`B_auto` **KHÔNG phải một nhánh so sánh riêng**. Nó là **mốc tham chiếu** nằm bên trong nhánh Truyền thống, để cho thấy công cụ tự-thân làm được tới đâu (phát hiện 27,5% / bắt 5%) — qua đó lý giải *vì sao cần con người*. **Không cộng** điểm của `B_auto` vào điểm nhánh A. Nhánh A chỉ tính khi **con người** bắt được flag (55% = 22/40).

## 6.5 Cách dùng tổng quan
`python run_arm_B_all.py` — chạy toàn bộ 40 bài, ghi kết quả vào `results.csv` với nhãn `B_auto`.

---

# 7. analyze.py — phân tích và sinh bảng/biểu đồ (TỰ VIẾT)

## 7.1 Là gì
Script pandas của nhóm, biến `results.csv` thành bảng và biểu đồ.

## 7.2 Cơ chế hoạt động
Đọc `results.csv`, bỏ các dòng chưa chạy (ô solved trống → không tính là trượt), rồi xuất: Bảng 1 (tổng hợp mỗi nhánh), Bảng 2 (theo độ khó), Bảng 3 (theo lớp lỗ hổng), Bảng 3b (detect-vs-capture cho tầng công cụ), Bảng 4 (memorisation gốc vs hint-free) + các biểu đồ PNG trong `paper/figures/`.

## 7.3 Nguồn gốc
**Tự viết hoàn toàn.**

## 7.4 Nhóm chỉnh sửa hoặc thêm gì
Toàn bộ; gồm cả logic bóc "detected=yes/no" từ cột ghi chú và cách tính Δ memorisation.

## 7.5 Cách dùng tổng quan
```
cd project/analysis
python analyze.py ../results/results.csv
```

---

# 8. Thiết kế thí nghiệm 3 nhánh — đóng góp phương pháp cốt lõi (TỰ THIẾT KẾ)

## 8.1 Là gì
Một so sánh có kiểm soát, within-subject: ba cách tiếp cận chạy trên **cùng** 40 bài, **cùng** luật, để chênh lệch phản ánh *phương pháp* chứ không phải *bài*.

## 8.2 Ba nhánh
- **A — Truyền thống (`A_manual`):** con người + mọi công cụ KHÔNG-AI. Bên trong có tầng tham chiếu `B_auto` (công cụ tự chạy, không cộng điểm).
- **C1 — AI local (`C_ai_local`):** PentestGPT + qwen2.5:7b.
- **C2 — AI API (`C_ai_api`):** PentestGPT + deepseek-v4-pro.

## 8.3 Giao thức đo (điểm cốt lõi)
- Grey-box: chỉ cho *lớp* lỗ hổng + URL cho nhánh AI (ngang thông tin mà pipeline công cụ dùng để chọn exploiter).
- 30 phút/bài (thời gian active, trừ AFK).
- Chấm **exact-match flag** (chỉ số CHÍNH, so chéo 3 nhánh). Chỉ số phụ (thời gian, bước, can thiệp, token, từ chối) chỉ để *giải thích*, không so chéo.
- Mẫu AI là **purposive** (12 và 24 bài, lệch khó) → báo cáo **paired + theo lớp/độ khó**, KHÔNG suy tỉ lệ dân số.

## 8.4 Nguồn gốc
**Của nhóm.** Đây là đóng góp chính của đồ án: không phải một tool mới, mà một *phép so sánh có kiểm soát* tách bạch "hiệu ứng tự động hoá" và "hiệu ứng model".

---

# 9. Cơ chế chấm điểm và ground-truth

## 9.1 Là gì
Quy tắc quyết định một bài có GIẢI hay không.

## 9.2 Cơ chế
Flag = `FLAG{sha256(UPPER(mã-bài))}`, lưu sẵn trong `targets.csv`. Một bài tính `solved=1` khi flag bắt được **khớp chính xác** chuỗi đó **và** không vi phạm lằn ranh (không ai mách kỹ thuật).

## 9.3 Điểm hay bị hỏi: "Flag tính được từ mã-bài, vậy liệt kê flag đúng có chứng minh đã giải không?"
Trả lời thẳng: **không**, chỉ flag đúng là chưa đủ. Vì vậy nhóm lưu **nhật ký từng lượt** (report_C1/C2) ghi lại model đã *thực sự khai thác* ra sao (recon → sink → payload → đọc flag). Bằng chứng giải là **chuỗi khai thác có thật trong log**, không chỉ con số flag.

---

# 10. Dữ liệu results.csv — quy ước cột

Mỗi lần chạy là một dòng. Cột:
`benchmark_id, difficulty, vuln_category, arm, variant, run_id, solved, flag_found, time_minutes, num_steps, tokens_used, manual_interventions, llm_refused, notes`

- `arm`: `A_manual` / `B_auto` / `C_ai_local` / `C_ai_api`.
- `manual_interventions` = số **redirect** (KHÔNG tính số lệnh chạy).
- `num_steps` = số lượt đối thoại/thao tác.
- `notes`: ghi hành vi + cột `detected=yes/no` cho tầng công cụ.

---

# 11. Câu hỏi phản biện hay gặp — trả lời gọn

**Q: Nhóm có tự viết PentestGPT / các model không?**
Không. Đó là công cụ và model của bên thứ ba. Đóng góp của nhóm là *thiết kế so sánh có kiểm soát*, *harness tự viết* (`build_target.py`, `raw.py`, `run_arm_B*.py`, `analyze.py`), *giao thức đo*, và *toàn bộ dữ liệu + phân tích*.

**Q: B có phải một nhánh so sánh không?**
Không. `B_auto` là mốc tham chiếu bên trong nhánh A (công cụ tự chạy không người: phát hiện 27,5% / bắt 5%), dùng để lý giải vì sao cần con người. Không cộng vào điểm nhánh A. Nhánh A = con người + công cụ = 55%.

**Q: So sánh có công bằng không khi nhánh AI chỉ chạy 12/24 bài?**
Có, vì nhóm báo cáo **theo cặp** (chỉ so trên đúng những bài cả hai cùng chạy) và theo lớp/độ khó, KHÔNG so tỉ lệ thô giữa bộ khác cỡ. Trên 12 bài chung: Người 6 / C1 3 / C2 8.

**Q: Nhánh AI có bị rò rỉ đề (operator mách) không?**
Grey-box: chỉ cho lớp lỗ hổng + URL. Operator không mách endpoint/payload/kỹ thuật; lỡ mách thì bài tính solved=0. Người điều phối nhánh AI không phải người đã giải nhánh người cùng bài (chống rò rỉ).

**Q: Benchmark công khai, điểm cao có phải do "học thuộc" không?**
Có nguy cơ. Nhóm chuẩn bị biến thể hint-free để đo Δ học thuộc, nhưng **hiện chưa đủ dữ liệu** (mới vài bài, n=1 nhiễu) nên báo cáo là **giới hạn + future work**, không bịa số.

**Q: Vì sao AI-local yếu (3/12)?**
Vì là model nhỏ 7B: bỏ qua 404/405, không đăng nhập bài auth-gated, lặp lệnh mù. Khi đổi sang model mạnh (cùng 12 bài) tăng 3 → 8 → "AI yếu" phần lớn là do *quy mô model*, không phải do *AI nói chung*.

**Q: AI-API gần ngang người (13 vs 12), vậy AI thay được người chưa?**
Chưa. Hai bên **bổ sung** nhau: mỗi bên thắng ~6 bài bên kia trượt. AI mạnh ở injection/SSTI (chuỗi textbook); người mạnh ở deserialization/XXE/blind-SQLi (đòi tự viết exploit / delivery đa-tầng). Trần của AI là *tự lập trình exploit chính xác*, không phải nhận diện.

**Q: Chi phí chạy AI thế nào?**
Chi phí API tỉ lệ với **số lượt đối thoại**, KHÔNG tỉ lệ số HTTP request (bài blind-SQLi/brute hàng triệu request vẫn rẻ). Tỉ lệ từ chối (refusal) = 0 trên bộ này.

**Q: Số liệu nhánh người có đáng tin không?**
Outcome giải/không-giải được giám sát trực tiếp và chắc. Hạn chế: 37/40 bài chưa xuất log Burp nên thời gian/số bước dựa vào ghi chú giám sát viên (đã nêu trong Threats); 6 bài xem writeup tính solved=0.
