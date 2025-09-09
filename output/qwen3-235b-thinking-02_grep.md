To extract **only the UUID** from the string `GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)`, use one of these methods:

---

### 1. **Using `grep` with PCRE (most efficient, requires GNU `grep`):**
```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | grep -oP 'UUID: \K[^\)]+'
```
**Output:**  
`GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53`

#### How it works:
- `-oP` enables **Perl-Compatible Regular Expressions (PCRE)**.
- `UUID: \K` matches `UUID: ` and discards it (`\K` resets the match start).
- `[^\)]+` captures all characters until the next `)`.

> ✅ **Best for Linux systems** (GNU `grep` is standard).  
> ❌ Not supported on macOS BSD `grep` (without GNU tools).

---

### 2. **Portable method (works everywhere, uses `grep` + `sed`):**
```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | grep -o 'UUID: [^)]*' | sed 's/UUID: //'
```
**Output:**  
`GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53`

#### How it works:
- `grep -o 'UUID: [^)]*'` extracts the substring `UUID: GPU-...` (up to the next `)`).
- `sed 's/UUID: //'` removes the prefix `UUID: `, leaving only the UUID.

> ✅ **Works on all systems** (Linux, macOS, BSD).  
> ✅ No dependencies beyond standard shell tools.

---

### Why these work:
- The UUID **always follows `UUID: `** and **ends before `)`** in NVIDIA's output.
- Both methods isolate the exact UUID string (`GPU-...`) without extra characters.

---

### Example with a file (if your data is in a file):
```bash
# Using PCRE (Linux):
grep -oP 'UUID: \K[^\)]+' /path/to/file.log

# Portable method (all systems):
grep -o 'UUID: [^)]*' /path/to/file.log | sed 's/UUID: //'
```

> 💡 **Note for macOS users**:  
> Install GNU `grep` via Homebrew (`brew install grep`) to use the `-P` method, or stick with the portable `grep` + `sed` solution.