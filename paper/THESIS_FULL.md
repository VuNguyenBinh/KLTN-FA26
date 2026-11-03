<!--
==============================================================================
 HƯỚNG DẪN SỬ DỤNG FILE NÀY  (đọc trước — xoá cả khối comment này khi nộp)
==============================================================================
Đây là bản LẮP GHÉP các draft (paper/draft_*.md) vào đúng khung luận văn FPT
(6 chương, theo IAP491_CP_StudentsGuideForm). Ngôn ngữ: tiếng Anh (quy định trường).

CÁCH DÙNG:
1. Mỗi khối "> ⚙️ HƯỚNG DẪN:" là chỉ dẫn cho nhóm — XOÁ hết trước khi nộp.
2. Mỗi "[[... ]]" là chỗ CHỜ SỐ LIỆU (nhánh Truyền thống — tầng người + nhánh AI).
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
6. Dữ liệu thật: project/results/results.csv ; log nhánh AI: docs/report_C.md ;
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

> ⚙️ HƯỚNG DẪN: Abstract phải tự đứng một mình: KHÔNG viết tắt chưa định nghĩa, KHÔNG URL, KHÔNG trích dẫn. Giữ 200–300 từ. Điền `[[…]]` khi có số nhánh người (traditional) và nhánh AI. Giữ 4 ý ẩn (Background/Methods/Results/Conclusions) nhưng KHÔNG in tiêu đề.

Automated security tools that use large language models now report high success rates on penetration-testing benchmarks, yet those numbers are rarely obtained under the same conditions as a human tester or a classic scanner, which makes them hard to trust. This study tackles that gap with a controlled, three-arm comparison on a single target set. We run forty web capture-the-flag challenges, drawn by stratified sampling from the XBOW validation benchmarks, through three arms under identical rules: a **traditional** arm in which a human tester works by hand with the standard non-AI tools, and two **AI-assisted** arms that pair a human operator with a language model, one local and one a commercial API. Every run is scored by exact-match flag capture and logged for time, number of steps, human interventions, and tool-refusal events; the AI arms are additionally run against a hint-removed copy of each target so that we can estimate how much of their performance is memorisation rather than reasoning. Within the traditional arm, the automated tooling on its own detects a vulnerability in 11 of 40 targets (27.5%) but captures the flag in only 2 (5%), a gap that exposes where automation stalls: recognising a vulnerability class is far easier than chaining a multi-step exploit to the flag, and several classes are not even recognised. [[Điền kết quả nhánh người (traditional) và nhánh AI: solve-rate, Δ memorisation, refusal rate.]] The findings suggest that, with a small local model, AI functions as an accelerating assistant rather than a replacement for the human tester, and they make the practical cost of that assistance visible.

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
- Figure 3. Automated tooling — detection vs capture by difficulty (`fig_detect_vs_capture.png`).
- Figure 4. Memorisation effect: original vs hint-free for the AI arm (`fig_memorization.png`, sau khi có số nhánh AI).

# LIST OF TABLES

> ⚙️ HƯỚNG DẪN: các bảng do analyze.py xuất ra (`paper/figures/table_*.csv`):
- Table 1. Summary of metrics per arm.
- Table 2. Solve rate by difficulty.
- Table 3. Detection vs capture by vulnerability class (automated tooling).
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

The backbone of non-AI automation is a family of scanners and class-specific exploiters: template scanners such as nuclei, directory fuzzers such as ffuf, and dedicated tools such as sqlmap for SQL injection, dalfox for cross-site scripting, and SSTImap for template injection. Their strength is quick, repeatable recognition of vulnerability classes that carry a clear signature. Their well-documented weakness lies with business-logic flaws — insecure direct object references, broken access control — and with exploits that take several chained steps, where no static signature captures enough of the context. We use exactly this toolchain as the automated-tooling layer of the traditional arm (recorded as `B_auto`), so that the study's baseline reflects a credible non-AI starting point rather than a strawman.

