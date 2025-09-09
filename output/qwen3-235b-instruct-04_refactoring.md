To refactor the Go code so that the scene is loaded from a YAML file, we'll need to:

1. Define structs that match the YAML structure.
2. Read and parse the YAML file using the `gopkg.in/yaml.v3` package.
3. Construct the scene (camera and objects) based on the parsed data.

Here’s how you can do it:

---

### ✅ Step 1: Install the YAML package

```bash
go get gopkg.in/yaml.v3
```

---

### ✅ Step 2: Refactored `main.go`

```go
package main

import (
	"gopkg.in/yaml.v3"
	"image/png"
	"os"

	"github.com/hnatekmarorg/sunshine/core"
)

// Define structs to match the YAML structure
type YAMLVector []float64

type YAMLSphere struct {
	Position []float64 `yaml:"position"`
	Radius   float64   `yaml:"radius"`
}

type YAMLObject struct {
	Sphere *YAMLSphere `yaml:"sphere,omitempty"`
}

type YAMLCamera struct {
	Width     int         `yaml:"width"`
	Height    int         `yaml:"height"`
	Direction YAMLVector  `yaml:"direction"`
}

type YAMLScene struct {
	Camera  YAMLCamera     `yaml:"camera"`
	Objects []YAMLObject   `yaml:"objects"`
}

func loadSceneFromFile(path string) (*YAMLScene, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var scene YAMLScene
	err = yaml.Unmarshal(data, &scene)
	if err != nil {
		return nil, err
	}

	return &scene, nil
}

func main() {
	// Load scene from YAML file (e.g., scene.yaml)
	scene, err := loadSceneFromFile("scene.yaml")
	if err != nil {
		panic(err)
	}

	// Create camera
	camera := core.Camera{
		Width:     scene.Camera.Width,
		Height:    scene.Camera.Height,
		Direction: scene.Camera.Direction,
	}

	// Convert YAML objects to RayMarchableObjects
	var objects []core.RayMarchableObject
	for _, obj := range scene.Objects {
		if obj.Sphere != nil {
			sphere := core.NewSphere(obj.Sphere.Position, obj.Sphere.Radius)
			objects = append(objects, sphere)
		}
		// You can add more object types here (plane, box, etc.)
	}

	// Render the image
	image := camera.Render(objects)

	// Save to output.png
	f, err := os.Create("output.png")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	err = png.Encode(f, image)
	if err != nil {
		panic(err)
	}
}
```

---

### ✅ Step 3: Create `scene.yaml`

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

> ❗ Note: The top-level key `scene` isn't actually used in the struct unmarshaling unless you nest it. Since we're unmarshaling directly into `YAMLScene`, the YAML should **not** have a top-level `scene:` key.

So, fix the YAML by **removing the outer `scene:` key**:

### ✅ Correct `scene.yaml` (no top-level mapping):

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

---

### ✅ Final Notes

- You can extend the `YAMLObject` struct to support other shapes using YAML polymorphism (e.g., `type: sphere`, `type: plane`).
- Consider adding error handling for invalid or missing fields.
- You might want to add a CLI flag to specify the scene file path.

---

This refactoring makes your ray tracer **data-driven** — you can now create multiple scenes just by writing new YAML files! 🎉