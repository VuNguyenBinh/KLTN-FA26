# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 5. Bối cảnh sống (Living Context)

> Khối này được nạp mỗi phiên và được giữ lại khi nén hội thoại (xem PreCompact hook trong `.claude/settings.json`). **Cập nhật khi mục tiêu / quyết định / số liệu đổi.** Mục đích: chống lệch hướng và mất ngữ cảnh ở hội thoại dài.

**Đề tài:** So sánh có kiểm soát kiểm thử web **thủ công (người + công cụ không-AI)** vs **AI hỗ trợ** (PentestGPT + model nhỏ local / model mạnh API), trên cùng benchmark XBOW (mẫu 40 bài).

**Ba nhánh:** A_manual (người, 40 bài) · C1 = PentestGPT+qwen2.5:7b (12 bài) · C2 = PentestGPT+deepseek-v4-pro API (24 bài). B_auto = tầng công cụ tham chiếu *bên trong* nhánh A, **không** phải nhánh so sánh.

**Luật chung:** grey-box (chỉ cho lớp lỗ hổng + URL), 30′/bài, chấm exact-match flag. So sánh công bằng = **theo cặp trên bài chung**, không so tỉ lệ thô giữa bộ khác cỡ.

**Số liệu chốt (đã thực nghiệm, không bịa):**
- Nhánh A: 22/40 = 55%.
- 12 bài chung (3 nhánh): C2 **8** · Người **6** · C1 **3**. Ba bài C1 giải nằm trọn trong 8 bài C2.
- 24 bài chung C2∩A: C2 **13/24** vs Người **12/24**; McNemar **p=1,0** (không khác biệt thống kê); thời gian ~26 vs ~24 phút; bước ~13,5 vs ~12,7.
- Redirect C1→C2 giảm 2,0 → 0,6 (model mạnh tự lái, ít cần điều hướng).

**File chuẩn (canonical):**
- Slide VN: `Slide/KTLN_slide.pptx` (27 slide) · Slide EN: `Slide/KTLN_slide_EN.pptx` — khuôn mẫu slide do người dùng chỉnh tay, giữ nguyên bố cục, đừng làm mất chỉnh sửa của họ.
- Bài báo: `paper/paper_ieee.tex` (+ `.docx`, `FA261A11_GFA261A11_paper.pdf`). Chỉ có bản IEEE (bản SCI đã xoá).
- Sổ tay phản biện: `docs/So_tay_phan_bien_KLTN.md` / `.docx`.
- Dữ liệu: `project/results/results.csv` · phân tích: `project/analysis/analyze.py` (de-dup 032 rerun) · điều phối: `docs/STATUS.md`.

**Quy ước làm việc đã chốt:** người dùng tự sửa slide trong PowerPoint rồi mới commit; khi sửa pptx bằng python-pptx phải gán shape-ID duy nhất (tránh PowerPoint "repair" xoá nội dung); dùng hình sẵn có thay vì vẽ chart mới; văn phong liền mạch, không ký tự mũi tên, mỗi ý có câu chốt rõ.
