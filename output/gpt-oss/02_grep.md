Below are a few one‑liners that will pull **only the UUID** from a line such as  

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

All of them assume the text is coming from a pipe (e.g. `nvidia‑smi -L`) or is stored in a variable.

---

## 1. Using `grep` with PCRE (`-P`) and `-o` (only‑match)

```bash
nvidia-smi -L | grep -oP '(?<=UUID: )[^)]+'
# → GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

**How it works**

* `-o`  – print only the part of the line that matches the pattern.  
* `-P`  – enable Perl‑compatible regular expressions (PCRE).  
* `(?<=UUID: )` – a *look‑behind* that asserts “UUID: ” is just before the match, but it’s not part of the output.  
* `[^)]+` – one or more characters that are **not** a closing parenthesis (i.e. everything up to the `)`).

If your `grep` does **not** support `-P`, you can achieve the same thing with the `\K` trick (also PCRE only):

```bash
nvidia-smi -L | grep -oP 'UUID:\s*\K[^)]+'
```

---

## 2. Using `sed`

```bash
nvidia-smi -L | sed -n 's/.*UUID: \([^)]*\)).*/\1/p'
# → GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

**Explanation**

* `-n` – suppress automatic printing.  
* The substitution `s/.*UUID: \([^)]*\)).*/\1/` captures everything between `UUID: ` and the next `)`.  
* `p` – print the substituted line only if the substitution succeeded.

---

## 3. Using `awk`

```bash
nvidia-smi -L | awk -F'UUID: ' '{sub(/\).*/, "", $2); print $2}'
# → GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

* `-F'UUID: '` splits the line into two fields on the literal “UUID: ”.  
* `sub(/\).*/, "", $2)` removes the trailing `)` and anything after it.  
* `print $2` outputs the cleaned UUID.

---

## 4. Pure `cut`/`tr` pipeline (no regex)

```bash
nvidia-smi -L |
cut -d '(' -f2 |            # keep "UUID: GPU-… )"
cut -d ')' -f1 |            # drop the trailing ')'
cut -d ':' -f2 |            # keep the part after "UUID:"
tr -d ' '                   # strip any stray spaces
# → GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

This works everywhere, but it’s a bit more fragile if the format ever changes.

---

## 5. Quick “just the UUID pattern” with `grep`

If you only care that the UUID starts with `GPU-` and contains hex digits/hyphens, you can skip the surrounding text altogether:

```bash
nvidia-smi -L | grep -oE 'GPU-[0-9a-fA-F-]+'
# → GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

`-E` (POSIX extended regex) is universally supported, and the pattern matches the UUID itself.

---

### Which one should you use?

| Tool | Availability | Regex needed? | Best for |
|------|--------------|---------------|----------|
| `grep -P` | GNU grep (most Linux) | Yes (PCRE) | Concise, readable |
| `sed` | POSIX everywhere | Yes (basic regex) | Portable, no PCRE |
| `awk` | POSIX everywhere | Minimal | When you’re already using `awk` for other processing |
| `cut`/`tr` | Anywhere | No | When you prefer field‑splitting only |
| `grep -E` | Everywhere | Simple pattern | Quick “match the UUID format” |

Pick the one that matches the tools you already have on your target system. All of them will give you just the UUID string (`GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53`). Happy scripting!