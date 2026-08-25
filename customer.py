# customer.py  — you, the customer. Run this LAST.
# Interactive: make as many transfers as you like, and choose per transfer
# whether to encrypt. You never have to edit this file to switch encryption.
import socket
import labcrypto

ATTACKER_ADDRESS = ("127.0.0.1", 8000)   # you believe this is the bank; it is really the attacker


def ask_amount() -> str:
    while True:
        value = input("  Amount to send: ").strip()
        if value.isdigit() and int(value) > 0:
            return value
        print("  Please enter a whole number greater than 0.")


def ask_text(prompt: str, allow_empty: bool = False) -> str:
    while True:
        value = input(prompt).strip()
        # Keep the two reserved separators out of typed text so parsing stays simple.
        value = value.replace(" :: ", " ").replace(" TO ", " ")
        if value or allow_empty:
            return value
        print("  This field cannot be empty.")


def ask_yes_no(prompt: str) -> bool:
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("  Please answer y or n.")


def send_transfer(amount: str, receiver: str, note: str, encrypt: bool) -> str:
    body = f"TRANSFER {amount} TO {receiver} :: {note}"
    if encrypt:
        envelope = b"encrypted:" + labcrypto.scramble(body.encode())
    else:
        envelope = b"plain:" + body.encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(ATTACKER_ADDRESS)
        s.sendall(envelope)
        reply = s.recv(1024).decode(errors="replace").strip()
    return reply


def make_transfer() -> None:
    print("\nNew transfer")
    amount = ask_amount()
    receiver = ask_text("  Receiver name: ")
    note = ask_text("  Message to attach (optional): ", allow_empty=True)
    encrypt = ask_yes_no("  Encrypt this message? (y/n): ")

    print(f"\n[YOU]  sending {amount} to {receiver} (encryption {'ON' if encrypt else 'OFF'})")
    try:
        reply = send_transfer(amount, receiver, note, encrypt)
    except ConnectionRefusedError:
        print("[YOU]  could not reach the server. Are bank.py and mitm.py running?")
        return
    print(f"[YOU]  bank replied: {reply!r}")


def main() -> None:
    print("Customer session started.")
    while True:
        print("\nWhat would you like to do?")
        print("  1. Make a transfer")
        print("  2. End session")
        choice = input("Choose 1 or 2: ").strip()
        if choice == "1":
            make_transfer()
        elif choice == "2":
            print("Customer session ended.")
            return
        else:
            print("Please choose 1 or 2.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nCustomer session ended.")
