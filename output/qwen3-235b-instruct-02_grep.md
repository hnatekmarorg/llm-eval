To extract **only the UUID** from a line like:

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

You can use `grep` with Perl-compatible regex (`-P`) and lookarounds, or combine `grep` with other tools like `sed` or `awk`. Here are a few clean approaches:

---

### ✅ Option 1: Using `grep -oP` (recommended if available)

```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | grep -oP 'UUID:\s*\K[^\)]+'
```

**Output:**
```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

- `-o`: only output the matched part
- `-P`: enables Perl-compatible regex
- `\K`: discards everything before it (so we don't include "UUID: ")
- `[^\)]+`: matches all characters up to the closing parenthesis

---

### ✅ Option 2: Using `grep` + `sed`

```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | grep -o 'UUID: [^)]*' | sed 's/UUID: //'
```

**Output:**
```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

---

### ✅ Option 3: Using `awk`

```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | awk '{gsub(/.*UUID: |\\)$/, "", $0)}1'
```

Or more clearly:

```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | awk -F'UUID: |\\)' '{print $2}'
```

**Output:**
```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

This splits the line on `UUID: ` or `)` and prints the second field.

---

### Summary

The most concise and reliable method (if `grep -P` is available) is:

```bash
grep -oP 'UUID:\s*\K[^\)]+'
```

Use this in scripts or pipelines to extract just the UUID value.