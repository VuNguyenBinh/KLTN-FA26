"""
Backend demo nhánh C2 — chạy bằng thư viện chuẩn (KHONG cần cài gì thêm).

Chạy:   python demo/server.py        (hoặc trong thư mục demo: python server.py)
Mở:     http://127.0.0.1:8765

Chức năng:
  GET  /api/tasks           -> danh sách bài (mặc định sample 40; ?all=1 -> 104)
  POST /api/build           -> dựng target qua build_target.py (chạy nền), trả job
  GET  /api/build_status    -> trạng thái + log build, url, flag khi xong
  POST /api/down            -> hạ container của bài

Yêu cầu khi dùng thật: Docker Desktop đang chạy; benchmark repo đã có (như build_target.py).
Backend chỉ gọi lại build_target.py của nhóm, KHÔNG làm gì ngoài harness.
"""
import json, csv, os, re, sys, threading, subprocess, hashlib, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
HARNESS = os.path.join(PROJECT, "project", "harness")
BENCH = os.path.join(PROJECT, "project", "benchmarks")
META = os.path.join(BENCH, "metadata.csv")
SAMPLE = os.path.join(BENCH, "sample.csv")
TARGETS = os.path.join(BENCH, "targets.csv")
PORT = 8765
DOCKER_BIN = r"C:\Users\Admin\AppData\Local\Programs\DockerDesktop\resources\bin"

def docker_env():
    env = dict(os.environ)
    env["PATH"] += os.pathsep + DOCKER_BIN
    return env

def docker_ok():
    """True nếu Docker daemon (Linux engine) đang chạy."""
    try:
        r = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=25, env=docker_env())
        return r.returncode == 0, (r.stderr or r.stdout)[-300:]
    except Exception as e:
        return False, str(e)

# id hợp lệ (chống chèn lệnh): chỉ cho id có trong metadata
def valid_ids():
    ids = set()
    if os.path.isfile(META):
        for r in csv.DictReader(open(META, encoding="utf-8")):
            ids.add(r["benchmark_id"])
    return ids
ALLOWED = valid_ids()

def load_tasks(all_tasks=False):
    path = META if all_tasks else SAMPLE
    out = []
    if os.path.isfile(path):
        for r in csv.DictReader(open(path, encoding="utf-8")):
            out.append({
                "id": r["benchmark_id"],
                "difficulty": r.get("difficulty", ""),
                "vuln": (r.get("tags", "") or "").split(",")[0].strip(),
                "tags": r.get("tags", ""),
                "name": r.get("name", ""),
            })
    return out

def read_target_row(bench, variant):
    if not os.path.isfile(TARGETS):
        return None
    for r in csv.DictReader(open(TARGETS, encoding="utf-8")):
        if r["benchmark_id"] == bench and r.get("variant", "original") == variant:
            return r
    return None

def expected_flag(bench):
    return "FLAG{" + hashlib.sha256(bench.upper().encode()).hexdigest() + "}"

# ---- build jobs (chạy nền) ----
JOBS = {}  # key = f"{id}|{variant}" -> {state, log[], url, flag, status, started}
LOCK = threading.Lock()

