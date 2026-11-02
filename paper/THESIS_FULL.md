<!--
==============================================================================
 HƯỚNG DẪN SỬ DỤNG FILE NÀY  (đọc trước — xoá cả khối comment này khi nộp)
==============================================================================
Đây là bản LẮP GHÉP các draft (paper/draft_*.md) vào đúng khung luận văn FPT
(6 chương, theo IAP491_CP_StudentsGuideForm). Ngôn ngữ: tiếng Anh (quy định trường).

CÁCH DÙNG:
1. Mỗi khối "> ⚙️ HƯỚNG DẪN:" là chỉ dẫn cho nhóm — XOÁ hết trước khi nộp.
2. Mỗi "[[... ]]" là chỗ CHỜ SỐ LIỆU (nhánh A thủ công + nhánh C mở rộng).
   Chạy `python analyze.py ../results/results.csv` để lấy số rồi điền vào.
3. 6 Report của FPT ánh xạ 1-1 với 6 chương:
   Report 1 = Ch.1 Introduction | Report 2 = Ch.2 Literature Review
   Report 3 = Ch.3 Methodology  | Report 4 = Ch.4 Experimental & Results
   Report 5 = Ch.5 Discussion   | Report 6 = Ch.6 Conclusion & Future Work
4. CHỐNG ĐẠO VĂN / AI-DETECT (quan trọng, đọc kỹ):
   - Nội dung dưới đây là bản NỀN. Mỗi người PHẢI đọc lại cả chương mình phụ
     trách và VIẾT LẠI theo giọng mình: đổi cách mở câu, thêm 1-2 quan sát
     riêng khi chạy thí nghiệm (vd "khi chạy XBEN-xxx chúng tôi thấy..."),
     gộp/tách câu. Chính các chi tiết thật của nhóm là thứ máy không bịa được.
   - Mọi câu trích dẫn người khác đã được diễn đạt lại + đánh số [n]; KHÔNG
     copy nguyên văn nguồn. Khi thêm ý mới nhớ trích nguồn.
   - Chạy qua Turnitin/AI-checker của trường TRƯỚC hạn, sửa chỗ bị gắn cờ.
5. Chuyển sang Word: dán từng chương, dùng Heading styles để tạo mục lục tự động
   (template FPT yêu cầu TOC/List of Figures/Tables tự động).
6. Dữ liệu thật: project/results/results.csv ; log nhánh C: docs/report_C.md ;
   mã phân tích: project/analysis/analyze.py ; repo: github.com/VuNguyenBinh/KLTN-FA26
==============================================================================
-->

MINISTRY OF EDUCATION AND TRAINING — FPT UNIVERSITY

# Capstone Project Document

## A Comparative Study of AI-Assisted and Traditional Web Application Penetration Testing Techniques

> ⚙️ HƯỚNG DẪN (Title page): điền bảng dưới theo mẫu FPT, thêm logo trường khi sang Word.

| | |
|---|---|
| **Group Members** | [Họ tên 1 — MSSV], [Họ tên 2 — MSSV], [Họ tên 3 — MSSV], … |
| **Supervisor** | [Tên GVHD] |
| **Capstone Project code** | [mã CP] |

*— Hanoi, [Month]/2026 —*

---

# ABSTRACT

> ⚙️ HƯỚNG DẪN: Abstract phải tự đứng một mình: KHÔNG viết tắt chưa định nghĩa, KHÔNG URL, KHÔNG trích dẫn. Giữ 200–300 từ. Điền `[[…]]` khi có số nhánh A/C. Giữ 4 ý ẩn (Background/Methods/Results/Conclusions) nhưng KHÔNG in tiêu đề.

Automated security tools that use large language models now report high success rates on penetration-testing benchmarks, yet those numbers are rarely obtained under the same conditions as a human tester or a classic scanner, which makes them hard to trust. This study tackles that gap with a controlled, three-arm comparison on a single target set. We run forty web capture-the-flag challenges, drawn by stratified sampling from the XBOW validation benchmarks, through three approaches under identical rules: a manual tester (arm A), a fixed non-AI automation pipeline (arm B), and an AI-assisted tester that pairs a human operator with a locally hosted language model (arm C). Every run is scored by exact-match flag capture and logged for time, number of steps, human interventions, and tool-refusal events; the AI arm is additionally run against a hint-removed copy of each target so that we can estimate how much of its performance is memorisation rather than reasoning. Our completed non-AI baseline detects a vulnerability in 22 of 40 targets (55%) but captures the flag in only 2 (5%), a gap that exposes where automation stalls: recognising a vulnerability class is far easier than chaining a multi-step exploit to the flag. [[Điền kết quả so sánh arm A và arm C: solve-rate, Δ memorisation, refusal rate.]] The findings suggest that, with a small local model, AI functions as an accelerating assistant rather than a replacement for the human tester, and they make the practical cost of that assistance visible.

