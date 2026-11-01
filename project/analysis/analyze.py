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
    # chuan hoa cot boolean
    for col in ["solved", "llm_refused"]:
        if col in df.columns:
            df[col] = (
                df[col].astype(str).str.strip().str.lower()
                .map({"1": 1, "y": 1, "yes": 1, "true": 1,
                      "0": 0, "n": 0, "no": 0, "false": 0, "": 0})
                .fillna(0).astype(int)
            )
    for col in ["time_minutes", "num_steps", "tokens_used", "manual_interventions"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # chi giu cac dong da chay (co ghi solved)
    return df[df["solved"].notna()]


def summary_table(df):
    g = df.groupby("arm")
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
    t = (df.groupby(["difficulty", "arm"])["solved"].mean() * 100).round(1).unstack("arm")
    cols = [a for a in ARM_ORDER if a in t.columns]
    return t[cols]


def solve_rate_by_category(df):
    t = (df.groupby(["vuln_category", "arm"])["solved"].mean() * 100).round(1).unstack("arm")
    cols = [a for a in ARM_ORDER if a in t.columns]
    return t[cols]


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


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <results.csv>")
        sys.exit(1)
    df = load(sys.argv[1])
    if df.empty:
        print("Chua co du lieu (chua ghi cot 'solved').")
        return

    print("\n=== BANG 1: Tong hop theo nhanh ===")
    summary = summary_table(df)
    print(summary.to_string())

    print("\n=== BANG 2: Solve rate theo do kho (%) ===")
    diff = solve_rate_by_difficulty(df)
    print(diff.to_string())

    print("\n=== BANG 3: Solve rate theo loai lo hong (%) ===")
    print(solve_rate_by_category(df).to_string())

    bar_solve_rate(summary)
    grouped_by_difficulty(diff)

    # xuat bang ra csv de dua vao bai bao
    summary.to_csv(os.path.join(FIG_DIR, "table_summary.csv"))
    diff.to_csv(os.path.join(FIG_DIR, "table_by_difficulty.csv"))
    print("\nDa xuat bang va bieu do vao paper/figures/")


if __name__ == "__main__":
    main()
