#!/usr/bin/env python3
import datetime
import hashlib
import json
import os
from pathlib import Path


def utc_now():
    """Return the current UTC time as an ISO-8601 string."""
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


issued_at = utc_now()
random_nonce = os.urandom(8).hex()

nonce = f"{issued_at}-nonce-{random_nonce}"

data = {
    "challenge": nonce,
    "issued_at": issued_at,
    "issued_by": "locustjr@proton.me",
}

# Canonical representation:
# - UTF-8
# - sorted object keys
# - no insignificant whitespace
canonical = json.dumps(
    data,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
).encode("utf-8")

sha256 = hashlib.sha256(canonical).hexdigest()

output = Path("challenge.canonical.json")
output.write_bytes(canonical)

print("challenge:", nonce)
print("issued_at:", issued_at)
print("canonical_sha256:", sha256)
print("file:", output)
