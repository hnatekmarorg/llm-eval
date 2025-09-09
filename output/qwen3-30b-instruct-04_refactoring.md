Here's a refactored version of your Go code that loads the scene from a YAML file instead of hardcoding it. We'll use the `gopkg.in/yaml.v3` package to parse the YAML configuration.

---

### ✅ Updated `main.go`

```go
package main

import (
	"github.com/hnatekmarorg/sunshine/core"
	"gopkg.in/yaml.v3"
	"image/png"
	"os"
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

// ObjectConfig represents a generic object in the scene
type ObjectConfig struct {
	Sphere *SphereConfig `yaml:"sphere"`
}

// SphereConfig represents a sphere object
type SphereConfig struct {
	Position []float64 `yaml:"position"`
	Radius   float64   `yaml:"radius"`
}

func main() {
	// Load YAML config
	data, err := os.ReadFile("scene.yaml")
	if err != nil {
		panic(err)
	}

	var config SceneConfig
	err = yaml.Unmarshal(data, &config)
	if err != nil {
		panic(err)
	}

	// Create camera
	c := core.Camera{
		Width:     config.Camera.Width,
		Height:    config.Camera.Height,
		Direction: config.Camera.Direction,
	}

	// Convert objects
	var objects []core.RayMarchableObject
	for _, obj := range config.Objects {
		if obj.Sphere != nil {
			objects = append(objects, core.NewSphere(obj.Sphere.Position, obj.Sphere.Radius))
		}
		// Add other object types (e.g. plane, box) here if needed
	}

	// Render scene
	image := c.Render(objects)

	// Save image
	f, err := os.Create("output.png")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	err = png.Encode(f, image)
	if err != nil {
		panic(err)
	}

	println("Image saved as output.png")
}
```

---

### ✅ Example `scene.yaml`

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

> 💡 Note: The `scene:` root key is optional. If you remove it, the YAML should still parse correctly as long as the structure matches the `SceneConfig` struct. For cleaner parsing, you can also just define the config at the root level.

---

### ✅ Optional: Remove `scene:` root key in YAML

If you prefer to keep it flat:

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

Then update `SceneConfig` to remove the `scene:` wrapper:

```go
type SceneConfig struct {
	Camera  struct { ... } `yaml:"camera"`
	Objects []ObjectConfig `yaml:"objects"`
}
```

---

### 📦 Dependencies

Make sure you have the YAML package installed:

```bash
go get gopkg.in/yaml.v3
```

---

### ✅ Summary

- ✅ Scene is now loaded from `scene.yaml`
- ✅ Configurable camera and objects
- ✅ Extensible for more object types (add `Plane`, `Box`, etc.)
- ✅ Clean separation of concerns

Let me know if you'd like to support multiple object types (e.g. planes, boxes) or lighting!