from eth_account import Account
from eth_account.messages import encode_defunct

acct = Account.create()  # NEVER use this key for real funds
print("address:", acct.address)

msg = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 3")
sig = Account.sign_message(msg, acct.key)
print("r,s,v:", hex(sig.r), hex(sig.s), sig.v)

who = Account.recover_message(msg, signature=sig.signature)
print("recovered:", who, "| match:", who == acct.address)

# Task 1: sign the same message again with the SAME key -> identical signature?
sig2 = Account.sign_message(msg, acct.key)
print("same signature on 2nd sign:", sig.signature == sig2.signature)

bad = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 4")
tampered = Account.recover_message(bad, signature=sig.signature)
print("tampered ->", tampered, "| differs:", tampered != acct.address)
