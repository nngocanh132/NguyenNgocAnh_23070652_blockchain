# Lab 03 — Answers

## Lab 3.1

Avalanche: changing one letter ("B" -> "b") gives two completely unrelated hashes:
- `c42dafbb...0b2d78`
- `3b467304...0f40c7`

Toy PoW output (my machine; times vary):

| k | nonce | time |
|---|-------|------|
| 1 | 5 | 0.000s |
| 2 | 61 | 0.000s |
| 3 | 61 | 0.000s |
| 4 | 14229 | 0.010s |
| 5 | 55980 | 0.032s |
| 6 | 24517505 | 18.056s |

**Q1.** Each extra leading hex zero multiplies expected work by about **16x**. A hex digit has 16 values, so
P(one specific digit is 0) = 1/16, so the expected number of tries is 16^k. (Single runs are noisy, e.g. k=2 and k=3
share nonce 61 by luck, but the average grows 16x per step.) If counting leading zero *bits*, each bit is 2x.

**Q2.** Verifying needs **1** hash call: compute sha256(data + nonce) and check the prefix. Finding is
expensive (~16^k) but verifying is O(1), an asymmetry that lets anyone cheaply check that work was done.

## Lab 3.2

`merkle_starter.py` completed, all CHECK lines print OK.

**Q3.** ceil(log2(1,000,000)) = **20** hashes per proof (one sibling per level; the tree has 20 levels).

**Q4.** Bitcoin SPV (light clients): a light wallet downloads only block headers (80 bytes each, containing the
Merkle root). To confirm that a tx is in a block, a full node sends the tx plus its Merkle proof (~log2(n) hashes);
the wallet recomputes upward and compares with the header's root. Same mechanism: Merkle airdrop claims
(a contract stores only the root; the claimer submits a proof) and exchange proof-of-reserves.

## Lab 3.3

The output of `python lab3_3.py` here:

```
address: 0xa5dC012DD7ee3caB2ADED94Adb4Fd7E356fE2070
r,s,v: 0xd242f008459bdde2bca1f799bccc09549fdbb18dedd771e97af5348d8ad244bf 0x3922292565d2839eb7d7bdf01feb936e79d962a8de67d44b1bd40724634eeb56 27
recovered: 0xa5dC012DD7ee3caB2ADED94Adb4Fd7E356fE2070 | match: True
same signature on 2nd sign: True
tampered -> 0x39d2B40637fe0FbEfa872F636AaCF7b43E421243 | differs: True
```

1. **Same message twice, same signature?** Yes, identical. Reason: eth-account uses deterministic ECDSA nonces
   per **RFC 6979** (k is derived from the private key and message hash via HMAC-DRBG instead of being random).
   This also avoids the catastrophic failure of reusing or biasing a random k.
2. **Tampered message** recovers a different (unrelated) address. Public-key recovery is computed from
   (signature, message hash). A one-character change gives a totally different hash (avalanche effect), so
   recovery yields a different public key/address that does not match the signer. Therefore any modification
   of the message is detected, which proves integrity (and authenticity when the address matches).
3. Bonus (optional): in the MetaMask console on a test profile
   `await ethereum.request({method:'personal_sign', params:['0x'+[...new TextEncoder().encode(TEXT)].map(b=>b.toString(16).padStart(2,'0')).join(''), ADDRESS]})`
   then `Account.recover_message(encode_defunct(text=TEXT), signature=SIG)`.