**Keywords:** penetration testing; large language models; web application security; controlled benchmark; vulnerability detection; memorisation; PentestGPT

---

# ACKNOWLEDGEMENT

> ⚙️ HƯỚNG DẪN: phần tuỳ chọn. Cảm ơn GVHD, trường, người hỗ trợ. Viết ngắn, thật, theo giọng nhóm.

[Nhóm viết lời cảm ơn ở đây.]

---

# TABLE OF CONTENTS

> ⚙️ HƯỚNG DẪN: trong Word dùng References → Table of Contents (tự động) sau khi gán Heading styles. Danh sách dưới chỉ để tham chiếu.

- Chapter 1. Introduction
- Chapter 2. Literature Review
- Chapter 3. Methodology
- Chapter 4. Experimental and Results
- Chapter 5. Discussion
- Chapter 6. Conclusion and Future Work
- References
- Appendices

# LIST OF FIGURES

> ⚙️ HƯỚNG DẪN: chèn hình thật từ `paper/figures/` (do analyze.py sinh) rồi tạo caption. Tối thiểu nên có:
- Figure 1. Overall solve rate by method (`fig_solve_rate.png`).
- Figure 2. Solve rate by difficulty (`fig_by_difficulty.png`).
- Figure 3. Arm B — detection vs capture by difficulty (`fig_detect_vs_capture.png`).
- Figure 4. Memorisation effect: original vs hint-free for the AI arm (`fig_memorization.png`, sau khi có số nhánh C).

# LIST OF TABLES

> ⚙️ HƯỚNG DẪN: các bảng do analyze.py xuất ra (`paper/figures/table_*.csv`):
- Table 1. Summary of metrics per arm.
- Table 2. Solve rate by difficulty.
- Table 3. Detection vs capture by vulnerability class (arm B).
- Table 4. Memorisation table for the AI arm (original vs hint-free).

# ABBREVIATIONS

| Acronym | Meaning |
|---|---|
| AI | Artificial Intelligence |
| CTF | Capture The Flag |
| CVE | Common Vulnerabilities and Exposures |
| IDOR | Insecure Direct Object Reference |
| LFI | Local File Inclusion |
| LLM | Large Language Model |
| RQ | Research Question |
| SQLi | SQL Injection |
| SSTI | Server-Side Template Injection |
| XSS | Cross-Site Scripting |

---

# CHAPTER 1. INTRODUCTION

## 1.1. Background

Web applications remain one of the most exposed parts of any organisation's attack surface, and penetration testing is the standard way of probing them before an attacker does. The work is slow, it leans heavily on scarce expert judgement, and it does not scale comfortably with the pace at which modern services ship. Against that backdrop, the recent wave of large language models has produced a crowd of "AI pentest" tools that claim to automate much of the job, often advertising very high scores on public benchmarks.

The trouble is that those scores are difficult to compare. They come from different models, different levels of access to the target, and — crucially — different assumptions about whether the benchmark was already seen during training. A single, widely cited result makes the fragility concrete: a GPT-4 agent exploited 87% of a set of one-day vulnerabilities when it was handed the vulnerability description, and only 7% when the description was withheld [4]. A number can swing by an order of magnitude depending on how the experiment is framed.

## 1.2. Problem Statement

What the field is missing is not another tool but a **controlled comparison**. Published results seldom place an AI-assisted tester, a non-AI automated scanner, and a human working by hand next to each other on the *same* targets, under the *same* time budget, with the *same* scoring rule. Without that, two questions stay open: how much of the measured gain comes from automation as such, and how much from the language model on top of it? This thesis is built to separate those two effects.

## 1.3. Research Objectives

We state the study as four research questions.

- **RQ1.** On identical targets and under identical rules, how does AI-assisted testing compare with non-AI automation and with manual testing, in terms of flag-capture rate, time, and human effort?
- **RQ2.** How does that comparison change with target **difficulty**?
- **RQ3.** How does it change with **vulnerability class** — in particular, classes that need multi-step reasoning versus classes a dedicated tool already handles?
- **RQ4.** How large is the **memorisation** effect (original versus hint-removed targets) for the AI arm, and how significant are the practical deployment barriers, namely tool refusals and cost?

## 1.4. Significance of the Study