### Pentest systems built on LLMs

PentestGPT [1] is the reference point. It decomposes an engagement into three self-interacting modules (reasoning, generation, parsing) to keep context from collapsing, and it reports a 58.6% improvement in sub-task completion over direct use of GPT-4, on a benchmark covering the OWASP Top 10; the work received a Distinguished Artifact Award at USENIX Security 2024. We adopt PentestGPT in its assistant ("legacy") mode for the two AI arms, specifically so that the number of human interventions can be counted — a figure that speaks directly to whether AI *replaces* or merely *accelerates* the tester.

A string of later systems extends this line but converges on one message: agents are strong on known CVEs and weak on open-ended, end-to-end tasks. AutoPenBench [5] reports a fully autonomous agent at 21% success across 33 tasks, rising to 64% once a human assists — a gap that is itself an argument for a human-in-the-loop design. HackSynth [6] contributes an autonomous agent and two CTF benchmarks of roughly 200 challenges. CVE-Bench [7] gathers 40 real web-application CVEs and finds the best agent solving at most 12.5% in the one-day setting. PentestEval [10] decomposes an engagement into 346 stage-level tasks and finds end-to-end success for fully autonomous agents still below 6%, i.e. competence at individual steps does not compose into a finished exploit chain. A 2026 systematic survey of 81 papers [8] frames these as structural open problems of the field: unreliable evaluation, weak multi-stage performance, and scarce training data.

### Benchmarks and the saturation problem

The XBOW validation benchmarks [2] are 104 Docker-packaged web CTF challenges, released publicly in late 2024, spanning XSS, SSTI, SQLi, IDOR, SSRF and more; XBOW reports roughly an 85% solve rate for its own system. We chose this set for its determinism (exact-match flags), its container isolation, and its class coverage. That same popularity creates a hazard: once a benchmark is public, a model's score on it may reflect recall rather than discovery. The survey [8] names this as a central reliability concern and notes that binary success metrics cannot separate genuine capability from benchmark alignment. The clearest quantitative evidence comes from CTFusion [9], which compares the same agent on a static benchmark and on live competition and identifies 71 "memorisation events"; removing them drops the mean success rate by 29 percentage points. Worth noting, too, is AWE [8] (a 2026 multi-agent web system), which runs *on the XBOW set we use* and reports 87% success on XSS and 66.7% on blind SQLi — high numbers on our exact benchmark, which both give the AI arm a reference point and sharpen the question of how much of such a figure is memorisation.

## 2.2. Summary of the Literature Review

Two themes run through the prior work. Reported capability keeps climbing, but it is measured in ways that are hard to compare across studies and that may be inflated by contamination; and even the better agents stumble on the multi-step, discovery-heavy tasks that real engagements are made of. The human-assisted variant of AutoPenBench outscoring its autonomous counterpart by a wide margin is the single most telling data point for our design choice.

## 2.3. Contribution of Research

Set against that body of work, our distinguishing move is the **controlled comparison** itself. Rather than evaluating one AI system on one benchmark, we place three approaches side by side on the same targets under the same protocol, which lets us separate the automation effect from the AI effect, and we quantify memorisation and deployment friction directly — aspects that single-score papers tend to pass over. In the spirit of CTFusion's memorisation check [9], but applied to a controlled three-arm comparison rather than a single agent.

---

# CHAPTER 3. METHODOLOGY

> ⚙️ HƯỚNG DẪN: Report 3 (20%). Phần này mô tả thiết kế — viết ở thì hiện tại, đã khớp đúng những gì nhóm chạy. Nhánh người (traditional) và nhánh AI mô tả ở mức giao thức; khi chạy xong chỉ bổ sung số vào Ch.4, KHÔNG sửa Ch.3.

## 3.1. Research Design

This is a controlled, within-subject comparison: all three approaches run on the exact same forty targets, so that any difference reflects the method rather than the target. The three arms are summarised below.

