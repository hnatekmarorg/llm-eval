To extract **only the UUID** from a line like:

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

You can use `grep` with a regular expression and `sed` (or `grep -o` with proper pattern) to extract just the UUID.

### ✅ Recommended Command:

```bash
grep -o 'UUID: [^)]*' file.txt | sed 's/UUID: //'
```

Or using `grep` with Perl-compatible regex (if supported):

```bash
grep -oP 'UUID: \K[^)]*' file.txt
```

### 🔍 Explanation:

- `grep -o`: Outputs only the matched part (not the whole line).
- `'UUID: [^)]*'`: Matches `UUID: ` followed by any characters that are not `)` — this stops at the closing parenthesis.
- `sed 's/UUID: //'`: Removes the `UUID: ` prefix.
- `-P` (Perl regex): Enables PCRE, and `\K` means "keep everything after this point", so it discards `UUID: `.

### Example:

Given input:
```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

Running:
```bash
grep -oP 'UUID: \K[^)]*' <<< "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)"
```

Output:
```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

### ✅ Final Answer (cleanest):
```bash
grep -oP 'UUID: \K[^)]*' file.txt
```

> ✅ This gives you **only the UUID** as output.  
> ⚠️ Make sure your `grep` supports `-P` (e.g., GNU grep on Linux). On macOS, use `pcregrep` or install `grep` via Homebrew.