The contribution is fourfold. First, a controlled three-arm design (manual / automated-no-AI / AI-assisted) run on one shared benchmark, so that the automation effect and the AI effect can be read apart rather than guessed at. Second, a multi-dimensional measurement set — capture rate, time, steps, cost, human interventions, refusal rate — broken down by difficulty and by vulnerability class. Third, a direct estimate of **memorisation**: by running the AI arm on both the original and a hint-removed copy of each challenge and reporting the delta, we address the saturation problem head-on instead of ignoring it. Fourth, an honest account of the practical frictions a team actually hits — safety filters that refuse the task, and the token cost of running the models.

## 1.5. Scope and Limitations

The study is deliberately narrow so that it can be controlled. Targets are forty CTF-style web applications, not production systems; the AI arm is anchored on one local model family; and the manual arm carries the subjectivity of a human grader. We return to these threats in Section 3.4 and Chapter 5. What the study does **not** claim is a general verdict on "AI versus humans" in security — only a measured comparison within this setting.

## 1.6. Thesis Structure

Chapter 2 reviews traditional scanners, LLM-based pentest systems, and the benchmark-saturation problem, and locates our contribution among them. Chapter 3 describes the three arms, the target set, the protocol, and the metrics. Chapter 4 presents the data, starting with the completed non-AI baseline. Chapter 5 interprets the results against the research questions and the prior literature. Chapter 6 concludes and points to future work.

---

# CHAPTER 2. LITERATURE REVIEW

> ⚙️ HƯỚNG DẪN: Report 2 có trọng số CAO (25%). Hội đồng sẽ soi "khoảng trống" và cách trích nguồn. Các nguồn [1]–[10] đã được xác minh (xem danh sách References + paper/draft_intro_relatedwork.md). Khi thêm nguồn mới, đánh số tiếp và trích trong văn.

## 2.1. Review of Previous Studies

### Traditional non-AI automation

The backbone of non-AI automation is a family of scanners and class-specific exploiters: template scanners such as nuclei, directory fuzzers such as ffuf, and dedicated tools such as sqlmap for SQL injection, dalfox for cross-site scripting, and SSTImap for template injection. Their strength is quick, repeatable recognition of vulnerability classes that carry a clear signature. Their well-documented weakness lies with business-logic flaws — insecure direct object references, broken access control — and with exploits that take several chained steps, where no static signature captures enough of the context. We use exactly this toolchain as arm B, so that the study's baseline reflects a credible non-AI starting point rather than a strawman.

### Pentest systems built on LLMs

PentestGPT [1] is the reference point. It decomposes an engagement into three self-interacting modules (reasoning, generation, parsing) to keep context from collapsing, and it reports a 58.6% improvement in sub-task completion over direct use of GPT-4, on a benchmark covering the OWASP Top 10; the work received a Distinguished Artifact Award at USENIX Security 2024. We adopt PentestGPT in its assistant ("legacy") mode as arm C, specifically so that the number of human interventions can be counted — a figure that speaks directly to whether AI *replaces* or merely *accelerates* the tester.

A string of later systems extends this line but converges on one message: agents are strong on known CVEs and weak on open-ended, end-to-end tasks. AutoPenBench [5] reports a fully autonomous agent at 21% success across 33 tasks, rising to 64% once a human assists — a gap that is itself an argument for a human-in-the-loop design. HackSynth [6] contributes an autonomous agent and two CTF benchmarks of roughly 200 challenges. CVE-Bench [7] gathers 40 real web-application CVEs and finds the best agent solving at most 12.5% in the one-day setting. PentestEval [10] decomposes an engagement into 346 stage-level tasks and finds end-to-end success for fully autonomous agents still below 6%, i.e. competence at individual steps does not compose into a finished exploit chain. A 2026 systematic survey of 81 papers [8] frames these as structural open problems of the field: unreliable evaluation, weak multi-stage performance, and scarce training data.

### Benchmarks and the saturation problem

The XBOW validation benchmarks [2] are 104 Docker-packaged web CTF challenges, released publicly in late 2024, spanning XSS, SSTI, SQLi, IDOR, SSRF and more; XBOW reports roughly an 85% solve rate for its own system. We chose this set for its determinism (exact-match flags), its container isolation, and its class coverage. That same popularity creates a hazard: once a benchmark is public, a model's score on it may reflect recall rather than discovery. The survey [8] names this as a central reliability concern and notes that binary success metrics cannot separate genuine capability from benchmark alignment. The clearest quantitative evidence comes from CTFusion [9], which compares the same agent on a static benchmark and on live competition and identifies 71 "memorisation events"; removing them drops the mean success rate by 29 percentage points. Worth noting, too, is AWE [8] (a 2026 multi-agent web system), which runs *on the XBOW set we use* and reports 87% success on XSS and 66.7% on blind SQLi — high numbers on our exact benchmark, which both give the AI arm a reference point and sharpen the question of how much of such a figure is memorisation.

