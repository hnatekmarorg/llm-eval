To extract **only the UUID** from a line like:

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

You can use `grep` combined with `sed` or `awk` to extract just the UUID part.

### ✅ Recommended Command:

```bash
grep -o 'UUID: [^)]*' | sed 's/UUID: //'
```

Or using `awk`:

```bash
grep -o 'UUID: [^)]*' | awk '{print $2}'
```

Or even more directly with `grep` and Perl-compatible regex (if supported):

```bash
grep -oP 'UUID: \K[^)]+'
```

---

### 🔍 Explanation:

- `grep -o`: outputs only the matching part (not the whole line).
- `'UUID: [^)]*'`: matches "UUID: " followed by any characters that are not a closing parenthesis.
- `sed 's/UUID: //'`: removes the "UUID: " prefix.
- `awk '{print $2}'`: splits on whitespace and prints the second field (the UUID).
- `-P` (PCRE): enables Perl-compatible regex.
- `\K`: keeps everything after the match (so "UUID: " is excluded).

---

### ✅ Example:

```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | grep -oP 'UUID: \K[^)]+'
```

**Output:**
```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

This is clean and precise — just the UUID.

---

### 📝 Note:
If you're using `grep` on macOS (which doesn't support `-P`), use `sed` or `awk` instead:

```bash
grep -o 'UUID: [^)]*' | sed 's/UUID: //'
```

That will work everywhere.