"""
Build + run MOT benchmark XBOW, ap cac ban va tuong thich da kiem chung,
inject flag chuan (SHA256), do port, health-check, ghi vao targets.csv.

Dung:
    python build_target.py XBEN-001-24
    python build_target.py XBEN-001-24 --repo ..\\benchmarks\\xbow-hint-free\\...  (ban hint-free)
    python build_target.py XBEN-001-24 --down     # ha container sau khi xong

Yeu cau: Docker Desktop dang chay. Chay tu thu muc harness/.

Ghi chu khoa hoc: moi ban va deu duoc log vao patches.log de tai lap / khai bao
trong muc "Threats to Validity" cua bai bao. Ban va KHONG thay doi lo hong hay flag,
chi sua tuong thich Docker/Debian theo dung giay phep cua bo benchmark.
"""
import argparse, csv, os, re, subprocess, sys, time, glob

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
DEFAULT_REPO = os.path.join(PROJECT, "benchmarks", "validation-benchmarks", "benchmarks")
META = os.path.join(PROJECT, "benchmarks", "metadata.csv")
TARGETS = os.path.join(PROJECT, "benchmarks", "targets.csv")
PATCHLOG = os.path.join(HERE, "patches.log")

# Docker CLI tren PATH hoac default Docker Desktop
os.environ["PATH"] += os.pathsep + r"C:\Users\Admin\AppData\Local\Programs\DockerDesktop\resources\bin"

MARK = "# [KLTN compat fix]"
APT_VALID = "-o Acquire::Check-Valid-Until=false"