| Arm | Name | Human | LLM | Main tools |
|---|---|---|---|---|
| **1** | Traditional (manual + tools) | Yes (tester) | No | Burp Suite + nuclei, ffuf, sqlmap, dalfox, SSTImap |
| **2** | AI — local model | Yes (in the loop) | Yes (local) | PentestGPT (legacy) + Ollama `qwen2.5:7b` |
| **3** | AI — commercial API | Yes (in the loop) | Yes (commercial) | PentestGPT (legacy) + hosted API |

Arm 1 is traditional penetration testing as practised in the field: a human tester working by hand through Burp and a browser, free to invoke the standard non-AI tools (vulnerability scanners and exploiters), but with no language model anywhere in the loop. We measure this arm in two layers that are kept as separate labels in the data (`A_manual` for the human, `B_auto` for the tools): the *automation layer* is a fixed, identical-for-every-target pipeline whose result is the "automation ceiling" — what classic tooling reaches on its own, used also to quantify the detection-versus-capture gap (Section 4) — and the *human layer* is the tester who may use those same tools. A target counts as solved for the traditional arm if the human or the tooling captures the flag. Arms 2 and 3 are AI-assisted testing in PentestGPT's assistant mode, differing only in the model behind it: a local model (Arm 2) and a commercial hosted model (Arm 3). Arm 2 (local) is the primary AI arm here; Arm 3 is an extension whose task-refusal rate is itself a reported result (Section 3.6).

## 3.2. Data Collection Methods

### Target set and ground truth

Targets come from the XBOW validation benchmarks — 104 Docker-packaged web CTF challenges, each with one planted vulnerability and a secret flag. Each flag follows a deterministic formula, `FLAG{sha256(UPPER(benchmark-id))}`, which we verified against the benchmark's own build pipeline. A target counts as **solved** only when the captured flag matches that string exactly; there is no partial credit.

To deal with saturation we prepare two variants of every challenge: the **original**, and a **hint-removed** fork (from the KeygraphHQ copy [3]) that strips solution hints — comments, suggestive names, README text — while leaving the vulnerability and flag intact. The AI arms run on both variants; the traditional arm (both its human and its tooling layers) runs on the original only, since a scanner and a human tester do not "read" source hints the way a trained model might have memorised them.

### Protocol

Every arm is capped at **30 minutes per target**. The automated tooling enforces this as a cumulative budget across its tool steps. The AI arms follow the assistant loop: the model proposes a step, the human runs it and pastes the result back. We separate the mechanical act of running a proposed command from a genuine *course-correction* (rejecting a wrong step, refusing a hallucinated endpoint, supplying reconnaissance the model should have found, or pulling it back on task) and count only the latter as an intervention (Section 3.4). The human layer of the traditional arm is a tester working through Burp and the same tools, recording time and steps by hand.

### Infrastructure and reproducibility

All targets are built by an automated harness (`build_target.py`) that compiles the image, starts it, finds the web port, waits for a real HTTP response, and records the URL. Two technical points matter for reproducibility and must be declared. First, because the benchmarks date from 2024, several base images are end-of-life; the harness applies a set of *compatibility-only* patches (bumping a broken image, repointing apt to the Debian archive, normalising line endings, randomising fixed ports) and logs every one to `patches.log`. These patches never touch the vulnerability or the flag. Second, because the two variants share a directory name, Docker Compose would otherwise collide them; the harness isolates each with an explicit project name, `-p <id>-<variant>`, so both variants run side by side with distinct images. Hardware: Docker engine 29.8.1; the local model runs under Ollama as `qwen2.5:7b` (4-bit) on an NVIDIA RTX A1000.

## 3.3. Sampling and Data Analysis Techniques

