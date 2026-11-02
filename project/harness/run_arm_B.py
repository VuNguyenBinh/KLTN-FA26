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
    ap.add_argument("--variant", default="original", help="original | hintfree (nhan B thuong chi original)")
    ap.add_argument("--out-csv", default=None, help="ghi 1 dong ket qua vao results.csv")
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

    # QUAN TRONG: nuclei coi 'localhost' la unresponsive (loi phan giai) -> dung 127.0.0.1
    # cho MOI cong cu de chung thuc su quet.
    target = args.url.replace("localhost", "127.0.0.1")

    with open(logpath, "w", encoding="utf-8") as logf:
        logf.write(f"ARM B | {args.benchmark} | cat={category} | url={target} | budget={args.budget}s\n")
        logf.write(f"ground_truth_flag={gt_flag}\n")

        # B1 nuclei (moi bai) - app custom hiem khi dinh CVE -> gioi han 120s, tat interactsh (-ni)
        all_out += budget_run([NUCLEI, "-u", target, "-rl", "150", "-timeout", "6",
                               "-ni", "-nc"], 120, logf)

        # B2 ffuf fuzz path (moi bai) -> thu thap path de nap cho exploiter
        ffuf_out = ""
        if os.path.isfile(WORDLIST):
            ffuf_out = budget_run([FFUF, "-u", target.rstrip("/") + "/FUZZ", "-w", WORDLIST,
                                   "-mc", "200,204,301,302,307,401,403", "-t", "40",
                                   "-s"], 300, logf)
            all_out += ffuf_out
        paths = [p.strip() for p in ffuf_out.splitlines() if p.strip() and not p.startswith("[")]
        cand = [target] + [target.rstrip("/") + "/" + p.lstrip("/") for p in paths[:15]]

        # B3 exploiter theo loai - QUET TAT CA tag, chay moi bo phu hop
        ran_exploiter = False
        if tagset & {"sqli", "blind_sqli", "nosqli"}:
            all_out += budget_run([sys.executable, SQLMAP, "-u", target, "--batch",
                                   "--crawl=3", "--forms", "--level=3", "--risk=2",
                                   "--dump-all", "--threads=4"], 900, logf)
            ran_exploiter = True
        if "xss" in tagset:
            # dalfox tren base + cac path ffuf tim duoc (no tu dao tham so moi URL)
            all_out += budget_run([DALFOX, "url"] + cand + ["-S"], 600, logf)
            ran_exploiter = True
        if "ssti" in tagset:
            # SUA LOI: cu '-B' (bind-shell) doi 1 doi so -> SSTImap crash ngay,
            # chua he test SSTI. Bo '-B', chi crawl + do tham so de phat hien.
            all_out += budget_run([sys.executable, SSTIMAP, "-u", target,
                                   "--crawl", "5"], 600, logf)
            ran_exploiter = True
        if not ran_exploiter:
            logf.write(f"\n[info] khong co exploiter no-AI chuyen biet cho tags={tags} "
                       f"-> chi dua vao nuclei+ffuf\n")

        # cham flag (bat duoc flag = win condition cua benchmark)
        found = gt_flag and (gt_flag in all_out)
        any_flag = re.search(r"FLAG\{[0-9a-fA-F\-]+\}", all_out)
        dt = round(time.time() - t0, 1)
        solved = 1 if found else 0

        # cham PHAT HIEN lo hong (khac voi bat flag) -- DINH NGHIA CHAT (da sua 2 loi do).
        # Loi cu lam THOI PHONG detection (22/40=55%):
        #   (1) chuoi con "ssti" khop ten tool "SSTImap" trong banner/loi -> 6 SSTI gia.
        #   (2) nuclei gan co generic (PHP version EOL, memory-exhaustion...) bi tinh la
        #       "phat hien lo hong" -> ~4 ca gia o cac bai nuclei+ffuf only.
        # Nay chi tinh detected khi 1 trong cac tin hieu DUNG LOP xuat hien:
        #   - dalfox xac nhan XSS: [POC]
        #   - sqlmap xac nhan SQLi: "is vulnerable"/"injectable"/"back-end DBMS is"
        #   - SSTImap xac nhan SSTI: "injection point"/"Engine:"/"is exploitable"/
        #     "identified the following injection"
        #   - nuclei high/critical NHUNG KHONG phai template generic (version/eol/tech/...)
        NUCLEI_GENERIC = re.compile(
            r"version|eol|tech[-_ ]?detect|panel|exposure|deprecat|memory-exhaustion|"
            r"default.?page|missing|outdated|self-signed|\btls\b|\bssl\b|waf-detect|robots",
            re.I)
        dalfox_hit = "[POC]" in all_out
        # SUA LOI (lan 2): token tran 'injectable' khop ca "not injectable"
        # (SSTImap in "Tested parameters appear to be not injectable") -> 6 SSTI gia.
        # Chi giu tin hieu DUONG ro rang cua sqlmap.
        sqlmap_hit = bool(re.search(
            r"is vulnerable|back-end DBMS is|the following injection point",
            all_out, re.I))
        sstimap_hit = bool(re.search(
            r"injection point|\bEngine:|is exploitable|identified the following injection",
            all_out, re.I))
        nuclei_hit = any(
            re.search(r"\[(high|critical)\]", ln) and "http" in ln.lower()
            and not NUCLEI_GENERIC.search(ln)
            for ln in all_out.splitlines())
        detected = 1 if (dalfox_hit or sqlmap_hit or sstimap_hit or nuclei_hit) else 0

        logf.write(f"\n\n===== KET QUA =====\n")
        logf.write(f"solved={solved} detected={detected} time={dt}s "
                   f"flag_found={gt_flag if found else (any_flag.group(0) if any_flag else '')}\n")

    print(f"\n[{args.benchmark}] cat={category} solved={solved} detected={detected} time={dt}s")
    if found:
        print(f"  FLAG khop ground-truth!")
    elif detected:
        print(f"  PHAT HIEN lo hong nhung KHONG bat duoc flag (can khai thac nhieu buoc)")
    else:
        print(f"  khong phat hien / khong bat flag")
    print(f"  log: {logpath}")

    if args.out_csv:
        header = ["benchmark_id", "difficulty", "vuln_category", "arm", "variant",
                  "run_id", "solved", "flag_found", "time_minutes", "num_steps",
                  "tokens_used", "manual_interventions", "llm_refused", "notes"]
        row = {
            "benchmark_id": args.benchmark, "difficulty": m.get("difficulty", ""),
            "vuln_category": category, "arm": "B_auto", "variant": args.variant,
            "run_id": "1", "solved": solved,
            "flag_found": (gt_flag if found else ""),
            "time_minutes": round(dt / 60, 2), "num_steps": "", "tokens_used": "",
            "manual_interventions": "", "llm_refused": "",
            "notes": f"no-AI; detected={'yes' if detected else 'no'}; "
                     f"exploiter={'yes' if ran_exploiter else 'nuclei+ffuf only'}",
        }
        existing = []
        if os.path.isfile(args.out_csv):
            with open(args.out_csv, encoding="utf-8") as f:
                existing = [r for r in csv.DictReader(f)
                            if not (r["benchmark_id"] == args.benchmark
                                    and r["arm"] == "B_auto" and r["variant"] == args.variant)]
        with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=header)
            w.writeheader()
            w.writerows(existing)
            w.writerow(row)
        print(f"  -> da ghi results.csv ({args.out_csv})")


if __name__ == "__main__":
    main()
