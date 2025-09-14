

To extract the **UUID** from the line:

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

you can use the following command with `grep` and **Perl-compatible regular expressions (`-P`)**:

---

### ✅ Command:

```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | grep -oP 'UUID: \K[0-9a-f-]+'
```

---

### 🔍 Explanation:

- `grep -oP`:  
  - `-o` prints **only the matched parts** of the line.  
  - `-P` enables **Perl-compatible regular expressions**, which allows the use of the `\K` modifier.

- `'UUID: \K[0-9a-f-]+'`:  
  - `UUID: `: Matches the literal string "UUID: "  
  - `\K`: **Discards** the previous matched part, effectively resetting the match so it starts from the character after "UUID: "  
  - `[0-9a-f-]+`: Matches the UUID string, which contains hexadecimal digits (`0-9`, `a-f`) and hyphens (`-`)

---

### 🔁 Output:

```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

---

### 📌 Notes:
- This assumes you have a `grep` that supports **Perl-compatible regular expressions** (e.g., `grep -P` in modern GNU `grep`).
- If you don’t have `-P`, you can use a combination of `grep`, `sed`, or `awk` for a more compatible solution. For example:

```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | grep -o 'UUID: [0-9a-f-]*' | sed 's/UUID: //'
```

This version uses `sed` to remove the "UUID: " prefix after matching.

---

### 📌 Summary:
Use the `grep -oP` command with the regex `UUID: \K[0-9a-f-]+` to **extract the UUID directly** from the line. This is efficient, concise, and works well with modern tools.