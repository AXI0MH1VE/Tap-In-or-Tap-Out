#
"""
AXIOM HIVE — Signature Tool — C=0
Signs a file with Ed25519 and writes .sig and .sha256; stores keys in keys/ed25519.json
"""
import sys, os, json, hashlib, base64
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder

def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_or_create_keys():
    os.makedirs("keys", exist_ok=True)
    key_path = os.path.join("keys", "ed25519.json")
    if os.path.exists(key_path):
        with open(key_path, "r") as f: return json.load(f)
    sk = SigningKey.generate()
    kp = {"sk": Base64Encoder.encode(sk.encode()).decode("utf-8"),
          "vk": Base64Encoder.encode(sk.verify_key.encode()).decode("utf-8")}
    with open(key_path, "w") as f: json.dump(kp, f, indent=2, sort_keys=True)
    return kp

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/sign_document.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    kp = load_or_create_keys()
    sk = SigningKey(Base64Encoder.decode(kp["sk"]), encoder=Base64Encoder)
    with open(path, "rb") as f:
        data = f.read()
    sig = sk.sign(data).signature
    sig_b64 = base64.b64encode(sig).decode("utf-8")
    sha = sha256(path)
    with open(path + ".sig", "w") as f: f.write(sig_b64 + "\n")
    with open(path + ".sha256", "w") as f: f.write(sha + "\n")
    print(f"Signed: {path}\nSHA-256: {sha}\nSignature: {path}.sig\nKeys: keys/ed25519.json")

if __name__ == "__main__":
    main()
