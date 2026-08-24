# bank.py  — the bank. Run this FIRST.
import socket
import labcrypto


def read_order(envelope: bytes) -> str:
    # Messages arrive as  b"plain:<text>"  or  b"encrypted:<scrambled bytes>".
    header, _, body = envelope.partition(b":")
    if header == b"encrypted":
        body = labcrypto.unscramble(body)      # only the bank can do this — it has the key
    return body.decode(errors="replace")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 9000))
    srv.listen(1)
    print("[BANK] open for business on port 9000")
    while True:
        conn, _ = srv.accept()
        with conn:
            order = read_order(conn.recv(1024))
            print(f"[BANK] carried out order: {order!r}")
            conn.sendall(b"OK - transfer complete")