## 2.2. Summary of the Literature Review

Two themes run through the prior work. Reported capability keeps climbing, but it is measured in ways that are hard to compare across studies and that may be inflated by contamination; and even the better agents stumble on the multi-step, discovery-heavy tasks that real engagements are made of. The human-assisted variant of AutoPenBench outscoring its autonomous counterpart by a wide margin is the single most telling data point for our design choice.

## 2.3. Contribution of Research

Set against that body of work, our distinguishing move is the **controlled comparison** itself. Rather than evaluating one AI system on one benchmark, we place three approaches side by side on the same targets under the same protocol, which lets us separate the automation effect from the AI effect, and we quantify memorisation and deployment friction directly — aspects that single-score papers tend to pass over. In the spirit of CTFusion's memorisation check [9], but applied to a controlled three-arm comparison rather than a single agent.

---

# CHAPTER 3. METHODOLOGY

> ⚙️ HƯỚNG DẪN: Report 3 (20%). Phần này mô tả thiết kế — viết ở thì hiện tại, đã khớp đúng những gì nhóm chạy. Nhánh A/C mô tả ở mức giao thức; khi chạy xong chỉ bổ sung số vào Ch.4, KHÔNG sửa Ch.3.

## 3.1. Research Design

This is a controlled, within-subject comparison: all three approaches run on the exact same forty targets, so that any difference reflects the method rather than the target. The three arms are summarised below.

| Arm | Name | Human | Automation | LLM | Main tools |
|---|---|---|---|---|---|
| **A** | Manual | Yes (tester) | No | No | Burp Suite Community + manual work |
| **B** | Automated, no-AI | No (after launch) | Yes | No | nuclei, ffuf, sqlmap, dalfox, SSTImap |
| **C1** | AI — local model | Yes (in the loop) | Partial | Yes (local) | PentestGPT (legacy) + Ollama `qwen2.5:7b` |
| **C2** | AI — API model | Yes (in the loop) | Partial | Yes (commercial) | PentestGPT (legacy) + hosted API |

Arm A stands for traditional manual testing. Arm B is a fixed, identical-for-every-target pipeline, so that differences between targets reflect tool capability and not per-target tuning by a human. Arm C is AI-assisted testing in PentestGPT's assistant mode, split into a local model (C1) and a commercial API model (C2). For this document C1-local is the primary AI arm; C2 is an optional extension whose refusal rate is itself a reported result (Section 3.6).

## 3.2. Data Collection Methods

### Target set and ground truth

Targets come from the XBOW validation benchmarks — 104 Docker-packaged web CTF challenges, each with one planted vulnerability and a secret flag. Each flag follows a deterministic formula, `FLAG{sha256(UPPER(benchmark-id))}`, which we verified against the benchmark's own build pipeline. A target counts as **solved** only when the captured flag matches that string exactly; there is no partial credit.

To deal with saturation we prepare two variants of every challenge: the **original**, and a **hint-removed** fork (from the KeygraphHQ copy [3]) that strips solution hints — comments, suggestive names, README text — while leaving the vulnerability and flag intact. Arm C runs on both variants; arms A and B run on the original only, since a scanner and a human tester do not "read" source hints the way a trained model might have memorised them.

### Protocol

Every arm is capped at **30 minutes per target**. Arm B enforces this as a cumulative budget across its tool steps. Arm C follows the assistant loop: the model proposes a step, the human runs it and pastes the result back, and each such human action is counted as one intervention. Arm A is a human working through Burp and recording time and steps by hand.

### Infrastructure and reproducibility

All targets are built by an automated harness (`build_target.py`) that compiles the image, starts it, finds the web port, waits for a real HTTP response, and records the URL. Two technical points matter for reproducibility and must be declared. First, because the benchmarks date from 2024, several base images are end-of-life; the harness applies a set of *compatibility-only* patches (bumping a broken image, repointing apt to the Debian archive, normalising line endings, randomising fixed ports) and logs every one to `patches.log`. These patches never touch the vulnerability or the flag. Second, because the two variants share a directory name, Docker Compose would otherwise collide them; the harness isolates each with an explicit project name, `-p <id>-<variant>`, so both variants run side by side with distinct images. Hardware: Docker engine 29.8.1; the local model runs under Ollama as `qwen2.5:7b` (4-bit) on an NVIDIA RTX A1000.

## 3.3. Sampling and Data Analysis Techniques

From the 104 challenges we draw a **stratified sample of forty** by difficulty, with a fixed seed (42) for reproducibility: 14 easy, 18 medium, and 8 hard (all eight hard challenges are taken, since there are only eight). Each target is tagged with one or more vulnerability classes from the benchmark metadata.

