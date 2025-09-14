To refactor the code so that the scene is loaded from a YAML file, we'll use the `gopkg.in/yaml.v3` package (a popular and well-maintained YAML library for Go). We'll define structs that mirror the YAML structure, unmarshal the YAML file, and then use the parsed data to construct the camera and objects for rendering.

Here's the complete refactored code:

---

### ✅ Step 1: Add YAML dependency

First, install the YAML package:

```bash
go get gopkg.in/yaml.v3
```

---

### ✅ Step 2: Refactored Go code (`main.go`)

```go
package main

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
	"github.com/hnatekmarorg/sunshine/core"
	"image/png"
)

// YAMLScene represents the structure of the YAML file
type YAMLScene struct {
	Camera struct {
		Width     int      `yaml:"width"`
		Height    int      `yaml:"height"`
		Direction []float64 `yaml:"direction"`
	} `yaml:"camera"`
	Objects []map[string]any `yaml:"objects"`
}

// SphereConfig represents the configuration for a sphere object
type SphereConfig struct {
	Position []float64 `yaml:"position"`
	Radius   float64   `yaml:"radius"`
}

func main() {
	// Read YAML file
	yamlFile, err := os.ReadFile("scene.yaml")
	if err != nil {
		fmt.Printf("Error reading scene.yaml: %v\n", err)
		return
	}

	var scene YAMLScene
	if err := yaml.Unmarshal(yamlFile, &scene); err != nil {
		fmt.Printf("Error unmarshaling YAML: %v\n", err)
		return
	}

	// Build camera
	camera := core.Camera{
		Width:     scene.Camera.Width,
		Height:    scene.Camera.Height,
		Direction: scene.Camera.Direction,
	}

	// Build ray-marchable objects from YAML
	var objects []core.RayMarchableObject
	for _, obj := range scene.Objects {
		for key, value := range obj {
			switch key {
			case "sphere":
				sphereConfig, ok := value.(map[string]any)
				if !ok {
					fmt.Println("Invalid sphere configuration")
					continue
				}

				position := extractFloat64Slice(sphereConfig["position"])
				radius := extractFloat64(sphereConfig["radius"])

				if len(position) == 3 {
					objects = append(objects, core.NewSphere(position, radius))
				} else {
					fmt.Println("Invalid sphere position")
				}
			default:
				fmt.Printf("Unknown object type: %s\n", key)
			}
		}
	}

	// Render the scene
	image := camera.Render(objects)

	// Save to PNG
	f, err := os.Create("output.png")
	if err != nil {
		fmt.Printf("Error creating output.png: %v\n", err)
		return
	}
	defer f.Close()

	if err := png.Encode(f, image); err != nil {
		fmt.Printf("Error encoding PNG: %v\n", err)
		return
	}

	fmt.Println("Rendered scene saved to output.png")
}

// Helper to extract []float64 from interface{}
func extractFloat64Slice(i any) []float64 {
	if i == nil {
		return nil
	}
	switch v := i.(type) {
	case []interface{}:
		result := make([]float64, len(v))
		for i, val := range v {
			result[i] = extractFloat64(val)
		}
		return result
	case []float64:
		return v
	default:
		return nil
	}
}

// Helper to extract float64 from interface{}
func extractFloat64(i any) float64 {
	if i == nil {
		return 0
	}
	switch v := i.(type) {
	case float64:
		return v
	case float32:
		return float64(v)
	case int:
		return float64(v)
	case int64:
		return float64(v)
	case int32:
		return float64(v)
	case int16:
		return float64(v)
	case int8:
		return float64(v)
	case uint:
		return float64(v)
	case uint64:
		return float64(v)
	case uint32:
		return float64(v)
	case uint16:
		return float64(v)
	case uint8:
		return float64(v)
	default:
		return 0
	}
}
```

---

### ✅ Step 3: Create `scene.yaml`

Save this as `scene.yaml` in the same directory as your Go program:

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

- The code is flexible and can be extended to support other object types (e.g., `cube`, `plane`, etc.) by adding more `case` statements in the object parsing loop.
- The helper functions `extractFloat64Slice` and `extractFloat64` handle the type assertion from `interface{}` (required due to YAML unmarshaling into `any`).
- Error handling is included to make the program robust.
- You can later extend this to support materials, lights, or ambient settings by extending the YAML and struct definitions.

---

### ✅ Run it

```bash
go run main.go
```

You should now see `output.png` generated with your rendered scene!

Let me know if you'd like to support more object types (like cubes or planes) or add lighting/texture support next!