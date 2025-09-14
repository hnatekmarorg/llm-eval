To extract **only the UUID** from the line:

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

You can use `grep` with **PCRE (Perl Compatible Regular Expressions)** to match and extract just the UUID value. Here's the best way:

---

### ✅ Recommended Command:

```bash
grep -oP 'UUID: \KGPU-[a-f0-9-]+'
```

#### Explanation:
- `grep -o` → Output only the matched part
- `grep -P` → Enable Perl-compatible regex (needed for `\K`)
- `UUID: ` → Match literal text
- `\K` → **Keep** everything before this point out of the match (i.e., don’t include "UUID: " in output)
- `GPU-[a-f0-9-]+` → Match the UUID pattern: starts with `GPU-`, then hex digits and hyphens

#### Output:
```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

---

### 🚫 Alternative (if `-P` is not available, e.g., on macOS):

If you're on macOS or a system without `grep -P`, use `sed` instead:

```bash
sed -n 's/.*UUID: \(GPU-[a-f0-9-]\+\).*/\1/p'
```

#### Explanation:
- `-n` → suppress default output
- `s/.../\1/p` → substitute entire line with the captured group (the UUID), then print

---

### 💡 Bonus: Extract from `nvidia-smi` output directly

If this line comes from `nvidia-smi --query-gpu=uuid --format=csv`, you might not need `grep` at all — but if you're parsing raw `nvidia-smi` output like:

```bash
nvidia-smi
```

...and want to extract GPU 0’s UUID, use:

```bash
nvidia-smi --query-gpu=index,uuid --format=csv | grep "^0," | cut -d',' -f2 | xargs
```

This is **more reliable** than parsing human-readable text — use the CSV output format when possible.

---

### ✅ Final Recommendation

Use this if you're grepping from a text line:

```bash
grep -oP 'UUID: \KGPU-[a-f0-9-]+'
```

Use this if you’re parsing `nvidia-smi` (best practice):

```bash
nvidia-smi --query-gpu=uuid --format=csv,noheader,nounits | head -n 1
```

*(Assumes GPU 0 is first — adjust `head -n 1` to `sed -n '2p'` for GPU 1, etc.)*

Let me know if you want to extract UUIDs for all GPUs!