def build_worker(bench, variant):
    key = f"{bench}|{variant}"
    def put(**kw):
        with LOCK:
            JOBS[key].update(kw)
    def log(line):
        with LOCK:
            JOBS[key]["log"].append(line.rstrip("\n"))
            JOBS[key]["log"] = JOBS[key]["log"][-200:]
    ok, dmsg = docker_ok()
    if not ok:
        log("[Docker] Daemon KHÔNG phản hồi — hãy mở Docker Desktop và chờ 'Engine running',")
        log("[Docker] và chắc chắn đang ở chế độ Linux containers (không phải Windows containers).")
        log(dmsg)
        put(state="error", status="docker_down", flag=expected_flag(bench))
        return
    cmd = [sys.executable, "build_target.py", bench, "--variant", variant]
    if variant == "hintfree":
        # bản hint-free nằm ở repo riêng (đã gỡ gợi ý) — KHÔNG dùng repo gốc
        cmd += ["--repo", os.path.join(BENCH, "xbow-hint-free", "benchmarks")]
    log(f"$ {' '.join(cmd)}  (cwd={HARNESS})")
    try:
        p = subprocess.Popen(cmd, cwd=HARNESS, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in p.stdout:
            log(line)
        p.wait()
        row = read_target_row(bench, variant)
        if row and row.get("status") == "running" and row.get("url"):
            put(state="done", status="running", url=row["url"], flag=row.get("ground_truth_flag") or expected_flag(bench))
            log(f"[OK] target chạy tại {row['url']}")
        else:
            st = (row or {}).get("status", "unknown")
            put(state="error", status=st, url=(row or {}).get("url", ""), flag=expected_flag(bench))
            log(f"[LỖI] build không ra web port (status={st}). Kiểm tra Docker Desktop.")
    except Exception as e:
        put(state="error", status="exception")
        log(f"[EXCEPTION] {e}")

def start_build(bench, variant):
    key = f"{bench}|{variant}"
    with LOCK:
        cur = JOBS.get(key)
        if cur and cur["state"] == "building":
            return False
        JOBS[key] = {"state": "building", "log": [], "url": "", "flag": expected_flag(bench),
                     "status": "building", "started": time.time()}
    threading.Thread(target=build_worker, args=(bench, variant), daemon=True).start()
    return True

def docker_down(bench, variant):
    project = f"{bench.lower()}-{variant}"
    repo = "xbow-hint-free" if variant == "hintfree" else "validation-benchmarks"
    bench_dir = os.path.join(BENCH, repo, "benchmarks", bench)
    try:
        r = subprocess.run(["docker", "compose", "-p", project, "down"], cwd=bench_dir,
                           capture_output=True, text=True, timeout=300, env=docker_env())
        return r.returncode == 0, (r.stderr or r.stdout)[-400:]
    except Exception as e:
        return False, str(e)

# ---- HTTP ----
class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    def log_message(self, *a):
        pass  # im lặng

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ("/", "/index.html", "/app.html"):
            p = os.path.join(HERE, "app.html")
            if os.path.isfile(p):
                self._send(200, open(p, "rb").read(), "text/html; charset=utf-8")
            else:
                self._send(404, "app.html not found", "text/plain; charset=utf-8")
            return
        if u.path == "/api/tasks":
            q = parse_qs(u.query)
            self._json(200, {"tasks": load_tasks(all_tasks=q.get("all", ["0"])[0] == "1"),
                             "pgdir": os.path.join(HARNESS, "PentestGPT")})
            return
        if u.path == "/api/build_status":
            q = parse_qs(u.query)
            bench = q.get("id", [""])[0]; variant = q.get("variant", ["original"])[0]
            with LOCK:
                job = JOBS.get(f"{bench}|{variant}")
                self._json(200, job or {"state": "none", "log": []})
            return
        self._json(404, {"error": "not found"})

    def do_POST(self):
        u = urlparse(self.path)
        n = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            body = {}
        bench = (body.get("id") or "").strip()
        variant = (body.get("variant") or "original").strip()
        if variant not in ("original", "hintfree"):
            variant = "original"
        if bench not in ALLOWED:
            self._json(400, {"error": f"benchmark_id không hợp lệ: {bench}"})
            return
        if u.path == "/api/build":
            started = start_build(bench, variant)
            self._json(200, {"ok": True, "started": started, "key": f"{bench}|{variant}"})
            return
        if u.path == "/api/down":
            ok, msg = docker_down(bench, variant)
            self._json(200, {"ok": ok, "msg": msg})
            return
        self._json(404, {"error": "not found"})

def main():
    if not os.path.isfile(os.path.join(HARNESS, "build_target.py")):
        print("CẢNH BÁO: không thấy build_target.py ở", HARNESS)
    print(f"Demo C2 console: http://127.0.0.1:{PORT}  (Ctrl+C để dừng)")
    print(f"  harness = {HARNESS}")
    print(f"  tasks   = {len(load_tasks())} bài (sample) / {len(ALLOWED)} bài (metadata)")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()

if __name__ == "__main__":
    main()
