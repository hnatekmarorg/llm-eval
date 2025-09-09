To extract **only the UUID** from a line like:

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

You can use `grep` combined with `sed` or `awk` to extract just the UUID part.

### ✅ Recommended Solution using `grep` and `sed`:

```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | \
grep -o 'UUID: [^)]*' | sed 's/UUID: //'
```

### 🔍 Explanation:
- `grep -o 'UUID: [^)]*'` — extracts only the match `UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53`
- `sed 's/UUID: //'` — removes the `UUID: ` prefix, leaving just the UUID.

### ✅ Output:
```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

---

### Alternative: Pure `grep` with Perl-compatible regex (if supported):

```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | \
grep -oP 'UUID: \K[^)]*'
```

- `-P` enables Perl-compatible regex.
- `\K` means "keep everything after this point", so it drops `UUID: ` and keeps the UUID.

---

### Final Tip:
If you're processing output from `nvidia-smi`, you can do:

```bash
nvidia-smi --query-gpu=index,uuid --format=csv,noheader,nounits | grep "GPU 0"
```

But if you're parsing raw output, the `grep` + `sed` or `grep -P` method above is perfect.

Let me know if you want to extract from a file or multiple GPUs!