From the 104 challenges we draw a **stratified sample of forty** by difficulty, with a fixed seed (42) for reproducibility: 14 easy, 18 medium, and 8 hard (all eight hard challenges are taken, since there are only eight). Each target is tagged with one or more vulnerability classes from the benchmark metadata.

Each run writes one row to `results.csv` with these fields: solved, time, number of steps, tokens used, manual interventions, LLM-refused, and a free-text note. For the automated tooling we additionally record a **detection** flag — whether the tools signalled a vulnerability at all, even when they could not reach the flag — because that distinction turns out to be central (Chapter 4). Analysis is automated with pandas in `analyze.py`, which produces a per-arm summary, breakdowns by difficulty and by vulnerability class, a detection-versus-capture table for the automated tooling, and the memorisation table for the AI arms. Rows that have not been run (blank `solved`) are dropped, not counted as failures. For the AI arm we compute the memorisation delta as `solve_rate(original) − solve_rate(hint-removed)`: a large delta signals reliance on having *seen* the solution rather than *finding* it.

## 3.4. Limitations of the Methodology

The sample is forty CTF-style challenges, which are not identical to production web applications; the AI arms rest on one model family; and the human layer of the traditional arm carries grader subjectivity. The detection metric for the automated tooling is a string-matching heuristic over tool output, so it can both over- and under-count and should be read as an *optimistic upper bound* on automated recognition, applicable to that tooling only. Only 21 of the 40 targets have a dedicated non-AI exploiter (the rest rely on nuclei+ffuf), so part of the tooling's low capture rate on IDOR/logic/deserialisation classes is a *tool* limitation rather than a property of "automation" in general. The 30-minute cap may cut short the hardest targets, though it does so equally for every arm. Finally, the compatibility patches are an environmental change that we declare rather than hide.

---

# CHAPTER 4. EXPERIMENTAL AND RESULTS

> ⚙️ HƯỚNG DẪN: Report 4 (25%, trọng số CAO). Hiện tầng công cụ tự động (của nhánh Truyền thống) đủ 40/40. Nhánh AI đã có 4 phiên. Tầng người (traditional) đang chạy. Phần dưới trình bày TRUNG THỰC đúng hiện trạng; điền `[[…]]` khi có thêm dữ liệu. TUYỆT ĐỐI không bịa số nhánh người / nhánh AI.

## 4.1. Introduction

This chapter reports the data collected so far. The automated tooling of the traditional arm is complete across all forty original targets; the AI arm is reported from the sessions run so far, with the campaign still in progress; the human layer of the traditional arm is in progress. We present the completed tooling baseline first and in full, then the evidence from the AI arm, and we are explicit about what is measured versus what remains to be collected.

## 4.2. Presentation of Data

### Traditional arm — automated tooling (complete, 40/40)

We report two numbers that must be kept apart: **capture** (the flag was obtained) and **detection** (the tools flagged a vulnerability, even if no flag followed).

**Table 1 (automated tooling).** Over 40 targets, the non-AI tooling **captures the flag in 2/40 (5.0%)** while **detecting a vulnerability in 11/40 (27.5%)**. Mean time was 2.7 minutes per target.

| Metric | Result |
|---|---|
| Flag capture (`solved`) | **2/40 = 5.0%** — XBEN-071, XBEN-083 (both SQLi, via sqlmap database dump) |
| Vulnerability detection | **11/40 = 27.5%** |

**By difficulty (capture / detection):** easy 2/14 = 14.3% / 7/14 = 50.0%; medium 0% / 2/18 = 11.1%; hard 0% / 2/8 = 25.0%.

**By vulnerability class (detection-sorted):** SQLi 2/2 detected and captured (100%); XSS 8/10 detected (dalfox `[POC]`) but 0 captured; CVE 1/1 detected (a genuine nuclei template, not a generic banner). Every remaining class is detected 0 times by the fixed pipeline — including SSTI 0/6 (SSTImap crawled but located no injection point unaided), IDOR 0/6, deserialisation 0/3. Only SQLi yields any capture, because sqlmap packages the whole "detect → dump → read" chain into one automated step.

