"""
Build toan bo mau (sample.csv) bang build_target.py, tuan tu (tranh xung dot cong).
Ghi tien do; bai nao loi van tiep tuc. Chay lai an toan (idempotent).

Dung:
    python build_all.py                  # build ban goc, GIU container chay
    python build_all.py --down           # build xong ha container ngay (chi kiem tra dung duoc)
    python build_all.py --variant hintfree --repo ..\\benchmarks\\xbow-hint-free\\benchmarks

Luu y: moi bai co the mat vai phut (mang cham). Chay qua dem cho ca mau.
Sau khi xong, xem targets.csv de biet bai nao 'running' / 'build_failed'.
"""
import argparse, csv, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
SAMPLE = os.path.join(PROJECT, "benchmarks", "sample.csv")
os.environ["PATH"] += os.pathsep + r"C:\Users\Admin\AppData\Local\Programs\DockerDesktop\resources\bin"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="original")
    ap.add_argument("--repo", default=None)
    ap.add_argument("--down", action="store_true")
    ap.add_argument("--prune", action="store_true",
                    help="xoa build cache sau moi bai (GIU dung luong o C on dinh - NEN BAT)")
    ap.add_argument("--only", nargs="*", help="chi build cac id nay")
    args = ap.parse_args()

    with open(SAMPLE, encoding="utf-8") as f:
        ids = [r["benchmark_id"] for r in csv.DictReader(f)]
    if args.only:
        ids = [i for i in ids if i in args.only]

    print(f"Se build {len(ids)} benchmark (variant={args.variant}).")
    ok = fail = 0
    for n, bid in enumerate(ids, 1):
        print(f"\n===== [{n}/{len(ids)}] {bid} =====")
        cmd = [sys.executable, os.path.join(HERE, "build_target.py"), bid, "--variant", args.variant]
        if args.repo:
            cmd += ["--repo", args.repo]
        if args.down:
            cmd.append("--down")
        t0 = time.time()
        r = subprocess.run(cmd)
        dt = time.time() - t0
        if r.returncode == 0:
            ok += 1; print(f"  OK ({dt:.0f}s)")
        else:
            fail += 1; print(f"  FAIL ({dt:.0f}s) - xem targets.csv / patches.log")
        if args.prune:
            # xoa build cache (hog chinh tren o C) - image va container giu nguyen
            subprocess.run(["docker", "builder", "prune", "-af"],
                           capture_output=True, text=True)
    print(f"\n==== XONG: {ok} ok, {fail} fail / {len(ids)} ====")
    print("Xem D:\\Binh\\KLTN new\\project\\benchmarks\\targets.csv")


if __name__ == "__main__":
    main()
