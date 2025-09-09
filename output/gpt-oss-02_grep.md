Below are a handful of ways to pull **only** the UUID out of a line that looks like  

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

The most compact solution uses **GNU grep** with Perl‑compatible regular expressions (`-P`).  
If you’re on macOS or another system that doesn’t support `-P`, I’ve added pure‑POSIX alternatives (awk, sed, etc.) and a “clean‑API” way that doesn’t need any text‑parsing at all.

---

## 1️⃣ One‑liner with `grep -oP`

```bash
# Keep the leading “GPU-” prefix
nvidia-smi -L | grep -oP '(?<=UUID: )GPU-[0-9a-fA-F-]+'

# Or drop the “GPU-” part and get just the hex string
nvidia-smi -L | grep -oP '(?<=UUID: GPU-)\K[0-9a-fA-F-]+'
```

**How it works**

| Piece                     | Meaning |
|---------------------------|---------|
| `-o`                      | Print only the part of the line that matches |
| `-P`                      | Enable PCRE (Perl‑compatible) regex syntax |
| `(?<=UUID: )`             | Positive *look‑behind*: the match must be preceded by `UUID: ` (but that text isn’t part of the output) |
| `GPU-`                    | Literal prefix (optional – drop it if you don’t need it) |
| `[0-9a-fA-F-]+`           | One or more hex digits or hyphens |
| `\K` (in the second example) | Reset the start of the reported match, so only the part **after** `GPU-` is printed |

> **Note:** `-P` is a GNU extension. On macOS you can get it via Homebrew (`brew install grep`) and call it `ggrep`, or just use any of the POSIX alternatives below.

---

## 2️⃣ POSIX‑only alternatives (works everywhere)

### 2.1 Using `grep -oE` + a tiny `sed` post‑process

```bash
nvidia-smi -L \
  | grep -oE 'UUID: [^)]+' \
  | sed -E 's/^UUID: //; s/[)]$//'
```

* `grep -oE 'UUID: [^)]+'` grabs the text from `UUID:` up to the closing parenthesis.  
* `sed` strips the leading label and any trailing `)`.

### 2.2 Pure `awk`

```bash
nvidia-smi -L | awk -F'UUID: |[)]' '/^GPU 0:/ {print $2}'
```

* `-F'UUID: |[)]'` tells `awk` to split each line on either the literal `UUID: ` **or** a closing parenthesis.  
* `$2` is the field that contains the UUID.

### 2.3 Pure `sed`

```bash
nvidia-smi -L \
  | sed -n 's/.*UUID: \([^)]*\)).*/\1/p'
```

* The capture group `\([^)]*\)` grabs everything up to the next `)`; the rest of the line is discarded.

---

## 3️⃣ Avoid parsing altogether – use `nvidia‑smi`’s query mode

If you only need the UUID(s), let `nvidia‑smi` give you exactly that:

```bash
# All GPUs, one UUID per line
nvidia-smi --query-gpu=uuid --format=csv,noheader

# Just GPU 0 (if you have more than one)
nvidia-smi --query-gpu=uuid --format=csv,noheader -i 0
```

* No regular expressions, no fragile text‑scraping.  
* Works on any driver version that supports `--query-gpu`.

---

## 4️⃣ Putting it together in a script

Below is a tiny Bash function that works on any platform (falls back to `awk` if `grep -P` isn’t available) and returns the UUID **without** the `GPU-` prefix:

```bash
#!/usr/bin/env bash
# get_gpu_uuid <gpu-index>
#   Prints the UUID for the given GPU (default 0)
#   Works with GNU grep, BSD grep, awk, or nvidia-smi query mode.

get_gpu_uuid() {
    local idx=${1:-0}
    # Prefer the official query API – fastest & safest
    if command -v nvidia-smi >/dev/null; then
        nvidia-smi --query-gpu=uuid --format=csv,noheader -i "$idx" 2>/dev/null | head -n1
        return
    fi

    # If nvidia-smi is not available, fall back to parsing `-L` output
    local line
    line=$(nvidia-smi -L 2>/dev/null | grep -E "^GPU $idx:" || true)

    # Try GNU grep first
    if grep -P '' </dev/null 2>/dev/null; then
        echo "$line" | grep -oP '(?<=UUID: GPU-)\K[0-9a-fA-F-]+'
        return
    fi

    # awk fallback
    echo "$line" | awk -F'UUID: |[)]' '{print $2}' | sed 's/^GPU-//'
}

# Example usage
uuid=$(get_gpu_uuid 0)
printf 'GPU‑0 UUID = %s\n' "$uuid"
```

*The function first asks `nvidia‑smi` for the UUID directly. If that fails (e.g. older drivers), it parses the output of `nvidia‑smi -L` using the most capable tool available.*

---

## 5️⃣ Quick cheat‑sheet

| Goal | Command (one‑liner) | Keeps `GPU-`? | Requires GNU `grep`? |
|------|----------------------|---------------|----------------------|
| **Exact string with prefix** | `nvidia-smi -L \| grep -oP '(?<=UUID: )GPU-[0-9a-fA-F-]+'` | ✅ | ✅ |
| **Only the hex part** | `nvidia-smi -L \| grep -oP '(?<=UUID: GPU-)\K[0-9a-fA-F-]+'` | ❌ | ✅ |
| **POSIX, no `-P`** | `nvidia-smi -L \| awk -F'UUID: |[)]' '/^GPU 0:/ {print $2}'` | ✅ | ❌ |
| **No parsing, just ask** | `nvidia-smi --query-gpu=uuid --format=csv,noheader -i 0` | ✅ (already raw) | ❌ |

---

### TL;DR

```bash
# Keep “GPU-” prefix
nvidia-smi -L | grep -oP '(?<=UUID: )GPU-[0-9a-fA-F-]+'

# Drop the prefix (just the hex UUID)
nvidia-smi -L | grep -oP '(?<=UUID: GPU-)\K[0-9a-fA-F-]+'

# Portable fallback (awk)
nvidia-smi -L | awk -F'UUID: |[)]' '/^GPU 0:/ {print $2}'
```

Pick whichever fits your environment and preference! 🚀