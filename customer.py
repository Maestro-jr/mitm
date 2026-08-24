# customer.py  — you, the customer. Run this LAST.
import socket
import labcrypto

# ---- Pass 2 switch: flip this to True and run again to see encryption win ----
ENCRYPT = False
# -----------------------------------------------------------------------------

order = "TRANSFER 100 TO alice"

if ENCRYPT:
    envelope = b"encrypted:" + labcrypto.scramble(order.encode())
else:
    envelope = b"plain:" + order.encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 8000))       # you THINK this is the bank (9000) — it's the attacker
    s.sendall(envelope)
    reply = s.recv(1024).decode(errors="replace").strip()

print(f"[YOU]  encryption is {'ON' if ENCRYPT else 'OFF'}")
print(f"[YOU]  you sent:      {order!r}")
print(f"[YOU]  bank replied:  {reply!r}")