Each run writes one row to `results.csv` with these fields: solved, time, number of steps, tokens used, manual interventions, LLM-refused, and a free-text note. For arm B we additionally record a **detection** flag — whether the tools signalled a vulnerability at all, even when they could not reach the flag — because that distinction turns out to be central (Chapter 4). Analysis is automated with pandas in `analyze.py`, which produces a per-arm summary, breakdowns by difficulty and by vulnerability class, an arm-B detection-versus-capture table, and the memorisation table for arm C. Rows that have not been run (blank `solved`) are dropped, not counted as failures. For the AI arm we compute the memorisation delta as `solve_rate(original) − solve_rate(hint-removed)`: a large delta signals reliance on having *seen* the solution rather than *finding* it.

## 3.4. Limitations of the Methodology

The sample is forty CTF-style challenges, which are not identical to production web applications; the AI arm rests on one model family; and arm A carries grader subjectivity. The detection metric for arm B is a string-matching heuristic over tool output, so it can both over- and under-count and should be read as an *optimistic upper bound* on automated recognition, applicable to arm B only. Only 21 of the 40 targets have a dedicated non-AI exploiter (the rest rely on nuclei+ffuf), so part of arm B's low capture rate on IDOR/logic/deserialisation classes is a *tool* limitation rather than a property of "automation" in general. The 30-minute cap may cut short the hardest targets, though it does so equally for every arm. Finally, the compatibility patches are an environmental change that we declare rather than hide.

---

# CHAPTER 4. EXPERIMENTAL AND RESULTS

> ⚙️ HƯỚNG DẪN: Report 4 (25%, trọng số CAO). Hiện CHỈ nhánh B đủ 40/40. Nhánh C mới 1 phiên mẫu (XBEN-061). Nhánh A chưa chạy. Phần dưới trình bày TRUNG THỰC đúng hiện trạng; điền `[[…]]` khi có thêm dữ liệu. TUYỆT ĐỐI không bịa số nhánh A/C.

## 4.1. Introduction

This chapter reports the data collected so far. The non-AI baseline (arm B) is complete across all forty original targets; the AI arm (C) is reported as a validated pilot run, with the full campaign still in progress; the manual arm (A) is pending. We present the completed baseline first and in full, then the pilot evidence from the AI arm, and we are explicit about what is measured versus what remains to be collected.

## 4.2. Presentation of Data

### Arm B — non-AI automation (complete, 40/40)

We report two numbers that must be kept apart: **capture** (the flag was obtained) and **detection** (the tools flagged a vulnerability, even if no flag followed).

**Table 1 (arm B).** Over 40 targets, arm B **captures the flag in 2/40 (5.0%)** while **detecting a vulnerability in 22/40 (55.0%)**. Mean time was 3.1 minutes per target.

| Metric | Result |
|---|---|
| Flag capture (`solved`) | **2/40 = 5.0%** — XBEN-071, XBEN-083 (both SQLi, via sqlmap database dump) |
| Vulnerability detection | **22/40 = 55.0%** |

**By difficulty (capture / detection):** easy 2/14 = 14.3% / 9/14 = 64.3%; medium 0% / 10/18 = 55.6%; hard 0% / 3/8 = 37.5%.

**By vulnerability class (selected, detection-sorted):** SQLi 2/2 captured (100%); SSTI 6/6 detected but 0 captured; XSS 8/10 detected, 0 captured; IDOR 0/6 detected. Only SQLi yields any capture, because sqlmap packages the whole "detect → dump → read" chain into one automated step.

> ⚙️ HƯỚNG DẪN: chèn Figure 1 (fig_solve_rate), Figure 2 (fig_by_difficulty), Figure 3 (fig_detect_vs_capture) ở đây; dán Table 3 từ table_detection.csv.

### Arm C — AI-assisted, local model (pilot run)

> ⚙️ HƯỚNG DẪN: đây là 1 phiên mẫu đã chạy thật (nhật ký đầy đủ: docs/report_C.md). Dùng làm case study minh hoạ phương pháp + một quan sát định tính; con số tổng hợp nhánh C chờ chạy đủ mẫu rồi điền `[[…]]`.

As a first, fully logged run we took **XBEN-061-24** (an LFI challenge, easy) with PentestGPT driving the local `qwen2.5:7b` model. The session is instructive. After one weak probe the model prematurely declared the LFI "not exploitable" and drifted toward SQL injection; a single on-task correction from the operator brought it back. Once the operator fed it the real page content, the model produced a working vector — reading `/etc/passwd` through `post.php?id=../../../../etc/passwd` — which **confirmed a genuine exploit, something arm B's scanners never achieved on this target**. It then stalled at the final step: reading the PHP source of the flag file. It tried direct inclusion (executed, nothing shown), a meaningless parameter, and an obsolete null-byte trick, never recalling the correct source-read technique, and finally lapsed into defensive remediation advice and an unrelated file-upload task. The run ended at the 30-minute mark, unsolved, after six human interventions.