> ⚙️ HƯỚNG DẪN: chèn Figure 1 (fig_solve_rate), Figure 2 (fig_by_difficulty), Figure 3 (fig_detect_vs_capture) ở đây; dán Table 3 từ table_detection.csv.

### AI arm — local model (sessions so far)

> ⚙️ HƯỚNG DẪN: đây là 1 phiên mẫu đã chạy thật (nhật ký đầy đủ: docs/report_C.md). Dùng làm case study minh hoạ phương pháp + một quan sát định tính; con số tổng hợp nhánh AI chờ chạy đủ mẫu rồi điền `[[…]]`.

As a first, fully logged run we took **XBEN-061-24** (an LFI challenge, easy) with PentestGPT driving the local `qwen2.5:7b` model. The session is instructive. After one weak probe the model prematurely declared the LFI "not exploitable" and drifted toward SQL injection; a single on-task correction from the operator brought it back. Once the operator fed it the real page content, the model produced a working vector — reading `/etc/passwd` through `post.php?id=../../../../etc/passwd` — which **confirmed a genuine exploit, something the automated tooling's scanners never achieved on this target**. It then stalled at the final step: reading the PHP source of the flag file. It tried direct inclusion (executed, nothing shown), a meaningless parameter, and an obsolete null-byte trick, never recalling the correct source-read technique, and finally lapsed into defensive remediation advice and an unrelated file-upload task. The run ended unsolved at twenty-five minutes — inside the thirty-minute budget — after four operator course-corrections (alongside seven mechanical runs of model-proposed commands).

| XBEN-061 (LFI, easy) | Outcome |
|---|---|
| Traditional — automated tooling (no-AI) | detected ✓ · **captured ✗** |
| AI — local (`qwen2.5:7b`) | **working LFI exploit ✓** (read `/etc/passwd`) · captured ✗ · drifted off-task |

> ⚙️ HƯỚNG DẪN: điền bảng tổng hợp nhánh AI khi đủ mẫu —
> [[Table: AI arms (local / commercial-API) — solve-rate overall; by difficulty; by class; avg time; avg steps; avg tokens; avg manual_interventions; refusal rate.]]
> [[Table 4: memorisation — solve_rate(original) vs solve_rate(hint-free) + delta, cho AI local và AI API.]]

### Traditional arm — human tester (in progress)

> ⚙️ HƯỚNG DẪN: [[chưa có dữ liệu]]. Khi chạy xong điền: solve-rate tổng, theo độ khó, theo loại, thời gian TB, số bước TB.

## 4.3. Analysis of Results

The dominant pattern in the completed baseline is the distance between detection (27.5%) and capture (5%) — a roughly five-fold gap. Automation without AI *sees* a vulnerability in only two situations: reflected XSS, which dalfox flags in 8 of 10 targets yet never turns into a captured flag, and SQLi, where sqlmap both detects and captures because it automates the entire chain. Classes that need several context-dependent steps — SSTI, IDOR, deserialisation — are not even detected by the off-the-shelf tools: SSTImap, run unaided, found no injection point in any of the six SSTI targets. [[Khi có đủ số nhánh người (traditional) và nhánh AI: so sánh solve-rate ba nhánh theo cùng cách trình bày.]]

## 4.4. Interpretation of Results

Read this way, the 5% figure does not mean the scanner is blind to 95% of the targets; it means the scanner *sees but cannot reach*. The pilot AI session sharpens the same point from the other side: the local model closed part of the detection-to-exploitation gap that defeated the automated tooling — it actually exploited the LFI — but it could not finish, and it wandered off task without a human steering it. Both observations point at the same bottleneck: the multi-step exploitation that sits between recognising a vulnerability and capturing a flag.

## 4.5. Comparison with Literature

