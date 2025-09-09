Below are a few one‑liners that pull **only** the UUID (`GPU‑f0f6d00d‑5367‑e890‑eea9‑e568a84a7d53`) out of a line that looks like

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

All of them assume the text is coming from `nvidia‑smi -L`, but you can replace that part with any command (or a file name) that produces the same line.

---

## 1. Using **grep** with PCRE (`-P`) and only‑matching (`-o`)

```bash
nvidia-smi -L | grep -Po '(?<=\(UUID: )[^)]*'
```

**Explanation**

| flag | meaning |
|------|----------|
| `-P` | Enable PCRE (Perl‑compatible regular expressions) – needed for look‑behinds. |
| `-o` | Print **only** the part of the line that matches the pattern. |

The pattern itself:

- `(?<=\(UUID: )` – a *positive look‑behind* that asserts the match is preceded by the literal `(UUID: ` (the opening parenthesis is escaped). It does **not** become part of the output.
- `[^)]*` – then match any characters that are **not** a closing parenthesis, up to the first `)`.  

Result: `GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53`

---

## 2. Grep without PCRE (POSIX‑compatible)

If your `grep` doesn’t support `-P` (e.g., on some older macOS installations), you can still do it with a two‑step approach:

```bash
nvidia-smi -L | grep -o 'UUID: [^)]*' | cut -d' ' -f2
```

- `grep -o 'UUID: [^)]*'` → prints `UUID: GPU-f0f6d00d-...`  
- `cut -d' ' -f2` → cuts the second whitespace‑separated field, leaving just the UUID.

---

## 3. Using **sed**

```bash
nvidia-smi -L | sed -n 's/.*(UUID: \([^)]*\)).*/\1/p'
```

- `sed -n` suppresses automatic printing.
- The substitution `s/.*(UUID: \([^)]*\)).*/\1/` captures everything between `(UUID: ` and the next `)` (the `\([^)]*\)` part) and replaces the whole line with that capture (`\1`).
- The trailing `p` prints only lines where the substitution succeeded.

---

## 4. Using **awk**

```bash
nvidia-smi -L | awk -F'[(]UUID: |[)]' '{print $2}'
```

- The field separator (`-F`) tells `awk` to split on either “`(UUID: `” **or** “`)`”.  
- After the split, the UUID lands in field 2, which we print.

---

## 5. Bash built‑in (no external tools)

If you already have the line in a Bash variable `$line`:

```bash
if [[ $line =~ UUID:\ ([^)]+) ]]; then
    echo "${BASH_REMATCH[1]}"
fi
```

`BASH_REMATCH[1]` holds the part matched by the parentheses in the regex (`[^)]+` → “one or more characters that aren’t a closing parenthesis”).

---

### Quick cheat‑sheet

| Tool | Command | Works on all `grep`? |
|------|---------|----------------------|
| **grep (PCRE)** | `grep -Po '(?<=\(UUID: )[^)]*'` | ✅ (requires GNU grep ≥ 2.22) |
| **grep + cut** | `grep -o 'UUID: [^)]*' | cut -d' ' -f2` | ✅ |
| **sed** | `sed -n 's/.*(UUID: \([^)]*\)).*/\1/p'` | ✅ |
| **awk** | `awk -F'[(]UUID: |[)]' '{print $2}'` | ✅ |
| **Bash** | `[[ $line =~ UUID:\ ([^)]+) ]] && echo "${BASH_REMATCH[1]}"` | ✅ (no external) |

Pick the one you like best (or the one that works on the system you’re on). All of them will output **just** the UUID string. Happy scripting!