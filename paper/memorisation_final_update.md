# Paper update — final hint-free / RQ4 (port thủ công sang paper_ieee.tex)

> Soạn 26/11/2026 sau khi hint-free HOÀN TẤT (26/26 lượt: 13 bài gốc-giải × 2 lần). Dưới đây là **văn bản thay thế** cho 3 vị trí trong `paper_ieee.tex` (+ abstract THESIS_FULL.md). Giọng văn giữ khớp bản IEEE hiện tại. Figure `fig_memorization.png` đã regenerate theo số final.

**Số chốt:** 13 bài gốc-giải chạy hint-free ×2 = 26 lượt. 11/13 vẫn giải; 2 bài (XSS khó 010/087) rớt cả 2 run ở khâu craft payload letterless (không phải nhận-bài). Dao động run-to-run hai chiều. 2 bài gốc-trượt lại giải khi hint-free (Δ ngược). Bảng 4: original 54.2% vs hint-free 68.4% → Δ = −14.2 (âm). Refusal: commercial API (APIVN content-filter) từ chối một số payload smuggling/injection trong lúc chạy hint-free (HTTP 400); model local không gặp.

---

## [A] Thay câu RQ4 trong đoạn tổng quan kết quả (paper_ieee.tex ~dòng 279)

**Thay:** *"On RQ4, one of the three barriers is answered directly: no arm produced a model refusal. ... Memorisation we could not measure cleanly with the hint-removed runs completed so far, so we report it as a limitation and a target for future work rather than a result, for the reasons set out in Section~\ref{sec:threats}."*

**Bằng:**
> On RQ4, the three deployment barriers now have answers. Model refusals do occur, but only on the commercial API: its content filter rejected a request-smuggling payload and, during the hint-removed re-runs, several injection payloads mid-session, each returned as an HTTP 400 from the gateway, whereas the local model, which runs without such a filter, never refused — a barrier that is a property of the hosted deployment rather than of the task. The running cost tracked reasoning turns rather than attack volume, the clearest instance being a hint-removed session that drove roughly one hundred thousand brute-force requests at a local target over nineteen minutes at essentially zero API cost; we did not log cost uniformly enough to report a full accounting, so we give it qualitatively. Memorisation, which we could earlier only flag as a limitation, we now measure directly by re-running every originally-solved target on a hint-removed copy, twice each, and the result shows no positive delta, as detailed in Section~\ref{sec:threats}.

---

## [B] Thay đoạn "Memorisation." trong Threats to Validity (paper_ieee.tex ~dòng 290–291)

**Thay toàn bộ đoạn** bắt đầu *"\textbf{Memorisation.} The benchmark is public ..."* **bằng:**
> \textbf{Memorisation.}
> The benchmark is public, so a high score on a class may reflect recall rather than discovery. One form of this leakage is ruled out by construction. The scoring flag is not the one in the public repository but is regenerated at build time by our harness; the model is given only the vulnerability class and the target URL rather than the benchmark identifier; and a language model cannot compute the SHA-256 in any case, so a correct flag cannot be recalled from training and can only come from exploiting the live target. What this does not rule out is recall of the method — recognising a target and replaying a known technique. Our quantitative handle on this is a hint-removed variant of each target, drawn from a public hint-free fork of the benchmark~\cite{keygraph2025}, on which we re-ran every target the commercial model had solved on the original. Because the model is stochastic, a single run per variant conflates memorisation with ordinary run-to-run variance, so we ran each hint-removed target twice: thirteen originally-solved targets, twenty-six runs in all. The result shows no sign of memorisation-driven scoring. Eleven of the thirteen targets remained solved on the hint-removed copy; the two that dropped were the hardest cross-site-scripting targets, where the model fails at crafting a letterless payload, a step that the removed identity hints would not have helped, rather than at recognising the task. The run-to-run variation went in both directions, with targets that failed on the first hint-removed run but succeeded on the second and the reverse, and two targets that the model had failed on the original were in fact solved on the hint-removed copy, a negative delta that is the opposite of what memorisation predicts. At the aggregate level the hint-removed solve rate does not fall below the original, standing at 68\% against 54\% across the runs (Table~\ref{tab:memorisation}, Figure~\ref{fig:memorisation}). We read the sign of this delta rather than its magnitude: the increase is inflated by selection bias, because the hint-removed set is drawn from originally-solved targets and counts multiple runs, so we do not claim a quantified zero delta. The claim we do make is narrower and well supported, that the model does not win by memorisation: the drop that memorisation would produce does not appear, and when an identity hint is genuinely removed the model re-derives the path from scratch, in one case down to re-guessing by brute force the default credentials that the hint had previously supplied. A fully clean quantitative delta still needs more runs per variant or freshly generated post-cutoff targets, which we leave to future work.

---

## [C] Thay câu memorisation trong Future work (paper_ieee.tex ~dòng 306)

**Thay:** *"The memorisation delta can be measured properly, with at least two runs per variant or a deterministic decoding configuration, and better still with freshly generated post-cutoff targets that remove memorisation by construction."*

**Bằng:**
> The memorisation delta, which we now measure as a sign rather than a magnitude, can be sharpened into a clean quantity with more runs per variant across both the original and hint-removed copies, a deterministic decoding configuration, and, best of all, freshly generated post-cutoff targets that remove memorisation by construction.

---

## [D] Abstract (THESIS_FULL.md ~dòng 53) — thay placeholder

**Thay** cụm *"[[Điền kết quả nhánh người ...]]"* **và câu memorisation** bằng ý:
> On the hint-removed copies, re-running every target the commercial model had solved, twice each, produces no positive memorisation delta — eleven of thirteen stay solved, the two that drop fail at payload crafting rather than recognition, and the hint-removed rate (68\%) does not fall below the original (54\%) — so we report that the model does not win by memorisation, while noting that the selection-biased sample lets us read only the sign of the delta, not a quantified zero.

---

## Ghi chú figure/table (đã sẵn, không vẽ mới)
- `paper/figures/fig_memorization.png` — Bảng 4 trực quan (original vs hint-free theo nhánh), đã regenerate số final. Dùng `\includegraphics` như cũ.
- `paper/figures/table_memorization.csv` — nguồn Bảng 4 (`\ref{tab:memorisation}`).
- Nếu muốn mạnh hơn: có thể thêm biểu đồ paired per-bench (gốc vs hint-free từng bài) — mục Future chart, chưa bắt buộc.
