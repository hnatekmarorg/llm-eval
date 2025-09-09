To extract **only the UUID** from a line like:

```
GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)
```

You can use `grep` with Perl-compatible regex (`-P`) and the `-o` flag to extract just the UUID part.

### ✅ Command:
```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | grep -oP 'UUID: \KGPU-[a-f0-9\-]+'
```

### Output:
```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

---

### Explanation:
- `grep -oP`: Enables Perl-compatible regex and outputs only the matched part.
- `\K`: Discards everything before it (so "UUID: " is matched but not included in output).
- `GPU-[a-f0-9\-]+`: Matches the UUID pattern starting with `GPU-` followed by hex digits and hyphens.

---

### Alternative using `sed`:
```bash
echo "GPU 0: NVIDIA GeForce RTX 4060 Laptop GPU (UUID: GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53)" | sed -n 's/.*UUID: \(GPU-[a-f0-9\-]\+\).*/\1/p'
```

Same output.

---

### If you're parsing actual `nvidia-smi` output:
```bash
nvidia-smi --query-gpu=uuid --format=csv,noheader,nounits
```

This directly returns just the UUID(s), no parsing needed.

Example output:
```
GPU-f0f6d00d-5367-e890-eea9-e568a84a7d53
```

✅ This is the cleanest and most reliable method if you just want UUIDs from NVIDIA GPUs.