These results sit comfortably beside the prior work. The detection-heavy, capture-poor profile of non-AI tooling mirrors the field's finding that step-level competence does not compose into end-to-end success [10]. The AI arm getting further than the scanner yet stalling on the final technique echoes the assisted-versus-autonomous gap in AutoPenBench [5] and the "strong on known patterns, weak on open-ended chaining" summary of the survey [8]. [[Khi có số: so sánh trực tiếp solve-rate nhánh AI của nhóm với các mốc đã công bố, vd AWE trên XBOW [8].]]

## 4.6. Implications of the Results

For a practitioner, the practical reading is that a scanner is a good *triage* instrument and a poor *closer*, and that a small local model, in this pilot, behaves as an assistant that needs steering rather than an autonomous operator. [[Hoàn thiện khi có bức tranh ba nhánh đầy đủ.]]

---

# CHAPTER 5. DISCUSSION

> ⚙️ HƯỚNG DẪN: Report 5 (15%). Trả lời từng RQ bằng số liệu + diễn giải rộng, nêu rõ giới hạn. Phần dưới đã viết dựa trên dữ liệu hiện có; mở rộng khi có đủ số nhánh người (traditional) và nhánh AI.

## 5.1. Restate the Research Problem or Objectives

The study set out to separate the effect of automation from the effect of a language model in web penetration testing, by running manual, non-AI-automated, and AI-assisted approaches on one shared set of forty targets under one protocol (RQ1–RQ4).

## 5.2. Summarize Key Findings

**On RQ1 and RQ3 (method and vulnerability class).** The firmest result is from the non-AI baseline: the tools detect a vulnerability in 27.5% of targets but capture the flag in only 5%, and every capture is a SQLi handled by a single packaged exploiter. The gap *is* the finding. The pilot AI session adds a complementary observation — the local model reached a genuine exploit that the scanner could not, which is where the AI's value appears to lie, but it failed to close and lost task focus, which is where its limits appear. [[Củng cố bằng solve-rate ba nhánh khi đủ dữ liệu; trả lời RQ2 theo độ khó.]]

**On RQ4 (memorisation and deployment barriers).** [[Điền Δ memorisation gốc–hint-free của nhánh AI.]] On deployment friction, two things already surfaced in practice and belong in the discussion: the local model repeatedly drifted into defensive advice and unrelated tasks, so a human had to keep it on task (four course-corrections on a single easy target); and the assistant workflow is only as smooth as its tooling, which in our runs required several non-obvious fixes (console compatibility, the `curl.exe` alias trap, a hanging selector dialog) documented in the project runbook. [[Nếu chạy nhánh AI API: báo cáo refusal rate như một kết quả riêng.]]

**Interpretation.** Taken together, the evidence so far is consistent with viewing AI as an *accelerating, human-in-the-loop assistant* rather than a replacement for the tester, at least for a small local model on classes that need contextual reasoning. This lines up with the broader literature [5], [8], [10] and is exactly why the design counts human interventions rather than assuming autonomy.

## 5.3. Interpreting the AI Arm's Non-Solves

A reasonable objection is that an AI arm which captures no flags cannot support any conclusion. We argue the opposite. Read against the completed baseline and the session logs, the near-zero result is itself an informative and defensible finding, as long as its claim is stated at the right scope.

The central claim is that on these targets automation, whether the non-AI pipeline or a small local model assisting a human, recognises the class of vulnerability that is present but does not carry the exploitation through to a captured flag. Three strands of evidence support it.

First, the completed non-AI baseline quantifies the gap directly. A vulnerability is detected in 27.5% of targets but a flag is captured in only 5%, a roughly five-fold difference. Every capture is a SQL injection, where sqlmap packages the whole detect-then-dump-then-read chain into a single automated step, whereas the classes that require multi-step contextual reasoning, such as server-side template injection, insecure direct object reference, and business-logic flaws, are not even detected. This gap is measured, not assumed.