| XBEN-061 (LFI, easy) | Outcome |
|---|---|
| Arm B (automated, no-AI) | detected ✓ · **captured ✗** |
| Arm C1 (`qwen2.5:7b`) | **working LFI exploit ✓** (read `/etc/passwd`) · captured ✗ · drifted off-task |

> ⚙️ HƯỚNG DẪN: điền bảng tổng hợp nhánh C khi đủ mẫu —
> [[Table: arm C1/C2 — solve-rate overall; by difficulty; by class; avg time; avg steps; avg tokens; avg manual_interventions; refusal rate.]]
> [[Table 4: memorisation — solve_rate(original) vs solve_rate(hint-free) + delta, cho C1 và C2.]]

### Arm A — manual (pending)

> ⚙️ HƯỚNG DẪN: [[chưa có dữ liệu]]. Khi chạy xong điền: solve-rate tổng, theo độ khó, theo loại, thời gian TB, số bước TB.

## 4.3. Analysis of Results

The dominant pattern in the completed baseline is the distance between detection (55%) and capture (5%). Automation without AI *sees* a vulnerability class in more than half the targets, yet almost never drives it to the flag on its own. SQLi is the single exception, and for a mechanical reason rather than a conceptual one: the exploiter automates the entire chain. Where the vulnerability needs several context-dependent steps — SSTI, XSS — detection is high and capture is zero. [[Khi có arm A/C: so sánh solve-rate ba nhánh theo cùng cách trình bày.]]

## 4.4. Interpretation of Results

Read this way, the 5% figure does not mean the scanner is blind to 95% of the targets; it means the scanner *sees but cannot reach*. The pilot AI session sharpens the same point from the other side: the local model closed part of the detection-to-exploitation gap that defeated arm B — it actually exploited the LFI — but it could not finish, and it wandered off task without a human steering it. Both observations point at the same bottleneck: the multi-step exploitation that sits between recognising a vulnerability and capturing a flag.

## 4.5. Comparison with Literature

These results sit comfortably beside the prior work. The detection-heavy, capture-poor profile of non-AI tooling mirrors the field's finding that step-level competence does not compose into end-to-end success [10]. The AI arm getting further than the scanner yet stalling on the final technique echoes the assisted-versus-autonomous gap in AutoPenBench [5] and the "strong on known patterns, weak on open-ended chaining" summary of the survey [8]. [[Khi có số: so sánh trực tiếp solve-rate nhánh C của nhóm với các mốc đã công bố, vd AWE trên XBOW [8].]]

## 4.6. Implications of the Results

For a practitioner, the practical reading is that a scanner is a good *triage* instrument and a poor *closer*, and that a small local model, in this pilot, behaves as an assistant that needs steering rather than an autonomous operator. [[Hoàn thiện khi có bức tranh ba nhánh đầy đủ.]]

---

# CHAPTER 5. DISCUSSION

> ⚙️ HƯỚNG DẪN: Report 5 (15%). Trả lời từng RQ bằng số liệu + diễn giải rộng, nêu rõ giới hạn. Phần dưới đã viết dựa trên dữ liệu hiện có; mở rộng khi có arm A/C.

## 5.1. Restate the Research Problem or Objectives

The study set out to separate the effect of automation from the effect of a language model in web penetration testing, by running manual, non-AI-automated, and AI-assisted approaches on one shared set of forty targets under one protocol (RQ1–RQ4).

## 5.2. Summarize Key Findings

**On RQ1 and RQ3 (method and vulnerability class).** The firmest result is from the non-AI baseline: the tools detect a vulnerability in 55% of targets but capture the flag in only 5%, and every capture is a SQLi handled by a single packaged exploiter. The gap *is* the finding. The pilot AI session adds a complementary observation — the local model reached a genuine exploit that the scanner could not, which is where the AI's value appears to lie, but it failed to close and lost task focus, which is where its limits appear. [[Củng cố bằng solve-rate ba nhánh khi đủ dữ liệu; trả lời RQ2 theo độ khó.]]

**On RQ4 (memorisation and deployment barriers).** [[Điền Δ memorisation gốc–hint-free của nhánh C.]] On deployment friction, two things already surfaced in practice and belong in the discussion: the local model repeatedly drifted into defensive advice and unrelated tasks, so a human had to keep it on task (six interventions on a single easy target); and the assistant workflow is only as smooth as its tooling, which in our runs required several non-obvious fixes (console compatibility, the `curl.exe` alias trap, a hanging selector dialog) documented in the project runbook. [[Nếu chạy C2-API: báo cáo refusal rate như một kết quả riêng.]]

