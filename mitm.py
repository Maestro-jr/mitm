# mitm.py  — the man in the middle. Run this SECOND.
# IMPORTANT: you do NOT change this file for Pass 2. The attacker does nothing
# different — encryption alone is what defeats it.
import socket


def show(raw: bytes) -> str:
    if all(32 <= b <= 126 for b in raw):     # every byte is normal printable text
        return raw.decode()
    return raw.hex()                          # otherwise it's scrambled — show the raw hex


def tamper(raw: bytes) -> bytes:
    changed = raw.replace(b"alice", b"attacker")     # try to redirect the money to us
    if changed != raw:
        print("[MITM] tampering SUCCEEDED — I rewrote the order")
    else:
        print("[MITM] tampering FAILED — I couldn't find 'alice' to change")
    return changed


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 8000))       # the customer connects HERE, thinking it's the bank
    listener.listen(1)
    print("[MITM] sitting in the middle, listening on port 8000")
    while True:
        customer, _ = listener.accept()
        with customer:
            raw = customer.recv(1024)
            print(f"[MITM] I intercepted: {show(raw)!r}")
            forwarded = tamper(raw)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as to_bank:
                to_bank.connect(("127.0.0.1", 9000))   # pass it on to the REAL bank
                to_bank.sendall(forwarded)
                reply = to_bank.recv(1024)
            customer.sendall(reply)          # relay a normal-looking reply back to the customer
