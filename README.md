# MITM Demo

A minimal, hands-on demonstration of a man-in-the-middle (MITM) attack, written
in Python using only the standard library. It runs entirely on your own machine
using local network sockets. Nothing leaves your computer.

The demo has two passes. In the first pass an attacker sits between a customer
and a bank, reads a money transfer, and secretly changes who the money goes to.
In the second pass the customer encrypts the message first, and the same attack
fails. That second pass is what the padlock (HTTPS) in your browser is doing.

## The idea

A man-in-the-middle attack is a dishonest messenger. Two parties talk to each
other through a messenger they both trust. The messenger can secretly read
everything and change it before passing it on, and neither party notices,
because the conversation looks normal to them.

Being in the middle gives the attacker two abilities:

- Read the traffic (eavesdrop).
- Change the traffic (tamper).

## Files

| File | Role |
| --- | --- |
| `bank.py` | The server. Receives a transfer order and confirms it. |
| `mitm.py` | The attacker. Sits between the customer and the bank. |
| `customer.py` | The client. Sends a transfer. Has an ENCRYPT switch. |
| `labcrypto.py` | A tiny shared scrambler used to "encrypt" the message. |

## How the pieces connect

The bank listens on port 9000. The attacker listens on port 8000. The customer
is told to connect to port 8000, believing it is the bank. So every message the
customer sends goes to the attacker first. The attacker reads it, optionally
changes it, forwards it to the real bank on 9000, and passes the bank's reply
back to the customer. From the customer's point of view, nothing looks wrong.

```
customer  --->  attacker (port 8000)  --->  bank (port 9000)
   ^                                            |
   |____________ reply relayed back ____________|
```

## Requirements

- Python 3 (any recent version).
- No third-party packages. No installation needed.
- Keep all four files in the same folder.

## Getting the code

```bash
git clone https://github.com/Maestro-jr/mitm
cd mitm
```

You will need three terminals open in that folder, one for each program.

## Running it

### Pass 1: the attack succeeds (no encryption)

Make sure the top of `customer.py` reads:

```python
ENCRYPT = False
```

Start the three programs in this order, one per terminal:

```bash
python3 bank.py        # terminal 1: start the bank first
python3 mitm.py        # terminal 2: start the attacker
python3 customer.py    # terminal 3: send the transfer
```

Now compare the three terminals:

- The customer sent `TRANSFER 100 TO alice` and got back
  `OK - transfer complete`. To the customer, everything looks fine.
- The attacker printed the transfer in plain text and reported
  `tampering SUCCEEDED`.
- The bank recorded `TRANSFER 100 TO attacker`.

The money went to the attacker, and the customer had no way to tell.

### Pass 2: the attack fails (with encryption)

Change one line at the top of `customer.py`:

```python
ENCRYPT = True
```

Do not change `mitm.py`. The attacker stays exactly the same. Run the customer
again (you can leave the bank and attacker running, or restart all three):

```bash
python3 customer.py
```

Compare the terminals again:

- The attacker now sees a block of scrambled hex instead of readable text, and
  reports `tampering FAILED`.
- The bank records `TRANSFER 100 TO alice`. The correct person was paid.

The attacker did nothing different. The only change is that the customer
scrambled the message before sending it, so the attacker could neither read it
nor find anything to change.

## Why encryption stops the attack

When the message is encrypted, the attacker in the middle sees only scrambled
bytes. They cannot read the transfer, and their find-and-replace has nothing to
match, so tampering does nothing. Only the bank, which shares the secret key,
can turn the scrambled bytes back into a readable order.

This is the core of what HTTPS gives you:

- Confidentiality: someone in the middle cannot read your data.
- Integrity: if they alter the encrypted data, it no longer decrypts correctly,
  so the change is detected.

This is why you should never send passwords or other sensitive data over plain
`http://` or over untrusted Wi-Fi.

## Things to try

1. In Pass 1, change the amount or the recipient in `mitm.py` and watch the bank
   carry out the modified order.
2. In Pass 2, print the raw bytes the attacker receives and confirm the transfer
   is not readable.
3. Change `SECRET_KEY` in `labcrypto.py` on only one side (customer or bank) and
   observe what the bank decodes when the keys do not match.
4. Explain in your own words how a real attacker might get into the middle
   position on a public network.

## Note on the encryption used

`labcrypto.py` uses a simple XOR scrambler so the code stays short and readable.
It is a teaching aid, not real encryption, and must never be used to protect
real data. Real systems, including HTTPS, use vetted modern encryption. The
concept it demonstrates (a shared secret makes the message unreadable to anyone
in the middle) is the real one.

## Scope and responsible use

This project runs against local processes on your own machine only. The
techniques it illustrates are for learning how attacks and defenses work. Do not
attempt to intercept, read, or modify traffic on any network or device you do
not own or have explicit permission to test.
