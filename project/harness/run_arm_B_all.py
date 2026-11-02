"""
Chay NHANH B (tu dong, khong AI) cho CA mau 40 bai, ghi thang vao results.csv.
Voi moi bai: bat target -> chay pipeline nhanh B -> ghi ket qua -> ha target.

Dung:
    python run_arm_B_all.py                 # ca 40 bai, ban goc
    python run_arm_B_all.py --only XBEN-006-24 XBEN-083-24
    python run_arm_B_all.py --budget 900    # gioi han 15 phut/bai

Chay nen vi lau (moi bai vai phut). Ket qua -> project/results/results.csv.
Nhanh B chi chay ban goc (scanner khong doc goi y nhu LLM).
"""
import argparse, csv, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
SAMPLE = os.path.join(PROJECT, "benchmarks", "sample.csv")
TARGETS = os.path.join(PROJECT, "benchmarks", "targets.csv")
RESULTS = os.path.join(PROJECT, "results", "results.csv")
REPO = os.path.join(PROJECT, "benchmarks", "validation-benchmarks", "benchmarks")
os.environ["PATH"] += os.pathsep + r"C:\Users\Admin\AppData\Local\Programs\DockerDesktop\resources\bin"


def url_for(bench):
    if not os.path.isfile(TARGETS):
        return None
    with open(TARGETS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["benchmark_id"] == bench and r["variant"] == "original":
                return r["url"] or None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--budget", type=int, default=1800)
    args = ap.parse_args()

    with open(SAMPLE, encoding="utf-8") as f:
        ids = [r["benchmark_id"] for r in csv.DictReader(f)]
    if args.only:
        ids = [i for i in ids if i in args.only]

    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    print(f"NHANH B cho {len(ids)} bai -> {RESULTS}\n")

    for n, bid in enumerate(ids, 1):
        print(f"===== [{n}/{len(ids)}] {bid} =====")
        bench_dir = os.path.join(REPO, bid)
        project = f"{bid.lower()}-original"
        # 1) bat target (khong --down)
        up = subprocess.run([sys.executable, os.path.join(HERE, "build_target.py"), bid],
                            capture_output=True, text=True)
        if up.returncode != 0:
            print(f"  bat target LOI -> bo qua\n{up.stdout[-300:]}")
            continue
        url = url_for(bid)
        if not url:
            print("  khong lay duoc URL -> bo qua")
            subprocess.run(["docker", "compose", "-p", project, "down"], cwd=bench_dir,
                           capture_output=True, text=True)
            continue
        # 2) chay pipeline nhanh B
        t0 = time.time()
        subprocess.run([sys.executable, os.path.join(HERE, "run_arm_B.py"), bid,
                        "--url", url, "--budget", str(args.budget),
                        "--out-csv", RESULTS])
        print(f"  xong trong {time.time()-t0:.0f}s")
        # 3) ha target
        subprocess.run(["docker", "compose", "-p", project, "down"], cwd=bench_dir,
                       capture_output=True, text=True)

    print(f"\n==== NHANH B XONG. Ket qua: {RESULTS} ====")
    print("Chay phan tich: cd ../analysis && python analyze.py ../results/results.csv")


if __name__ == "__main__":
    main()