Second, the logged AI sessions show that the local model does not close that gap, and they locate precisely where it breaks down. On the file-inclusion target the model went further than the scanner, since it genuinely exploited the flaw and read a system file, yet it stalled at the final step of reading the page source to recover the flag. On the cross-site-scripting target it broke down earlier: given the page's HTML twice, it still could not parse the form field needed to build a correct request, it repeated one wrong command three times, and it ignored two operator corrections; even when the parameter name was supplied directly, its payload was reflected but did not execute. The number of corrective interventions, four on the first target and two on the second, makes the cost of human supervision explicit. Within this sample the local model behaves as a weak assistant that needs continuous steering rather than an autonomous solver.

Third, this low result is consistent with the published literature rather than an artefact of our setup. Autonomous agents reach about 21% on AutoPenBench [5] and at best 12.5% on CVE-Bench [7], and smaller models perform worse still. A local model sitting near zero follows that trend, which points to genuine task difficulty and model scale rather than a flawed experiment.

Stated at its proper scope, the conclusion is therefore that a small, locally hosted language model used as an assistant does not, on this CTF web benchmark, close the detection-to-exploitation gap that the non-AI baseline also leaves open, and that the human supervision cost remains substantial. This claim rests on the evidence above and does not depend on whether the other two arms have been run.

Two questions are deliberately left outside this claim, and we do not prejudge them. Whether a larger hosted model would close the gap is a question for the commercial-API AI arm; we do not assert that artificial intelligence cannot perform penetration testing, only that a small local model does not do so here. Whether a human outperforms both the automated tooling and the AI is a question for the human layer of the traditional arm; should the human solve substantially more while the automated tooling and the local AI remain near zero, the claim strengthens from "the local model does not close the gap" to "within this setting, only the human does." The human layer is therefore pursued to widen the conclusion, not to rescue the AI result.

## 5.4. Threats to Validity

> ⚙️ HƯỚNG DẪN: giữ văn phong thẳng, mỗi mối đe doạ kèm cách giảm thiểu. Khi có đủ số nhánh AI, rà lại các con số trong mục này.

**Construct and measurement.** The non-AI detection figure is produced by a keyword heuristic over tool output and is read as an *optimistic upper bound* on automated recognition, not a precise rate; an earlier version over-counted it at 55% through three substring artefacts — the tool name "SSTImap" matching the token "ssti", generic version-EOL nuclei banners, and the token "injectable" matching the *negative* phrase "not injectable" — which we traced in the raw logs, corrected to class-specific positive signals, and re-scored to the 27.5% reported here. Capture, by contrast, is exact-match against the ground-truth flag and is not subject to this noise. Vulnerability classes come from the benchmark's first metadata tag and are approximate; where a target carries several tags the non-AI exploiter runs all of them, but the per-class breakdown should be read with that labelling caveat.

**Internal validity — the AI arm.** Three threats are specific to the AI arm and bear directly on how far its results can be pushed. (i) *Sample size.* The AI arm runs on a purposive subset of twelve targets, not all forty, so it is reported as a paired, per-class analysis and an existence proof of capability rather than a population solve-rate; we do not claim a percentage that generalises. (ii) *Information parity and the human boundary.* The AI arm is told the vulnerability *class* — the same information the non-AI pipeline uses to select its exploiter — but must discover the endpoint, parameter and technique itself; the operator never supplies the exploit payload, and any session where that line is crossed is scored unsolved and flagged. We also separate mechanical command execution from genuine *redirects* and count only the latter as interventions, though that split retains some grader subjectivity. (iii) *Operator leakage.* Because the AI arm is compared against the automated tooling on the same targets, an operator who ran the tooling first already knows the target; we mitigate by running the AI session before reading the tooling log for that target, or by assigning a different operator, and acknowledge the residual risk.

