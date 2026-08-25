# bank.py  — the bank. Run this FIRST.
import socket
import labcrypto

LISTEN_ADDRESS = ("127.0.0.1", 9000)


def read_body(envelope: bytes) -> str:
    # Messages arrive as  b"plain:<text>"  or  b"encrypted:<scrambled>".
    header, _, body = envelope.partition(b":")
    if header == b"encrypted":
        body = labcrypto.unscramble(body)     # only the bank can do this; it has the key
    return body.decode(errors="replace")


def parse_transfer(text: str) -> dict:
    # text looks like: "TRANSFER 100 TO alice :: note"
    note = ""
    if " :: " in text:
        text, note = text.split(" :: ", 1)
    amount, receiver = "?", "?"
    if " TO " in text:
        left, receiver = text.split(" TO ", 1)
        receiver = receiver.strip()
        parts = left.split()
        if len(parts) >= 2:
            amount = parts[1]
    return {"amount": amount, "receiver": receiver, "note": note}


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(LISTEN_ADDRESS)
    srv.listen(1)
    print("[BANK] open for business on port 9000")
    while True:
        conn, _ = srv.accept()
        with conn:
            order = parse_transfer(read_body(conn.recv(1024)))
            print("\n" + "-" * 50)
            print("[BANK] transfer carried out:")
            print(f"       amount:   {order['amount']}")
            print(f"       to:       {order['receiver']}")
            print(f"       note:     {order['note']!r}")
            conn.sendall(b"OK - transfer complete")
