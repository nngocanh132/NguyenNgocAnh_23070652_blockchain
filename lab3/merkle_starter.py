import hashlib


def H(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def _leaf_hashes(leaves):
    return [H(x) if isinstance(x, bytes) else H(x.encode()) for x in leaves]


# TODO 1
def merkle_root(leaves) -> bytes:
    """Dựng cây từ dưới lên; nhân đôi nút cuối khi tầng lẻ (quy tắc Bitcoin)."""
    if not leaves:
        raise ValueError("no leaves")
    level = _leaf_hashes(leaves)
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])          # duplicate last node
        level = [H(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


# TODO 2
def merkle_proof(leaves, index):
    """Trả về list (sibling_hash, is_left) từ lá lên gốc."""
    level = _leaf_hashes(leaves)
    proof = []
    idx = index
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        if idx % 2 == 0:                      # node is left -> sibling on right
            proof.append((level[idx + 1], False))
        else:                                 # node is right -> sibling on left
            proof.append((level[idx - 1], True))
        level = [H(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
        idx //= 2
    return proof


# TODO 3
def verify_proof(leaf_hash: bytes, proof, root: bytes) -> bool:
    """Tính ngược lên và so sánh với root."""
    cur = leaf_hash
    for sibling, is_left in proof:
        cur = H(sibling + cur) if is_left else H(cur + sibling)
    return cur == root


if __name__ == "__main__":
    txs = [f"tx{i}" for i in range(7)]            # odd length on purpose
    root = merkle_root(txs)
    print("root:", root.hex())

    # CHECK 1: determinism
    print("CHECK 1 deterministic:", "OK" if merkle_root(txs) == root else "FAIL")

    # CHECK 2: every leaf has a valid proof
    ok = all(verify_proof(H(t.encode()), merkle_proof(txs, i), root)
             for i, t in enumerate(txs))
    print("CHECK 2 all proofs valid:", "OK" if ok else "FAIL")

    # CHECK 3: tampered leaf is rejected
    p = merkle_proof(txs, 3)
    print("CHECK 3 tampered leaf rejected:",
          "OK" if not verify_proof(H(b"tx3-evil"), p, root) else "FAIL")

    # CHECK 4: changing any tx changes the root
    txs2 = txs.copy(); txs2[5] = "tx5-evil"
    print("CHECK 4 root changes:", "OK" if merkle_root(txs2) != root else "FAIL")

    # CHECK 5: single leaf and power-of-two sizes
    print("CHECK 5 single leaf:",
          "OK" if merkle_root(["a"]) == H(b"a") else "FAIL")
    big = [str(i) for i in range(1000)]
    r = merkle_root(big)
    print("CHECK 6 n=1000 proofs:",
          "OK" if all(verify_proof(H(x.encode()), merkle_proof(big, i), r)
                      for i, x in enumerate(big)) else "FAIL")
    print("proof length for n=1000:", len(merkle_proof(big, 0)))
