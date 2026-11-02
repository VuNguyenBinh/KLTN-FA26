"""
NHANH B - pipeline quet TU DONG, KHONG AI (co dinh, tai lap duoc).
Cung mot cau hinh cho MOI bai -> day la "automation without AI" baseline.

Dung:
  1) Bat target:   python build_target.py XBEN-023-24        (lay URL o targets.csv)
  2) Chay nhanh B: python run_arm_B.py XBEN-023-24 --url http://localhost:PORT

Pipeline (co dinh):
  B1. nuclei     -> quet template lo hong/expose/CVE (moi bai)
  B2. ffuf       -> fuzz path bang wordlist common.txt (moi bai)
  B3. exploiter theo loai lo hong (anh xa CO DINH tu metadata tags):
        sqli/blind_sqli/nosqli -> sqlmap --batch --dump
        xss                    -> dalfox
        ssti                   -> SSTImap
        (loai khac: chi dua vao nuclei+ffuf -> thuong KHONG ra flag; day la 1 ket qua)
  => gom log, do khop ground_truth_flag / mau FLAG{...} -> solved Y/N.

KHONG co LLM o bat ky buoc nao.
"""
import argparse, csv, glob, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
TOOLS = os.path.join(HERE, "toolsB")
META = os.path.join(PROJECT, "benchmarks", "metadata.csv")
LOGDIR = os.path.join(PROJECT, "logs")
os.makedirs(LOGDIR, exist_ok=True)

NUCLEI = os.path.join(TOOLS, "nuclei", "nuclei.exe")
DALFOX = glob.glob(os.path.join(TOOLS, "dalfox", "**", "dalfox.exe"), recursive=True)
DALFOX = DALFOX[0] if DALFOX else "dalfox"
SQLMAP = os.path.join(TOOLS, "sqlmap", "sqlmap.py")
SSTIMAP = os.path.join(TOOLS, "SSTImap", "sstimap.py")
WORDLIST = os.path.join(TOOLS, "wordlists", "common.txt")


def find_ffuf():
    p = shutil.which("ffuf")
    if p:
        return p
    g = glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", ""),
                               "Microsoft", "WinGet", "Packages", "ffuf*", "ffuf.exe"))
    return g[0] if g else "ffuf"


FFUF = find_ffuf()


def meta_for(bench):
    with open(META, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["benchmark_id"] == bench:
                return r
    return {}


def run(cmd, logf, timeout):
    logf.write(f"\n\n$ {' '.join(str(c) for c in cmd)}\n")
    logf.flush()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, errors="replace")
        logf.write(p.stdout or "")
        logf.write(p.stderr or "")
        logf.flush()
        return (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired as e:
        msg = f"[TIMEOUT after {timeout}s]\n" + (e.stdout or "" if isinstance(e.stdout, str) else "")
        logf.write(msg); logf.flush()
        return msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("benchmark")
    ap.add_argument("--url", required=True, help="http://localhost:PORT cua target dang chay")
    ap.add_argument("--budget", type=int, default=1800, help="gioi han tong (giay), mac dinh 30 phut")
    args = ap.parse_args()

    m = meta_for(args.benchmark)
    tags = [t.strip() for t in m.get("tags", "").split(",") if t.strip()]
    tagset = set(tags)
    category = tags[0] if tags else ""  # chi de ghi nhan
    gt_flag = m.get("ground_truth_flag", "")
    logpath = os.path.join(LOGDIR, f"B_{args.benchmark}.txt")
    t0 = time.time()
    all_out = ""

    def budget_run(cmd, step_timeout, logf):
        """Chay 1 buoc nhung GIOI HAN boi tong ngan sach con lai (args.budget).
        Neu het gio -> bo qua. Dam bao tong thoi gian khong vuot --budget."""
        remaining = args.budget - (time.time() - t0)
        if remaining <= 5:
            logf.write(f"\n[budget] het ngan sach {args.budget}s -> BO QUA: {os.path.basename(str(cmd[0]))}\n")
            logf.flush()
            return ""
        return run(cmd, logf, int(min(step_timeout, remaining)))

    with open(logpath, "w", encoding="utf-8") as logf:
        logf.write(f"ARM B | {args.benchmark} | cat={category} | url={args.url} | budget={args.budget}s\n")
        logf.write(f"ground_truth_flag={gt_flag}\n")

        # B1 nuclei (moi bai)
        all_out += budget_run([NUCLEI, "-u", args.url, "-rl", "50", "-timeout", "10",
                               "-nc", "-silent"], 600, logf)

        # B2 ffuf fuzz path (moi bai)
        if os.path.isfile(WORDLIST):
            all_out += budget_run([FFUF, "-u", args.url.rstrip("/") + "/FUZZ", "-w", WORDLIST,
                                   "-mc", "200,204,301,302,307,401,403", "-t", "40",
                                   "-s"], 300, logf)

        # B3 exploiter theo loai - QUET TAT CA tag, chay moi bo phu hop (co the nhieu)
        ran_exploiter = False
        if tagset & {"sqli", "blind_sqli", "nosqli"}:
            all_out += budget_run([sys.executable, SQLMAP, "-u", args.url, "--batch",
                                   "--crawl=3", "--forms", "--level=2", "--risk=2",
                                   "--dump-all", "--threads=4"], 900, logf)
            ran_exploiter = True
        if "xss" in tagset:
            all_out += budget_run([DALFOX, "url", args.url, "--no-spinner"], 600, logf)
            ran_exploiter = True
        if "ssti" in tagset:
            all_out += budget_run([sys.executable, SSTIMAP, "-u", args.url, "--crawl", "5",
                                   "-B"], 600, logf)
            ran_exploiter = True
        if not ran_exploiter:
            logf.write(f"\n[info] khong co exploiter no-AI chuyen biet cho tags={tags} "
                       f"-> chi dua vao nuclei+ffuf\n")

        # cham flag
        found = gt_flag and (gt_flag in all_out)
        any_flag = re.search(r"FLAG\{[0-9a-fA-F\-]+\}", all_out)
        dt = round(time.time() - t0, 1)
        solved = 1 if found else 0
        logf.write(f"\n\n===== KET QUA =====\n")
        logf.write(f"solved={solved} time={dt}s flag_found={gt_flag if found else (any_flag.group(0) if any_flag else '')}\n")

    print(f"\n[{args.benchmark}] cat={category} solved={solved} time={dt}s")
    if found:
        print(f"  FLAG khop ground-truth!")
    elif any_flag:
        print(f"  tim thay chuoi FLAG nhung KHAC ground-truth: {any_flag.group(0)}")
    else:
        print(f"  khong tim thay flag (ket qua thuong gap voi nhanh B)")
    print(f"  log: {logpath}")
    print(f"  -> dong results.csv: {args.benchmark},{m.get('difficulty','')},{category},B_auto,original,1,{solved},...,{dt},...")


if __name__ == "__main__":
    main()
