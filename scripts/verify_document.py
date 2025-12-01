#
"""
AXIOM HIVE — Verify Tool — C=0
Verifies .sig and .sha256 for a file using keys/ed25519.json
"""
import sys, os, json, hashlib, base64
from nacl.signing import VerifyKey
from nacl.encoding import Base64Encoder

def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/verify_document.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    sig_path = path + ".sig"
    sha_path = path + ".sha256"
    key_path = os.path.join("keys", "ed25519.json")
    if not all(map(os.path.exists, [sig_path, sha_path, key_path])):
        print("Missing .sig/.sha256/keys/ed25519.json"); sys.exit(2)
    with open(key_path, "r") as f: kp = json.load(f)
    vk = VerifyKey(Base64Encoder.decode(kp["vk"]), encoder=Base64Encoder)
    with open(sig_path, "r") as f: sig_b64 = f.read().strip()
    sig = base64.b64decode(sig_b64.encode("utf-8"))
    with open(path, "rb") as f: data = f.read()
    try:
        vk.verify(data, sig)
    except Exception:
        print("Signature verification: FAIL"); sys.exit(3)
    sha = sha256(path)
    with open(sha_path, "r") as f: expected = f.read().strip()
    if sha != expected:
        print("SHA-256 mismatch: FAIL"); sys.exit(4)
    print("Verification: PASS")

if __name__ == "__main__":
    main()