def log_patch(bench, msg):
    with open(PATCHLOG, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{bench}\t{msg}\n")
    print(f"  [patch] {msg}")


def flag_for(bench):
    with open(META, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["benchmark_id"] == bench:
                return r["ground_truth_flag"]
    # fallback: tinh truc tiep
    import hashlib
    return "FLAG{" + hashlib.sha256(bench.upper().encode()).hexdigest() + "}"


def patch_dockerfile(bench, path):
    """Ap ban va tuong thich idempotent cho 1 Dockerfile. Tra ve True neu co sua."""
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    if MARK in txt:
        return False  # da va roi
    orig = txt

    # 1) mysql:5.7.15 -> mysql:5.7
    if re.search(r"FROM\s+mysql:5\.7\.15", txt):
        # comment phai o dong rieng - Dockerfile khong cho comment cung dong voi FROM
        txt = re.sub(r"FROM\s+mysql:5\.7\.15", f"{MARK} bumped from mysql:5.7.15\nFROM mysql:5.7", txt)
        log_patch(bench, f"{os.path.relpath(path, DEFAULT_REPO)}: mysql:5.7.15 -> mysql:5.7")

    # 2) Debian EOL (bat ky base nao chay apt: debian/php/ruby/python-slim...) -> archive mirror
    #    Tu do codename trong image, chi doi sang archive neu la ban EOL. bookworm+ khong dong toi.
    if "apt-get" in txt:
        smart = (
            'RUN if [ -f /etc/os-release ]; then . /etc/os-release; '
            'case "$VERSION_CODENAME" in '
            'jessie|stretch|buster) '
            'echo "deb http://archive.debian.org/debian $VERSION_CODENAME main" > /etc/apt/sources.list; '
            'echo "deb http://archive.debian.org/debian-security $VERSION_CODENAME/updates main" >> /etc/apt/sources.list;; '
            'bullseye) '
            'echo "deb http://archive.debian.org/debian bullseye main" > /etc/apt/sources.list; '
            'echo "deb http://archive.debian.org/debian-security bullseye-security main" >> /etc/apt/sources.list;; '
            'esac; fi'
        )
        inject = f"{MARK} Debian EOL -> archive mirror (auto codename)\n{smart}\n"
        # chen sau dong FROM DAU TIEN
        txt = re.sub(r"(FROM\s+[^\n]*\n)", r"\1" + inject, txt, count=1)
        txt = re.sub(r"apt-get\s+update", f"apt-get {APT_VALID} update", txt)
        log_patch(bench, f"{os.path.relpath(path, DEFAULT_REPO)}: apt -> archive.debian.org (auto)")

    if txt != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(txt)
        return True
    return False


def patch_compose(bench, bench_dir):
    """Sua cu phap cu trong docker-compose.yml (expose 'A:B' -> '\"A\"')."""
    path = os.path.join(bench_dir, "docker-compose.yml")
    if not os.path.isfile(path):
        path = os.path.join(bench_dir, "docker-compose.yaml")
        if not os.path.isfile(path):
            return
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    changed = False
    in_expose = False
    in_ports = False
    for i, ln in enumerate(lines):
        # pin mongo:latest -> mongo:4.4 (mongo moi lech wire version voi driver cu cua app)
        mm = re.match(r"(\s*image\s*:\s*)mongo:latest\s*$", ln)
        if mm:
            lines[i] = f"{mm.group(1)}mongo:4.4  # {MARK}\n"
            changed = True
            log_patch(bench, "docker-compose.yml: mongo:latest -> mongo:4.4")
            continue
        stripped = ln.strip()
        if re.match(r"expose\s*:", stripped):
            in_expose = True; in_ports = False
            continue
        if re.match(r"ports\s*:", stripped):
            in_ports = True; in_expose = False
            continue
        if in_expose:
            m = re.match(r"(\s*-\s*)\"?(\d+):\d+\"?\s*$", ln)
            if m:
                lines[i] = f'{m.group(1)}"{m.group(2)}"\n'
                changed = True
                log_patch(bench, f"docker-compose.yml: expose '{stripped}' -> \"{m.group(2)}\"")
            elif not re.match(r"\s*-\s", ln):
                in_expose = False
        if in_ports:
            # cong co dinh HOST:CONTAINER -> chi giu CONTAINER (cong host ngau nhien, tranh xung dot)
            m = re.match(r"(\s*-\s*)\"?(\d+):(\d+)\"?\s*$", ln)
            if m:
                lines[i] = f'{m.group(1)}"{m.group(3)}"\n'
                changed = True
                log_patch(bench, f"docker-compose.yml: ports '{stripped}' -> random host (\"{m.group(3)}\")")
            elif not re.match(r"\s*-\s", ln):
                in_ports = False
    # neu da pin mongo:4.4 -> healthcheck 'mongosh' (chi co o mongo 5+) phai doi ve 'mongo'
    if any("mongo:4.4" in l for l in lines):
        for i, ln in enumerate(lines):
            if "mongosh" in ln:
                lines[i] = ln.replace("mongosh", "mongo")
                changed = True
                log_patch(bench, "docker-compose.yml: healthcheck mongosh -> mongo (mongo:4.4)")

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)


def normalize_sh(bench, bench_dir):
    """CRLF -> LF cho script shell (.sh/.bash) + entrypoint khong duoi .sh.
    git autocrlf=true tren Windows lam shebang '#!/bin/bash\\r' hong -> container exit 255."""
    patterns = ["**/*.sh", "**/*.bash", "**/entrypoint*", "**/*entrypoint*"]
    seen = set()
    for pat in patterns:
        for f in glob.glob(os.path.join(bench_dir, pat), recursive=True):
            if not os.path.isfile(f) or f in seen:
                continue
            seen.add(f)
            with open(f, "rb") as fh:
                data = fh.read()
            if b"\r\n" in data:
                with open(f, "wb") as fh:
                    fh.write(data.replace(b"\r\n", b"\n"))
                log_patch(bench, f"{os.path.relpath(f, DEFAULT_REPO)}: CRLF -> LF")


def apply_fixes(bench, bench_dir):
    for df in glob.glob(os.path.join(bench_dir, "**", "Dockerfile"), recursive=True):
        patch_dockerfile(bench, df)
    patch_compose(bench, bench_dir)
    normalize_sh(bench, bench_dir)


def run(cmd, cwd, timeout=1800):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


DB_PORTS = {3306, 5432, 6379, 27017, 1433, 11211}


def detect_url(bench_dir):
    """Tra ve http://localhost:<host_port> cua service web (bo cong DB, uu tien cong HTTP phan hoi)."""
    import json as _json
    import urllib.request
    r = run(["docker", "compose", "ps", "--format", "json"], bench_dir, 120)
    candidates = []  # (svc, published_port, target_port)
    for line in r.stdout.splitlines():
        line = line.strip().lstrip("﻿")
        if not line:
            continue
        try:
            d = _json.loads(line)
        except Exception:
            continue
        svc = d.get("Service")
        for pub in (d.get("Publishers") or []):
            pp, tp = pub.get("PublishedPort"), pub.get("TargetPort")
            if pp and tp not in DB_PORTS:
                candidates.append((svc, pp, tp))
    # bo trung, uu tien cong khong phai DB
    seen = set()
    uniq = []
    for c in candidates:
        if c[1] not in seen:
            seen.add(c[1]); uniq.append(c)
    # HTTP-probe de chon cong web thuc su
    for svc, pp, tp in uniq:
        url = f"http://localhost:{pp}"
        try:
            urllib.request.urlopen(url, timeout=8)
            return url, svc
        except urllib.error.HTTPError:
            return url, svc  # co phan hoi HTTP (401/403...) van la web
        except Exception:
            continue
    # fallback: cong non-DB dau tien du khong probe duoc
    if uniq:
        return f"http://localhost:{uniq[0][1]}", uniq[0][0]
    return None, None


def write_target(bench, status, url, flag, variant):
    header = ["benchmark_id", "variant", "status", "url", "ground_truth_flag"]
    rows = []
    if os.path.isfile(TARGETS):
        with open(TARGETS, encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if not (r["benchmark_id"] == bench and r["variant"] == variant)]
    rows.append({"benchmark_id": bench, "variant": variant, "status": status, "url": url or "", "ground_truth_flag": flag})
    with open(TARGETS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("benchmark")
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("--variant", default="original", help="original | hintfree")
    ap.add_argument("--down", action="store_true", help="ha container sau khi health-check")
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args()

    bench_dir = os.path.join(args.repo, args.benchmark)
    if not os.path.isdir(bench_dir):
        print(f"KHONG tim thay {bench_dir}"); sys.exit(2)

    flag = flag_for(args.benchmark)
    print(f"[{args.benchmark}] variant={args.variant} flag={flag[:20]}...")

    print("Ap ban va tuong thich...")
    apply_fixes(args.benchmark, bench_dir)

    print("Building...")
    build = ["docker", "compose", "build", "--build-arg", f"FLAG={flag}", "--build-arg", f"flag={flag}"]
    if args.no_cache:
        build.append("--no-cache")
    b = run(build, bench_dir, 2400)
    if b.returncode != 0:
        tail = (b.stderr or b.stdout)[-600:]
        print("BUILD FAILED:\n", tail)
        write_target(args.benchmark, "build_failed", None, flag, args.variant)
        sys.exit(1)

    print("Starting...")
    # KHONG dung --wait: nhieu benchmark cu cau hinh healthcheck sai (mongosh, haproxy,
    # Flask debug) -> bao unhealthy du web van phuc vu. Ta tin HTTP-probe that su.
    u = run(["docker", "compose", "up", "-d"], bench_dir, 600)
    if u.returncode != 0:
        print("UP FAILED:\n", (u.stderr or u.stdout)[-600:])
        write_target(args.benchmark, "up_failed", None, flag, args.variant)
        sys.exit(1)

    import urllib.request, urllib.error
    url, svc, status = None, None, "up_failed"
    deadline = time.time() + 120
    while time.time() < deadline:
        url, svc = detect_url(bench_dir)
        if url:
            try:
                code = urllib.request.urlopen(url, timeout=8).getcode()
                print(f"  web OK: {url} (svc={svc}, HTTP {code})")
                status = "running"; break
            except urllib.error.HTTPError as e:
                print(f"  web OK: {url} (svc={svc}, HTTP {e.code})")
                status = "running"; break
            except Exception:
                pass
        time.sleep(5)

    if status != "running":
        print(f"  khong co web port phan hoi HTTP sau 120s (url cuoi={url})")
        write_target(args.benchmark, "up_failed", url, flag, args.variant)
        if args.down:
            run(["docker", "compose", "down"], bench_dir, 300)
        sys.exit(1)

    write_target(args.benchmark, status, url, flag, args.variant)
    print(f"  -> ghi targets.csv: {status} {url}")

    if args.down:
        run(["docker", "compose", "down"], bench_dir, 300)
        print("  da ha container.")


if __name__ == "__main__":
    main()
