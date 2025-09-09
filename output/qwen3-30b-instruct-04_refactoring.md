Here's a refactored version of your Go code that loads the scene from a YAML file instead of hardcoding it. We'll use `gopkg.in/yaml.v3` for YAML parsing and update the `core` package to support deserialization.

---

### ✅ Step 1: Install YAML dependency
Make sure you have `gopkg.in/yaml.v3` installed:

```bash
go get gopkg.in/yaml.v3
```

---

### ✅ Step 2: Update your `main.go`

```go
package main

import (
	"fmt"
	"github.com/hnatekmarorg/sunshine/core"
	"image/png"
	"os"
	"gopkg.in/yaml.v3"
)

// SceneConfig represents the structure of the YAML scene file
type SceneConfig struct {
	Camera struct {
		Width     int      `yaml:"width"`
		Height    int      `yaml:"height"`
		Direction []float64 `yaml:"direction"`
	} `yaml:"camera"`
	Objects []ObjectConfig `yaml:"objects"`
}

type ObjectConfig struct {
	Sphere *SphereConfig `yaml:"sphere"`
}

type SphereConfig struct {
	Position []float64 `yaml:"position"`
	Radius   float64   `yaml:"radius"`
}

func main() {
	// Load YAML config
	var scene SceneConfig
	data, err := os.ReadFile("scene.yaml")
	if err != nil {
		panic(fmt.Sprintf("Failed to read scene.yaml: %v", err))
	}
	if err := yaml.Unmarshal(data, &scene); err != nil {
		panic(fmt.Sprintf("Failed to parse YAML: %v", err))
	}

	// Build the camera
	c := core.Camera{
		Width:     scene.Camera.Width,
		Height:    scene.Camera.Height,
		Direction: scene.Camera.Direction,
	}

	// Build objects
	var objects []core.RayMarchableObject
	for _, obj := range scene.Objects {
		if obj.Sphere != nil {
			sphere := core.NewSphere(obj.Sphere.Position, obj.Sphere.Radius)
			objects = append(objects, sphere)
		}
	}

	// Render the scene
	image := c.Render(objects)

	// Save to file
	f, err := os.Create("output.png")
	if err != nil {
		panic(fmt.Sprintf("Failed to create output.png: %v", err))
	}
	defer f.Close()

	if err := png.Encode(f, image); err != nil {
		panic(fmt.Sprintf("Failed to encode PNG: %v", err))
	}

	fmt.Println("Rendered image saved as output.png")
}
```

---

### ✅ Step 3: Create `scene.yaml`

Save this as `scene.yaml` in the same directory:

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

> ✅ Note: The outer `scene:` key is not used in the struct — it's just a YAML root. We're parsing directly into `SceneConfig`, so you can remove `scene:` if you prefer, or keep it for clarity.

---

### 🔧 Optional: Remove `scene:` from YAML

If you want to simplify the YAML (and match the struct exactly), use:

```yaml
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

Then update your `SceneConfig` to remove the outer `scene:` nesting.

---

### ✅ Final Notes

- Make sure your `core` package exports `NewSphere`, `Camera`, and `RayMarchableObject`.
- This design is extensible — you can later add `cube`, `plane`, etc., by adding new types in `ObjectConfig`.
- Add error handling as needed (e.g. validate radius > 0, position length == 3).

Let me know if you want to support multiple object types with polymorphism or more complex materials!