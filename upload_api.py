import os, base64, subprocess, sys

GH = r"C:\Program Files\GitHub CLI\gh.exe"
REPO = "kh4tzjsjfy-eng/familyAlbum"
BASE = os.path.dirname(os.path.abspath(__file__))

files = []
for root, dirs, fnames in os.walk(BASE):
    dirs[:] = [d for d in dirs if d != ".git"]
    for fn in fnames:
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, BASE).replace("\\", "/")
        files.append((rel, p))
files.sort()

ok = 0
for rel, p in files:
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    body = '{"message":"add %s","content":"%s"}' % (rel, b64)
    r = subprocess.run(
        [GH, "api", "-X", "PUT", "repos/%s/contents/%s" % (REPO, rel), "--input", "-"],
        input=body.encode(), capture_output=True)
    if r.returncode == 0:
        print("OK  ", rel)
        ok += 1
    else:
        print("FAIL", rel, r.stderr.decode(errors="replace")[:300], file=sys.stderr)

print("\n%d/%d files uploaded" % (ok, len(files)))
sys.exit(0 if ok == len(files) else 1)
