Below is a **complete, drop‑in replacement** for the original program that reads the whole scene (camera + objects) from a YAML file instead of being hard‑coded in Go.  
The changes are:

1. **YAML parsing** – using `gopkg.in/yaml.v3` to un‑marshal a `scene.yaml` file into Go structs.  
2. **Typed scene description** – `CameraConfig`, `SphereConfig` (and a placeholder for other objects) map one‑to‑one to the YAML layout.  
3. **Factory loop** – after unmarshalling we turn each config entry into the appropriate `core.RayMarchableObject` (currently only spheres).  
4. **Better error handling** – every I/O step is checked and reported to `stderr`.  
5. **CLI flag (optional)** – you can pass the path to the yaml file (`-scene my.yaml`), otherwise `scene.yaml` is used.

---

## 1. `scene.yaml` – the data file

```yaml
scene:
  camera:
    width: 512
    height: 512
    direction: [0, 0, 1]
  objects:
    - sphere:
        position: [0, 0, -2]
        radius: 1
    - sphere:
        position: [1, 0, -2]
        radius: 1
    - sphere:
        position: [0.5, 1, -2]
        radius: 1
    - sphere:
        position: [0, 0, -0.5]
        radius: 0.1
```

Feel free to add more objects later – just follow the same pattern (a map whose key is the object type).

---

## 2. `go.mod`

```go
module github.com/yourname/sunshine-demo

go 1.22

require (
    github.com/hnatekmarorg/sunshine v0.0.0-2024xxxxxx   // whatever version you use
    gopkg.in/yaml.v3 v3.0.1
)
```

Run `go mod tidy` after adding the file – the yaml module will be pulled in automatically.

---

## 3. Refactored `main.go`

```go
package main

import (
	"flag"
	"fmt"
	"image/png"
	"os"

	"github.com/hnatekmarorg/sunshine/core"
	"gopkg.in/yaml.v3"
)

/* --------------------------------------------------------------------------
   1️⃣  Scene description structs – these map 1‑to‑1 to the YAML layout
   --------------------------------------------------------------------------*/

type Config struct {
	Scene struct {
		Camera  CameraConfig   `yaml:"camera"`
		Objects []ObjectConfig `yaml:"objects"`
	} `yaml:"scene"`
}

// CameraConfig mirrors the YAML camera fields.
type CameraConfig struct {
	Width     int       `yaml:"width"`
	Height    int       `yaml:"height"`
	Direction []float64 `yaml:"direction"` // must be length‑3
}

// ObjectConfig is a *union* – only one of its fields will be non‑nil after
// unmarshalling.  Add new object types here as you need them.
type ObjectConfig struct {
	Sphere *SphereConfig `yaml:"sphere,omitempty"`
	// Plane *PlaneConfig `yaml:"plane,omitempty"`   // example placeholder
}

// SphereConfig holds the data required to instantiate a core.NewSphere.
type SphereConfig struct {
	Position []float64 `yaml:"position"` // must be length‑3
	Radius   float64   `yaml:"radius"`
}

/* --------------------------------------------------------------------------
   2️⃣  Helper to load and parse the YAML file
   --------------------------------------------------------------------------*/

func loadConfig(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("reading %s: %w", path, err)
	}
	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("unmarshalling yaml: %w", err)
	}
	return &cfg, nil
}

/* --------------------------------------------------------------------------
   3️⃣  Main – glue everything together
   --------------------------------------------------------------------------*/

func main() {
	// Optional CLI flag so the user can point at any yaml file.
	scenePath := flag.String("scene", "scene.yaml", "path to the scene description (yaml)")
	flag.Parse()

	// 1️⃣ Load the yaml.
	cfg, err := loadConfig(*scenePath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "❌ error loading scene: %v\n", err)
		os.Exit(1)
	}

	// 2️⃣ Build the core.Camera from the config.
	cam := core.Camera{
		Width:     cfg.Scene.Camera.Width,
		Height:    cfg.Scene.Camera.Height,
		Direction: cfg.Scene.Camera.Direction,
	}

	// 3️⃣ Convert each object config into a core.RayMarchableObject.
	var objects []core.RayMarchableObject
	for i, oc := range cfg.Scene.Objects {
		switch {
		case oc.Sphere != nil:
			s := core.NewSphere(oc.Sphere.Position, oc.Sphere.Radius)
			objects = append(objects, s)
		default:
			// If we ever add more object types we’ll extend this switch.
			fmt.Fprintf(os.Stderr, "⚠️  object %d: unknown/unsupported type – skipping\n", i)
		}
	}

	// 4️⃣ Render.
	img := cam.Render(objects)

	// 5️⃣ Write PNG.
	out, err := os.Create("output.png")
	if err != nil {
		fmt.Fprintf(os.Stderr, "❌ cannot create output.png: %v\n", err)
		os.Exit(1)
	}
	defer out.Close()

	if err := png.Encode(out, img); err != nil {
		fmt.Fprintf(os.Stderr, "❌ png encoding failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("✅ rendered image saved as output.png")
}
```

### What changed, step‑by‑step?

| Original | New |
|----------|-----|
| Hard‑coded `core.Camera{...}` | Populated from `cfg.Scene.Camera`. |
| Hard‑coded slice of `core.NewSphere(...)` | Dynamically built by iterating over `cfg.Scene.Objects`. |
| No error handling for file I/O | All I/O now returns clear messages and exits with a non‑zero status on failure. |
| Fixed file name `output.png` | Same, but now preceded by a helpful log line. |
| No external configuration | The program now reads `scene.yaml` (or a file passed via `-scene`). |

---

## 4️⃣  Extending the format (future‑proof)

If you later want to support more primitives (e.g. planes, boxes, meshes), just:

1. Add a config struct (`type PlaneConfig struct { … }`).  
2. Add a pointer field to `ObjectConfig` (`Plane *PlaneConfig `yaml:"plane,omitempty"`).  
3. Add a case in the `switch` that creates the appropriate `core.New…` object.

Because the YAML uses a **keyed map per object**, adding a new type never collides with existing entries.

---

## 5️⃣  Running the demo

```bash
# 1️⃣  Ensure dependencies are present
go mod tidy

# 2️⃣  Build (or just run)
go run .
# or
go build -o render && ./render -scene scene.yaml
```

You should see:

```
✅ rendered image saved as output.png
```

and `output.png` will contain exactly the same picture that the original hard‑coded program produced – but now the whole scene lives in a human‑editable YAML file.

---

### TL;DR

*Define a Go struct that mirrors the YAML layout, unmarshal the file, build the `core.Camera` and a slice of `core.RayMarchableObject` from those structs, then render as before.*  
The snippet above does precisely that, with clean error handling and a small CLI flag for convenience. Happy rendering!