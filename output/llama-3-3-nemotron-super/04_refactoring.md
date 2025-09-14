

To refactor the provided Go code to load the scene configuration from a YAML file, we need to define a structured way to parse and interpret the YAML data into the appropriate Go structs. This involves:

- Defining a `Scene` structure that matches the YAML layout.
- Parsing the YAML file into this structure.
- Converting the parsed data into the corresponding `core.Camera` and `core.RayMarchableObject` instances.
- Rendering the scene and saving the output as a PNG image.

---

### ✅ YAML Structure

The YAML file should follow this format:

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

This structure allows for easy extension to support other types of objects (e.g., planes, boxes) in the future.

---

### 📦 Go Implementation

Here is the complete refactored Go code that reads the scene from a YAML file and renders it:

```go
package main

import (
	"log"
	"os"

	"gopkg.in/yaml.v3"

	"github.com/hnatekmarorg/sunshine/core"
	_ "image/png" // Required for png.Encode
)

// Structs for YAML parsing
type CameraConfig struct {
	Width     int       `yaml:"width"`
	Height    int       `yaml:"height"`
	Direction []float64 `yaml:"direction"`
}

type Scene struct {
	Camera   CameraConfig `yaml:"camera"`
	Objects  []map[string]interface{} `yaml:"objects"`
}

func main() {
	// Load and parse YAML file
	yamlData, err := os.ReadFile("scene.yaml")
	if err != nil {
		log.Fatalf("Error reading YAML file: %v", err)
	}

	var scene Scene
	err = yaml.Unmarshal(yamlData, &scene)
	if err != nil {
		log.Fatalf("Error unmarshaling YAML: %v", err)
	}

	// Create the camera
	camera := core.Camera{
		Width:     scene.Camera.Width,
		Height:    scene.Camera.Height,
		Direction: scene.Camera.Direction,
	}

	// Parse and create objects
	var objects []core.RayMarchableObject
	for _, obj := range scene.Objects {
		for objType, config := range obj {
			switch objType {
			case "sphere":
				configMap, ok := config.(map[string]interface{})
				if !ok {
					log.Fatal("Invalid sphere configuration")
				}

				// Parse position
				position, ok := configMap["position"].([]interface{})
				if !ok {
					log.Fatal("Position not found or invalid type")
				}
				pos := make([]float64, len(position))
				for i, v := range position {
					pos[i] = v.(float64)
				}

				// Parse radius
				radius, ok := configMap["radius"].(float64)
				if !ok {
					log.Fatal("Radius not found or invalid type")
				}

				objects = append(objects, core.NewSphere(pos, radius))

			default:
				log.Fatalf("Unknown object type: %s", objType)
			}
		}
	}

	// Render the scene
	image := camera.Render(objects)

	// Save the result to a PNG file
	file, err := os.Create("output.png")
	if err != nil {
		log.Fatalf("Error creating output file: %v", err)
	}
	defer file.Close()

	err = png.Encode(file, image)
	if err != nil {
		log.Fatalf("Error encoding PNG: %v", err)
	}
}
```

---

### 🧪 Example YAML File (`scene.yaml`)

Save the following as `scene.yaml` in the same directory as your Go code:

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

### 📌 Notes

- This implementation uses the `gopkg.in/yaml.v3` library for parsing YAML. Make sure to install it:

  ```bash
  go get gopkg.in/yaml.v3
  ```

- The code assumes the `core` package provides the `Camera` and `RayMarchableObject` types, including the `NewSphere` constructor.
- The error handling is minimal for brevity but can be expanded for production use.
- This structure is easily extensible to support other object types (e.g., planes, boxes, etc.) by adding more `case` blocks in the `switch objType` section.

---

### ✅ Summary

This refactoring allows the scene configuration to be defined externally in a YAML file, making it easier to modify and extend without changing the Go code. The code reads the YAML, constructs the camera and objects, and renders the scene as before.