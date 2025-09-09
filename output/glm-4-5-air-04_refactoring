To refactor the code so that the scene is loaded from a YAML file, we'll need to:
1. Define Go structs to match the YAML structure
2. Read and parse the YAML file
3. Convert YAML objects into the `RayMarchableObject` interface

Here's the refactored implementation:

```go
package main

import (
	"fmt"
	"os"
	"github.com/hnatekmarorg/sunshine/core"
	"image/png"
	"gopkg.in/yaml.v3"
)

// YAML structures matching the scene definition
type Scene struct {
	Camera struct {
		Width     int       `yaml:"width"`
		Height    int       `yaml:"height"`
		Direction [3]float64 `yaml:"direction"`
	} `yaml:"camera"`
	Objects []struct {
		Sphere struct {
			Position [3]float64 `yaml:"position"`
			Radius   float64    `yaml:"radius"`
		} `yaml:"sphere"`
	} `yaml:"objects"`
}

func main() {
	// Read YAML file
	yamlData, err := os.ReadFile("scene.yaml")
	if err != nil {
		fmt.Printf("Error reading YAML file: %v\n", err)
		os.Exit(1)
	}

	// Parse YAML
	var yamlScene Scene
	err = yaml.Unmarshal(yamlData, &yamlScene)
	if err != nil {
		fmt.Printf("Error parsing YAML: %v\n", err)
		os.Exit(1)
	}

	// Create camera from YAML
	camera := core.Camera{
		Width:     yamlScene.Camera.Width,
		Height:    yamlScene.Camera.Height,
		Direction: yamlScene.Camera.Direction,
	}

	// Convert YAML objects to RayMarchableObjects
	objects := make([]core.RayMarchableObject, 0, len(yamlScene.Objects))
	for _, objYAML := range yamlScene.Objects {
		objects = append(objects, core.NewSphere(objYAML.Sphere.Position, objYAML.Sphere.Radius))
	}

	// Render and save image
	image := camera.Render(objects)
	file, err := os.Create("output.png")
	if err != nil {
		fmt.Printf("Error creating output file: %v\n", err)
		os.Exit(1)
	}
	defer file.Close()

	err = png.Encode(file, image)
	if err != nil {
		fmt.Printf("Error encoding PNG: %v\n", err)
		os.Exit(1)
	}
}
```

**Key changes:**
1. Added YAML-compatible structs (`Scene`, nested `Camera` and `Objects` types)
2. Reader/parser logic to load `scene.yaml`
3. Conversion from YAML data to `core.RayMarchableObject` slices
4. Maintained the original rendering and image saving functionality

**Required YAML file (`scene.yaml`):**
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

**To use:**
1. Save the Go code with this refactored `main`
2. Create `scene.yaml` with your scene definition
3. Ensure required packages are installed:
   ```bash
   go get github.com/hnatekmarorg/sunshine/core
   go get gopkg.in/yaml.v3
   ```
4. Run the program:
   ```bash
   go run main.go
   ```
   This will generate `output.png` using the scene defined in the YAML file.

**Notes:**
- The YAML parser expects exact field names matching the Go struct tags
- Position is represented as an array of 3 floats in YAML
- Error handling has been added for file operations and unmarshaling
- The conversion assumes only sphere objects are present (extend with additional types as needed)