**Interpretation.** Taken together, the evidence so far is consistent with viewing AI as an *accelerating, human-in-the-loop assistant* rather than a replacement for the tester, at least for a small local model on classes that need contextual reasoning. This lines up with the broader literature [5], [8], [10] and is exactly why the design counts human interventions rather than assuming autonomy.

## 5.2. Threats to Validity

> ⚙️ HƯỚNG DẪN: giữ văn phong thẳng, mỗi mối đe doạ kèm cách giảm thiểu. Khi có đủ số nhánh C, rà lại các con số trong mục này.

**Construct and measurement.** The non-AI detection figure is produced by a keyword heuristic over tool output and is read as an *optimistic upper bound* on automated recognition, not a precise rate; an earlier version over-counted it (a tool-name substring and generic version-EOL findings), which we corrected and re-ran. Capture, by contrast, is exact-match against the ground-truth flag and is not subject to this noise. Vulnerability classes come from the benchmark's first metadata tag and are approximate; where a target carries several tags the non-AI exploiter runs all of them, but the per-class breakdown should be read with that labelling caveat.

**Internal validity — the AI arm.** Three threats are specific to Arm C and bear directly on how far its results can be pushed. (i) *Sample size.* Arm C runs on a purposive subset of twelve targets, not all forty, so it is reported as a paired, per-class analysis and an existence proof of capability rather than a population solve-rate; we do not claim a percentage that generalises. (ii) *Information parity and the human boundary.* Arm C is told the vulnerability *class* — the same information the non-AI pipeline uses to select its exploiter — but must discover the endpoint, parameter and technique itself; the operator never supplies the exploit payload, and any session where that line is crossed is scored unsolved and flagged. We also separate mechanical command execution from genuine *redirects* and count only the latter as interventions, though that split retains some grader subjectivity. (iii) *Operator leakage.* Because Arm C is compared against Arm B on the same targets, an operator who ran B first already knows the target; we mitigate by running C before reading the B log for that target, or by assigning a different operator, and acknowledge the residual risk.

**The memorisation measure.** The original-versus-hint-free delta is our handle on benchmark saturation, but it conflates two effects: removing hints visible in the page over HTTP, and genuine training-set memorisation. It reduces the saturation problem without eliminating it. Hint-free runs should use a different operator or order from the original runs to limit cross-contamination, and the cleaner long-term fix is freshly generated post-cutoff targets (Section 6.2).

**External validity.** Targets are forty CTF-style web applications, not production systems, and the Arm C subset is deliberately skewed toward easy targets to give a small local model its best chance — so failures there are strong negative evidence, but successes do not extend to hard targets. The AI arm is anchored on one 4-bit-quantised 7B local model, which is a conservative lower bound on "AI-assisted" performance, not a ceiling; a hosted model (Arm C2, deferred) would likely raise it. Only 21 of 40 targets have a dedicated non-AI exploiter, so Arm B's weakness on IDOR, logic and deserialisation classes reflects a *tooling* limit, not automation in general.

**Reproducibility.** All Docker-compatibility patches are environment-only and logged in `patches.log`; none alters a vulnerability or flag. The manual arm carries the usual human-grader subjectivity, bounded by the fixed 30-minute budget and exact-match scoring shared across all arms.

---

# CHAPTER 6. CONCLUSION AND FUTURE WORK

> ⚙️ HƯỚNG DẪN: Report 6 (5%). Kết luận là TỔNG HỢP, không phải tóm tắt lại. Bổ sung câu chốt khi có đủ ba nhánh.

## 6.1. Conclusion

We built a controlled, three-arm comparison of manual, non-AI-automated, and AI-assisted web penetration testing on one shared set of forty CTF targets, so that the automation effect and the AI effect could be read apart. The completed non-AI baseline gives a clear and, we think, useful result: classic tools recognise a vulnerability class in 55% of targets but capture the flag in only 5%, with the sole exceptions being SQL injection handled end-to-end by a dedicated exploiter. A first fully logged AI-assisted session reaches further than the scanner — it produced a working LFI exploit the scanner could not — but stalls at the multi-step finish and loses focus without a human guiding it. The recurring bottleneck across both arms is the span between *detecting* a vulnerability and *chaining it* to a captured flag. [[Câu kết luận cuối cùng về vị trí của AI — trợ lý tăng tốc hay thay thế — chốt lại khi có số liệu đầy đủ của ba nhánh.]]

