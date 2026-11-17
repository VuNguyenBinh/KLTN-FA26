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
ARM_SHORT = {"A_manual": "A", "C_ai_local": "C1", "C_ai_api": "C2"}
ARM_COLOR = {"A_manual": "#4E8FC7", "C_ai_local": "#E0A33C", "C_ai_api": "#58B97E"}


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
    # Gop lan chay-lai cung 1 target (vd 032 restart sau khi moi truong loi):
    # moi (arm, benchmark_id, variant) chi tinh 1 lan, uu tien attempt DA GIAI.
    key = ["arm", "benchmark_id", "variant"]
    if all(k in df.columns for k in key):
        before = len(df)
        df = (df.sort_values("solved")
                .drop_duplicates(subset=key, keep="last")
                .reset_index(drop=True))
        if len(df) < before:
            print(f"[dedup] gop {before - len(df)} dong chay-lai (moi target tinh 1 lan)")
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
    ax.bar([i - w / 2 for i in x], t["detect_rate_pct"], w, label="Vulnerability detected")
    ax.bar([i + w / 2 for i in x], t["capture_rate_pct"], w, label="Flag captured")
    ax.set_xticks(list(x))
    ax.set_xticklabels(list(t.index))
    ax.set_ylabel("Rate (%)")
    ax.set_xlabel("Difficulty")
    ax.set_title("Tools-only layer: detection vs. capture by difficulty")
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
    ax.bar([i - w / 2 for i in x], mem["original"], w, label="Original")
    ax.bar([i + w / 2 for i in x], mem["hintfree"], w, label="Hint-free")
    ax.set_xticks(list(x))
    ax.set_xticklabels([ARM_LABEL.get(a, a) for a in arms])
    ax.set_ylabel("Solve rate (%)")
    ax.set_title("Memorisation check: original vs. hint-free")
    ax.set_ylim(0, 100)
    ax.legend()
    fig.tight_layout()
    p = os.path.join(FIG_DIR, "fig_memorization.png")
    fig.savefig(p, dpi=150)
    print(f"[fig] {p}")


# ===================== SO SANH THEO CAP (paired on shared) =====================
# Cac nhanh chay so bai khac nhau, nen so cong bang = so tren DUNG nhung bai
# ca hai (hoac ca ba) nhanh cung chay. Day la cac bieu do tuong ung slide ket qua.

def shared_sets(df):
    d = df[df["variant"] == "original"]
    by = {a: set(d[d["arm"] == a]["benchmark_id"]) for a in d["arm"].unique()}
    A = by.get("A_manual", set())
    C1 = by.get("C_ai_local", set())
    C2 = by.get("C_ai_api", set())
    return (A & C1 & C2), (A & C2)


def paired_agg(df, ids, arms):
    d = df[(df["variant"] == "original") & (df["benchmark_id"].isin(ids))]
    res = {}
    for a in arms:
        da = d[d["arm"] == a]
        res[a] = {
            "solved": int(da["solved"].sum()),
            "n": len(da),
            "steps": round(da["num_steps"].mean(), 1),
            "time": round(da["time_minutes"].mean(), 1),
            "interv": round(da["manual_interventions"].mean(), 1),
        }
    return res


def mcnemar_exact(b, c):
    """p hai phia chinh xac (binomial) tren cac cap LECH nhau b vs c."""
    from math import comb
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) * (0.5 ** n))


def discordant(df, ids, a1, a2):
    d = df[(df["variant"] == "original") & (df["benchmark_id"].isin(ids))]
    s1 = dict(zip(d[d["arm"] == a1]["benchmark_id"], d[d["arm"] == a1]["solved"]))
    s2 = dict(zip(d[d["arm"] == a2]["benchmark_id"], d[d["arm"] == a2]["solved"]))
    b = c = 0
    for i in ids:
        if i in s1 and i in s2:
            if s1[i] == 1 and s2[i] == 0:
                b += 1
            elif s1[i] == 0 and s2[i] == 1:
                c += 1
    return b, c


def paired_panels(path, suptitle, arms, panels):
    fig, axs = plt.subplots(1, len(panels), figsize=(3.6 * len(panels), 3.8))
    if len(panels) == 1:
        axs = [axs]
    for ax, (ptitle, vals, ylab) in zip(axs, panels):
        xs = range(len(arms))
        ax.bar(xs, [vals[a] for a in arms], width=0.6,
               color=[ARM_COLOR[a] for a in arms])
        for i, a in enumerate(arms):
            v = vals[a]
            if v is not None and v == v:  # khong NaN
                ax.text(i, v, f"{v:g}", ha="center", va="bottom",
                        fontsize=10, fontweight="bold")
        ax.set_xticks(list(xs))
        ax.set_xticklabels([ARM_SHORT[a] for a in arms])
        ax.set_title(ptitle, fontsize=11)
        ax.set_ylabel(ylab)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[fig] {path}")


