Here's a refactored version of your Go program that loads the scene from a YAML file instead of hardcoding it. We'll use the `gopkg.in/yaml.v3` package to parse the YAML configuration.

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
	Objects []yaml.Node `yaml:"objects"`
}

func main() {
	// Load YAML file
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

	// Parse objects
	var objects []core.RayMarchableObject
	for _, objNode := range config.Objects {
		var objMap map[string]yaml.Node
		if err := objNode.Decode(&objMap); err != nil {
			panic(err)
		}

		for objType, node := range objMap {
			switch objType {
			case "sphere":
				var sphereData struct {
					Position []float64 `yaml:"position"`
					Radius   float64   `yaml:"radius"`
				}
				if err := node.Decode(&sphereData); err != nil {
					panic(err)
				}
				objects = append(objects, core.NewSphere(sphereData.Position, sphereData.Radius))
			default:
				panic("unknown object type: " + objType)
			}
		}
	}

	// Render scene
	image := c.Render(objects)

	// Save image
	f, err := os.Create("output.png")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	if err := png.Encode(f, image); err != nil {
		panic(err)
	}

	println("Rendered image saved to output.png")
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

### ✅ Required Dependencies

Make sure you have the YAML parser installed:

```bash
go get gopkg.in/yaml.v3
```

---

### ✅ Notes

- This assumes `core.NewSphere` takes `[]float64` and `float64` as arguments.
- The `yaml.Node` approach allows us to handle dynamic object types (e.g., `sphere`, `plane`, etc.) in the future.
- You can easily extend this to support more shapes (like planes, boxes) by adding more `case` blocks.

---

Let me know if you'd like to support more object types or use a different structure (e.g., `type: sphere`, `params: {...}`) for cleaner parsing!