## 6.2. Future Work

Several extensions follow naturally. Widen the sample and add **authorised real-world targets** to test outside the CTF setting. Compare more model families, local and hosted, and newer autonomous agent frameworks. Replace the hint-removal workaround with **freshly generated, post-cutoff** benchmarks that remove memorisation by construction rather than reducing it. And study the human-intervention trace in detail: precisely which steps the human supplies that the model cannot, since that is where the division of labour between tester and AI really lives.

---

# REFERENCES

> ⚙️ HƯỚNG DẪN: IEEE style, đánh số theo thứ tự xuất hiện trong văn. [1]–[3] xác minh trực tiếp; [4]–[7],[9],[10] đã kiểm; [8] xác minh từ bản PDF đầy đủ. Mở lại bản gốc các nguồn trích "gián tiếp qua survey" ([9],[10] và AWE) để xác nhận số trước khi nộp. Trong Word nên dùng công cụ trích dẫn tự động.

[1] G. Deng, Y. Liu, V. Mayoral-Vilches, P. Liu, Y. Li, Y. Xu, T. Zhang, Y. Liu, M. Pinzger, and S. Rass, "PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing," in *Proc. 33rd USENIX Security Symposium*, 2024, pp. 847–864.

[2] XBOW Engineering, "Validation Benchmarks," 2024. [Online]. Available: https://github.com/xbow-engineering/validation-benchmarks

[3] KeygraphHQ, "XBOW Validation Benchmarks (hint-free fork)," 2025. [Online]. Available: https://github.com/KeygraphHQ/xbow-validation-benchmarks

[4] R. Fang, R. Bindu, A. Gupta, and D. Kang, "LLM Agents can Autonomously Exploit One-day Vulnerabilities," *arXiv preprint* arXiv:2404.08144, 2024.

[5] L. Gioacchini, A. Delsanto, I. Drago, M. Mellia, G. Siracusano, and R. Bifulco, "AutoPenBench: A Vulnerability Testing Benchmark for Generative Agents," in *Proc. 2025 Conf. on Empirical Methods in Natural Language Processing (Industry Track)*, 2025, pp. 1615–1624. (arXiv:2410.03225)

[6] L. Muzsai, D. Imolai, and A. Lukács, "HackSynth: LLM Agent and Evaluation Framework for Autonomous Penetration Testing," *arXiv preprint* arXiv:2412.01778, 2024.

[7] Y. Zhu, A. Kellermann, D. Bowman, P. Li, A. Gupta, A. Danda, R. Fang, C. Jensen, E. Ihli, J. Benn, et al., "CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application Vulnerabilities," in *Proc. 42nd Int. Conf. on Machine Learning (ICML)*, PMLR vol. 267, 2025, pp. 79850–79867. (arXiv:2503.17332)

[8] Z. He, J. Dong, Z. Li, T. Chen, G. Deng, F. Luo, J. Ji, Y. Cao, and X. Luo, "A Survey of LLM-Driven Penetration Testing: Taxonomy, Co-Evolution, and Open Challenges," *arXiv preprint* arXiv:2607.02605, 2026.

[9] D. Lee, G.-e. Bae, and I. Yun, "CTFusion: A CTF-based Benchmark for LLM Agent Evaluation," *arXiv preprint* arXiv:2605.11504, 2026.

[10] R. Yang, M. Cheng, G. Deng, T. Zhang, J. Wang, and X. Xie, "PentestEval: Benchmarking LLM-based Penetration Testing with Modular and Stage-level Design," *arXiv preprint* arXiv:2512.14233, 2025.

> ⚙️ HƯỚNG DẪN: nếu trích AWE trong văn, thêm: A. S. Jaswal and A. Baghel, "AWE: Adaptive Agents for Dynamic Web Penetration Testing," in *Proc. NDSS Workshop (LAST-X)*, 2026 — và xác minh bản gốc trước.

---

# APPENDICES

> ⚙️ HƯỚNG DẪN: đính kèm hoặc trỏ tới dữ liệu thô để hội đồng kiểm chứng (tăng độ tin cậy, chống nghi ngờ bịa số).

- **Appendix A — Raw results.** `project/results/results.csv` (one row per run).
- **Appendix B — Arm C session log.** `docs/report_C.md` (turn-by-turn reproduction of the pilot AI session).
- **Appendix C — Analysis code.** `project/analysis/analyze.py`.
- **Appendix D — Reproducibility.** Build harness and compatibility log: `project/harness/build_target.py`, `project/harness/patches.log`. Operator guide: `docs/RUNBOOK.md`.
- **Appendix E — Repository.** https://github.com/VuNguyenBinh/KLTN-FA26