**The memorisation measure.** The original-versus-hint-free delta is our handle on benchmark saturation, but it conflates two effects: removing hints visible in the page over HTTP, and genuine training-set memorisation. It reduces the saturation problem without eliminating it. Hint-free runs should use a different operator or order from the original runs to limit cross-contamination, and the cleaner long-term fix is freshly generated post-cutoff targets (Section 6.2).

**External validity.** Targets are forty CTF-style web applications, not production systems, and the AI-arm subset is deliberately skewed toward easy targets to give a small local model its best chance — so failures there are strong negative evidence, but successes do not extend to hard targets. The AI arm is anchored on one 4-bit-quantised 7B local model, which is a conservative lower bound on "AI-assisted" performance, not a ceiling; a hosted model (the commercial-API arm, deferred) would likely raise it. Only 21 of 40 targets have a dedicated non-AI exploiter, so the automated tooling's weakness on IDOR, logic and deserialisation classes reflects a *tooling* limit, not automation in general.

**Reproducibility.** All Docker-compatibility patches are environment-only and logged in `patches.log`; none alters a vulnerability or flag. The human layer of the traditional arm carries the usual human-grader subjectivity, bounded by the fixed 30-minute budget and exact-match scoring shared across all arms. Each human session was directly supervised by a group member who recorded timing and step counts in real time; for 37 of the 40 benches, however, the Burp HTTP-history was not exported, so those timing and effort figures rest on the supervisor's contemporaneous notes rather than on saved tool logs (three benches were measured within a live session). We therefore treat the human arm's solve/no-solve outcomes as the firm result and read its time/effort figures (RQ2) with that caveat; future sessions export the tool log as an artifact.

**Traditional-arm tool reference (disclosed).** The traditional arm is run by an independent tester using the standard non-AI toolset with no language model performing any pentest reasoning. We disclose one bounded exception for transparency: the operator was permitted to consult an assistant for *generic tool reference only* — which tools exist for a given vulnerability class and how a tool or repository is used in general — but never for anything specific to a given target (no inspection of a target's responses, no choice of endpoint, parameter or payload, and no interpretation of a target's output toward the solution). Each such consultation is flagged in the run's notes. This keeps the exploitation reasoning human, but a strict reader may still prefer the stricter protocol of no assistant in the loop at all; we therefore report it openly rather than claim an absolute AI-free human arm.

---

# CHAPTER 6. CONCLUSION AND FUTURE WORK

> ⚙️ HƯỚNG DẪN: Report 6 (5%). Kết luận là TỔNG HỢP, không phải tóm tắt lại. Bổ sung câu chốt khi có đủ ba nhánh.

## 6.1. Conclusion

We built a controlled, three-arm comparison of manual, non-AI-automated, and AI-assisted web penetration testing on one shared set of forty CTF targets, so that the automation effect and the AI effect could be read apart. The completed non-AI baseline gives a clear and, we think, useful result: classic tools recognise a vulnerability class in 27.5% of targets but capture the flag in only 5%, with the sole exceptions being SQL injection handled end-to-end by a dedicated exploiter. A first fully logged AI-assisted session reaches further than the scanner — it produced a working LFI exploit the scanner could not — but stalls at the multi-step finish and loses focus without a human guiding it. The recurring bottleneck across both arms is the span between *detecting* a vulnerability and *chaining it* to a captured flag. [[Câu kết luận cuối cùng về vị trí của AI — trợ lý tăng tốc hay thay thế — chốt lại khi có số liệu đầy đủ của ba nhánh.]]

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
- **Appendix B — AI-arm session log.** `docs/report_C.md` (turn-by-turn reproduction of the AI sessions).
- **Appendix C — Analysis code.** `project/analysis/analyze.py`.
- **Appendix D — Reproducibility.** Build harness and compatibility log: `project/harness/build_target.py`, `project/harness/patches.log`. Operator guide: `docs/RUNBOOK.md`.
- **Appendix E — Repository.** https://github.com/VuNguyenBinh/KLTN-FA26
