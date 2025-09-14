

To refactor the given Go code so that it reads the scene configuration from a YAML file, we follow a structured approach to:

1. Define a `Scene` struct to represent the YAML structure.
2. Parse the YAML file using `gopkg.in/yaml.v2`.
3. Extract the camera configuration.
4. Parse each object from the YAML and create the corresponding `RayMarchableObject` (in this case, spheres).
5. Render the scene and save the image to a PNG file.

---

### ✅ Final Refactored Code

```go
package main

import (
	"gopkg.in/yaml.v2"
	"github.com/hnatekmarorg/sunshine/core"
	"image/png"
	"os"
)

// Scene struct represents the structure of the YAML file.
type Scene struct {
	Camera  core.Camera
	Objects []map[string]interface{}
}

func main() {
	// Open the YAML configuration file.
	file, err := os.Open("config.yaml")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// Parse the YAML content into the Scene struct.
	var scene Scene
	if err := yaml.NewDecoder(file).Decode(&scene); err != nil {
		panic(err)
	}

	// Create the camera from the parsed configuration.
	camera := core.Camera{
		Width:     scene.Camera.Width,
		Height:    scene.Camera.Height,
		Direction: scene.Camera.Direction,
	}

	// Create the list of objects from the YAML.
	objects := make([]core.RayMarchableObject, 0)
	for _, obj := range scene.Objects {
		if sphere, ok := obj["sphere"].(map[string]interface{}); ok {
			// Extract position and radius from the sphere configuration.
			positions := sphere["position"].([]float64)
			radius := sphere["radius"].(float64)

			// Create the sphere and add it to the objects list.
			objects = append(objects, core.NewSphere(positions, radius))
		}
	}

	// Render the scene.
	image := camera.Render(objects)

	// Save the rendered image as a PNG file.
	outputFile, _ := os.Create("output.png")
	defer outputFile.Close()
	png.Encode(outputFile, image)
}
```

---

### 📁 Sample YAML Configuration (`config.yaml`)

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

### 🧠 Key Notes

- The `Scene` struct is designed to match the structure of the YAML file.
- We use `yaml.v2` to decode the YAML content into a Go struct.
- The code assumes all objects are spheres (`core.NewSphere`), but the design allows for adding more object types in the future.
- Error handling is simplified using `panic` for demonstration clarity; in production, you'd want to handle these more gracefully.

---

### ✅ Summary

This refactoring allows the scene configuration to be externalized into a YAML file, making it more flexible and easier to maintain. The code remains idiomatic Go and uses the same core rendering logic but now reads the scene data from an external file.