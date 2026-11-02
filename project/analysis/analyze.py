"""
Phan tich ket qua so sanh 3 nhanh A/B/C.
Chay:  python analyze.py ../results/results.csv
Yeu cau: pip install pandas matplotlib
Xuat: bang tong hop (stdout) + bieu do trong ../../paper/figures/
"""
import sys
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "paper", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

ARM_ORDER = ["A_manual", "B_auto", "C_ai_local", "C_ai_api"]
ARM_LABEL = {
    "A_manual": "A: Manual",
    "B_auto": "B: Automated",
    "C_ai_local": "C1: AI (local)",
    "C_ai_api": "C2: AI (API)",
}


def load(path):
    df = pd.read_csv(path)
    if "variant" not in df.columns:
        df["variant"] = "original"
    df["variant"] = (df["variant"].astype(str).str.strip().str.lower()
                     .replace({"": "original", "nan": "original"}))
    truth = {"1": 1, "y": 1, "yes": 1, "true": 1,
             "0": 0, "n": 0, "no": 0, "false": 0}

    def to_bool(v):
        # Tra 1/0 neu dien, None neu trong/khong ro. Xu ly ca "1.0" (khi pandas doc thanh float).
        if pd.isna(v):
            return None
        sv = str(v).strip().lower()
        if sv in ("", "nan", "none"):
            return None
        if sv.endswith(".0"):
            sv = sv[:-2]
        return truth.get(sv)  # None neu gia tri la

    # 'detected' (phat hien lo hong, khac voi bat flag) nam trong cot 'notes'
    # duoi dang "detected=yes/no" (chi nhanh B ghi). Boc ra thanh cot rieng.
    # Dong khong co chu 'detected=' -> None -> tu bi loai khoi bang detection.
    import re
    def parse_detected(note):
        if pd.isna(note):
            return None
        mm = re.search(r"detected\s*=\s*(yes|no)", str(note), re.IGNORECASE)
        if not mm:
            return None
        return 1 if mm.group(1).lower() == "yes" else 0
    df["detected"] = (df["notes"].map(parse_detected)
                      if "notes" in df.columns else None)

    # QUAN TRONG: dong CHUA chay (solved trong) -> None -> bi loai, KHONG tinh la fail.
    df["solved"] = df["solved"].map(to_bool)
    if "llm_refused" in df.columns:
        df["llm_refused"] = df["llm_refused"].map(to_bool).fillna(0).astype(int)
    for col in ["time_minutes", "num_steps", "tokens_used", "manual_interventions"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # chi giu cac dong DA CHAY (cot solved da dien 0/1); dong trong bi loai that su
    df = df[df["solved"].notna()].copy()
    df["solved"] = df["solved"].astype(int)
    return df


def summary_table(df):
    # So sanh 3 nhanh tren CUNG dieu kien: variant=original (A/B chi co original)
    d = df[df["variant"] == "original"]
    g = d.groupby("arm")
    out = pd.DataFrame({
        "n_runs": g.size(),
        "solve_rate_%": (g["solved"].mean() * 100).round(1),
        "avg_time_min": g["time_minutes"].mean().round(1),
        "avg_steps": g["num_steps"].mean().round(1),
        "avg_tokens": g["tokens_used"].mean().round(0),
        "avg_manual_interv": g["manual_interventions"].mean().round(1),
        "refusal_rate_%": (g["llm_refused"].mean() * 100).round(1),
    })
    out = out.reindex([a for a in ARM_ORDER if a in out.index])
    return out


def solve_rate_by_difficulty(df):
    d = df[df["variant"] == "original"]
    t = (d.groupby(["difficulty", "arm"])["solved"].mean() * 100).round(1).unstack("arm")
    cols = [a for a in ARM_ORDER if a in t.columns]
    return t[cols]


def solve_rate_by_category(df):
    d = df[df["variant"] == "original"]
    t = (d.groupby(["vuln_category", "arm"])["solved"].mean() * 100).round(1).unstack("arm")
    cols = [a for a in ARM_ORDER if a in t.columns]
    return t[cols]


def detection_table(df):
    """CHI NHANH B: phat hien lo hong (detected) vs bat duoc flag (solved).
    Detection chi co y nghia voi scanner tu dong; A/C khong co tin hieu nay."""
    d = df[(df["arm"] == "B_auto") & (df["variant"] == "original")].copy()
    d = d[d["detected"].notna()]
    if d.empty:
        return None, None, None
    d["detected"] = d["detected"].astype(int)
    overall = pd.DataFrame({
        "n": [len(d)],
        "detect_rate_%": [round(d["detected"].mean() * 100, 1)],
        "capture_rate_%": [round(d["solved"].mean() * 100, 1)],
    }, index=["B_auto"])
    by_diff = d.groupby("difficulty").agg(
        n=("detected", "size"),
        detect_rate_pct=("detected", lambda s: round(s.mean() * 100, 1)),
        capture_rate_pct=("solved", lambda s: round(s.mean() * 100, 1)),
    )
    by_cat = d.groupby("vuln_category").agg(
        n=("detected", "size"),
        detect_rate_pct=("detected", lambda s: round(s.mean() * 100, 1)),
        capture_rate_pct=("solved", lambda s: round(s.mean() * 100, 1)),
    ).sort_values("detect_rate_pct", ascending=False)
    return overall, by_diff, by_cat


def bar_detect_vs_capture(by_diff):
    fig, ax = plt.subplots(figsize=(6, 4))
    x = range(len(by_diff))
    w = 0.38
    order = [d for d in ["easy", "medium", "hard"] if d in by_diff.index]
    t = by_diff.reindex(order)
    ax.bar([i - w / 2 for i in x], t["detect_rate_pct"], w, label="Detected (phat hien)")
    ax.bar([i + w / 2 for i in x], t["capture_rate_pct"], w, label="Captured (bat flag)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(list(t.index))
    ax.set_ylabel("Rate (%)")
    ax.set_title("Arm B: phat hien vs bat flag theo do kho")
    ax.set_ylim(0, 100)
    ax.legend()
    fig.tight_layout()
    p = os.path.join(FIG_DIR, "fig_detect_vs_capture.png")
    fig.savefig(p, dpi=150)
    print(f"[fig] {p}")


def memorization_table(df):
    """Dong gop chinh: nhanh AI tren ban goc vs hint-free. Delta = muc 'hoc thuoc'."""
    ai = df[df["arm"].isin(["C_ai_local", "C_ai_api"])]
    if ai.empty:
        return None
    t = (ai.groupby(["arm", "variant"])["solved"].mean() * 100).round(1).unstack("variant")
    for col in ["original", "hintfree"]:
        if col not in t.columns:
            t[col] = float("nan")
    t = t[["original", "hintfree"]]
    t["delta_hoc_thuoc"] = (t["original"] - t["hintfree"]).round(1)
    return t.reindex([a for a in ARM_ORDER if a in t.index])


def bar_solve_rate(summary):
    fig, ax = plt.subplots(figsize=(6, 4))
    arms = list(summary.index)
    ax.bar([ARM_LABEL.get(a, a) for a in arms], summary["solve_rate_%"])
    ax.set_ylabel("Solve rate (%)")
    ax.set_title("Overall solve rate by method")
    ax.set_ylim(0, 100)
    for i, v in enumerate(summary["solve_rate_%"]):
        ax.text(i, v + 1, f"{v}", ha="center")
    fig.tight_layout()
    p = os.path.join(FIG_DIR, "fig_solve_rate.png")
    fig.savefig(p, dpi=150)
    print(f"[fig] {p}")


def grouped_by_difficulty(diff_table):
    fig, ax = plt.subplots(figsize=(7, 4))
    diff_table.plot(kind="bar", ax=ax)
    ax.set_ylabel("Solve rate (%)")
    ax.set_title("Solve rate by difficulty")
    ax.set_ylim(0, 100)
    ax.legend([ARM_LABEL.get(c, c) for c in diff_table.columns], fontsize=8)
    fig.tight_layout()
    p = os.path.join(FIG_DIR, "fig_by_difficulty.png")
    fig.savefig(p, dpi=150)
    print(f"[fig] {p}")


def bar_memorization(mem):
    fig, ax = plt.subplots(figsize=(6, 4))
    arms = list(mem.index)
    x = range(len(arms))
    w = 0.38
    ax.bar([i - w / 2 for i in x], mem["original"], w, label="Ban goc")
    ax.bar([i + w / 2 for i in x], mem["hintfree"], w, label="Hint-free")
    ax.set_xticks(list(x))
    ax.set_xticklabels([ARM_LABEL.get(a, a) for a in arms])
    ax.set_ylabel("Solve rate (%)")
    ax.set_title("Hieu ung 'AI hoc thuoc': goc vs hint-free")
    ax.set_ylim(0, 100)
    ax.legend()
    fig.tight_layout()
    p = os.path.join(FIG_DIR, "fig_memorization.png")
    fig.savefig(p, dpi=150)
    print(f"[fig] {p}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <results.csv>")
        sys.exit(1)
    df = load(sys.argv[1])
    if df.empty:
        print("Chua co du lieu (chua ghi cot 'solved').")
        return

    n_orig = (df["variant"] == "original").sum()
    print(f"[info] {len(df)} luot da chay | original={n_orig} | hintfree={len(df) - n_orig}")

    print("\n=== BANG 1: Tong hop theo nhanh (variant=original) ===")
    summary = summary_table(df)
    print(summary.to_string())

    print("\n=== BANG 2: Solve rate theo do kho (%, original) ===")
    diff = solve_rate_by_difficulty(df)
    print(diff.to_string())

    print("\n=== BANG 3: Solve rate theo loai lo hong (%, original) ===")
    print(solve_rate_by_category(df).to_string())

    print("\n=== BANG 3b: Phat hien vs bat flag — CHI NHANH B (original) ===")
    det_overall, det_diff, det_cat = detection_table(df)
    if det_overall is not None:
        print(det_overall.to_string())
        print("\n-- theo do kho --")
        print(det_diff.to_string())
        print("\n-- theo loai lo hong (sap theo ty le phat hien) --")
        print(det_cat.to_string())
        det_cat.to_csv(os.path.join(FIG_DIR, "table_detection.csv"))
        bar_detect_vs_capture(det_diff)
    else:
        print("(chua co du lieu 'detected' cua nhanh B)")

    print("\n=== BANG 4: Hieu ung 'AI hoc thuoc' (nhanh C: goc vs hint-free) ===")
    mem = memorization_table(df)
    if mem is not None:
        print(mem.to_string())
        mem.to_csv(os.path.join(FIG_DIR, "table_memorization.csv"))
        bar_memorization(mem)
    else:
        print("(chua co du lieu nhanh C)")

    bar_solve_rate(summary)
    grouped_by_difficulty(diff)

    # xuat bang ra csv de dua vao bai bao
    summary.to_csv(os.path.join(FIG_DIR, "table_summary.csv"))
    diff.to_csv(os.path.join(FIG_DIR, "table_by_difficulty.csv"))
    print("\nDa xuat bang va bieu do vao paper/figures/")


if __name__ == "__main__":
    main()
