# MITM Demo

A minimal, hands-on demonstration of a man-in-the-middle (MITM) attack, written
in Python using only the standard library. It runs entirely on your own machine
using local network sockets. Nothing leaves your computer.

An attacker sits between a customer and a bank. When the customer sends a money
transfer without encryption, the attacker reads it and secretly changes who the
money goes to. When the customer encrypts the transfer, the same attack fails.
That is what the padlock (HTTPS) in your browser is doing.

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
| `bank.py` | The server. Receives a transfer and records the amount, receiver, and note. |
| `mitm.py` | The attacker. Sits between the customer and the bank and tries to read and change every message. |
| `customer.py` | The client. An interactive menu to make transfers and choose whether to encrypt. |
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
git clone <repository-url>
cd <repository-folder>
```

You will need three terminals open in that folder, one for each program.

## Running it

Start the three programs in this order, one per terminal:

```bash
python3 bank.py        # terminal 1: start the bank first
python3 mitm.py        # terminal 2: start the attacker
python3 customer.py    # terminal 3: the interactive customer
```

The customer shows a menu:

```
  1. Make a transfer
  2. End session
```

Choose `1` to make a transfer. You will be asked for four things:

- the amount,
- the receiver name,
- a message to attach (optional),
- whether to encrypt the message (y/n).

After the transfer, the menu appears again so you can make another one. Choose
`2` to end the customer program. The bank and the attacker keep running; stop
them with Ctrl-C when you are done.

You do not edit any code to switch encryption on or off. You choose it at the
prompt each time.

### What to observe

Make one transfer with encryption OFF, then make the same transfer with
encryption ON, and compare the three terminals.

With encryption OFF:

- The attacker prints your transfer in plain text and reports
  `Tampering SUCCEEDED`.
- The bank records the money going to `attacker`, not the person you chose.
- Your own terminal shows a normal confirmation, so as the customer you cannot
  tell anything went wrong.

With encryption ON:

- The attacker sees only scrambled hex and reports `Tampering FAILED`.
- The bank records the money going to the receiver you actually chose.

The attacker code is identical in both cases. The only thing that changed is that
the customer encrypted the message.

## Why encryption stops the attack

When the message is encrypted, the attacker in the middle sees only scrambled
bytes. It cannot read the transfer, and it has nothing to match when it tries to
change the receiver, so tampering does nothing. Only the bank, which shares the
secret key, can turn the scrambled bytes back into a readable order.

This is the core of what HTTPS gives you:

- Confidentiality: someone in the middle cannot read your data.
- Integrity: if they alter the encrypted data, it no longer decrypts correctly,
  so the change is detected.

This is why you should never send passwords or other sensitive data over plain
`http://` or over untrusted Wi-Fi.

## Things to try

1. Send the same transfer with encryption off and then on, and compare what the
   bank records each time.
2. Read the attacker's output during an unencrypted transfer and notice that it
   also sees the note you attached, not just the amount and receiver.
3. In `mitm.py`, change the amount as well as the receiver, and watch the bank
   carry out the fully rewritten order.
4. Change `SECRET_KEY` in `labcrypto.py` on only one side and observe what the
   bank decodes when the keys do not match.
5. Explain in your own words how a real attacker might get into the middle
   position on a public network.

## Note on the encryption used

`labcrypto.py` uses a simple XOR scrambler so the code stays short and readable.
It is a teaching aid, not real encryption, and must never be used to protect real
data. Real systems, including HTTPS, use vetted modern encryption. The concept it
demonstrates (a shared secret makes the message unreadable to anyone in the
middle) is the real one.

## Scope and responsible use

This project runs against local processes on your own machine only. The
techniques it illustrates are for learning how attacks and defenses work. Do not
attempt to intercept, read, or modify traffic on any network or device you do not
own or have explicit permission to test.