def fig_paired(df):
    sh12, sh24 = shared_sets(df)
    arms3 = ["A_manual", "C_ai_local", "C_ai_api"]
    a12 = paired_agg(df, sh12, arms3)
    paired_panels(
        os.path.join(FIG_DIR, "fig_paired_12.png"),
        f"Paired on the {len(sh12)} shared tasks (all three arms)",
        arms3,
        [("Tasks solved", {a: a12[a]["solved"] for a in arms3}, "tasks"),
         ("Mean steps / task", {a: a12[a]["steps"] for a in arms3}, "steps"),
         ("Mean redirects / task",
          {a: (float("nan") if a == "A_manual" else a12[a]["interv"]) for a in arms3},
          "per task")],
    )
    arms2 = ["A_manual", "C_ai_api"]
    a24 = paired_agg(df, sh24, arms2)
    paired_panels(
        os.path.join(FIG_DIR, "fig_paired_24.png"),
        f"Human vs AI API on the {len(sh24)} shared tasks",
        arms2,
        [("Tasks solved", {a: a24[a]["solved"] for a in arms2}, "tasks"),
         ("Mean time / task (min)", {a: a24[a]["time"] for a in arms2}, "minutes"),
         ("Mean steps / task", {a: a24[a]["steps"] for a in arms2}, "steps")],
    )
    print("\n=== McNemar (exact, paired on shared targets) ===")
    for lab, ids, a1, a2 in [
        ("C1 vs C2 (12 shared)", sh12, "C_ai_local", "C_ai_api"),
        ("C2 vs Human (12 shared)", sh12, "C_ai_api", "A_manual"),
        ("C2 vs Human (24 shared)", sh24, "C_ai_api", "A_manual"),
    ]:
        b, c = discordant(df, ids, a1, a2)
        print(f"  {lab}: discordant {b} vs {c}, p = {mcnemar_exact(b, c):.2f}")


def fig_difficulty_counts(df):
    """3 'the' (moi nhanh 1 panel): so bai GIAI tren so bai DA LAM, theo do kho."""
    d = df[df["variant"] == "original"]
    arms = ["A_manual", "C_ai_local", "C_ai_api"]
    tiers = ["easy", "medium", "hard"]
    fig, axs = plt.subplots(len(arms), 1, figsize=(7, 5))
    for ax, a in zip(axs, arms):
        da = d[d["arm"] == a]
        tot = [len(da[da["difficulty"] == t]) for t in tiers]
        sol = [int(da[da["difficulty"] == t]["solved"].sum()) for t in tiers]
        tmax = max(tot) if tot else 1
        ys = list(range(len(tiers)))[::-1]
        for yy, t, s, tt in zip(ys, tiers, sol, tot):
            ax.barh(yy, tt, color="#D9DEE2", height=0.6)
            ax.barh(yy, s, color=ARM_COLOR[a], height=0.6)
            ax.text(tmax * 1.02, yy, f"{s}/{tt}", va="center", fontsize=9, fontweight="bold")
            ax.text(-tmax * 0.03, yy, t, va="center", ha="right", fontsize=9)
        ax.set_xlim(0, tmax * 1.15)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_title(f"{ARM_LABEL[a]}   ({int(da['solved'].sum())}/{len(da)})",
                     fontsize=10, loc="left")
        for sp in ("top", "right", "bottom", "left"):
            ax.spines[sp].set_visible(False)
    fig.suptitle("Tasks solved / attempted by difficulty", fontsize=12)
    fig.tight_layout()
    p = os.path.join(FIG_DIR, "fig_difficulty_counts.png")
    fig.savefig(p, dpi=150)
    plt.close(fig)
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

    # Chart so sanh BO cot B_auto (B la tham chieu, trinh bay rieng qua detect-vs-capture).
    summary_chart = summary.drop(index="B_auto", errors="ignore")
    diff_chart = diff.drop(columns="B_auto", errors="ignore")
    bar_solve_rate(summary_chart)
    grouped_by_difficulty(diff_chart)

    # So sanh theo cap tren bai chung (12 & 24) + McNemar + the theo do kho
    print("\n=== BIEU DO SO CAP (paired on shared) ===")
    fig_paired(df)
    fig_difficulty_counts(df)

    # xuat bang ra csv de dua vao bai bao
    summary.to_csv(os.path.join(FIG_DIR, "table_summary.csv"))
    diff.to_csv(os.path.join(FIG_DIR, "table_by_difficulty.csv"))
    print("\nDa xuat bang va bieu do vao paper/figures/")


if __name__ == "__main__":
    main()
