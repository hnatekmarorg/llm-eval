To refactor the Go code so that the scene is loaded from a YAML file, we'll need to:

1. Define structs that map to the YAML structure.
2. Use a YAML parser (e.g., `gopkg.in/yaml.v3`).
3. Read and parse the YAML file.
4. Construct the scene accordingly.

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
	"image"
	"image/png"
	"os"

	"github.com/hnatekmarorg/sunshine/core"
)

// Define structs to match the YAML structure
type Config struct {
	Scene SceneConfig `yaml:"scene"`
}

type SceneConfig struct {
	Camera  CameraConfig           `yaml:"camera"`
	Objects []map[string]ObjectCfg `yaml:"objects"`
}

type CameraConfig struct {
	Width     int       `yaml:"width"`
	Height    int       `yaml:"height"`
	Direction []float64 `yaml:"direction"`
}

type ObjectCfg struct {
	Position []float64 `yaml:"position"`
	Radius   float64   `yaml:"radius"`
}

func main() {
	// Read YAML config file
	data, err := os.ReadFile("scene.yaml")
	if err != nil {
		panic(err)
	}

	var config Config
	err = yaml.Unmarshal(data, &config)
	if err != nil {
		panic(err)
	}

	// Create camera
	cam := core.Camera{
		Width:     config.Scene.Camera.Width,
		Height:    config.Scene.Camera.Height,
		Direction: config.Scene.Camera.Direction,
	}

	// Build list of ray-marchable objects
	var objects []core.RayMarchableObject
	for _, obj := range config.Scene.Objects {
		if sphere, exists := obj["sphere"]; exists {
			sphereObj := core.NewSphere(sphere.Position, sphere.Radius)
			objects = append(objects, sphereObj)
		}
		// You can add more object types here (e.g., "box", "plane", etc.)
	}

	// Render the scene
	img := cam.Render(objects)

	// Save image
	f, err := os.Create("output.png")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	err = png.Encode(f, img)
	if err != nil {
		panic(err)
	}
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

---

### ✅ Notes

- This approach is extensible: you can later add other object types (like `box`, `plane`) by checking for their keys in the `objects` list.
- Ensure that the `core.NewSphere` function takes `[]float64` for position and `float64` for radius, as assumed here.
- You may want to add error handling for missing fields in production.

---

Now you can run:

```bash
go run main.go
```

And it will render the scene defined in `scene.yaml`. ✅