To refactor the provided Go code to load the scene configuration from a YAML file, we'll make the following changes:
1. Add YAML parsing capability using `gopkg.in/yaml.v3`
2. Define structures to match the expected YAML format
3. Replace hardcoded scene elements with YAML-loaded values
4. Implement proper error handling

Here's the refactored code:

```go
package main

import (
	"log"
	"os"

	"gopkg.in/yaml.v3"
	"github.com/hnatekmarorg/sunshine/core"
	"image/png"
)

func main() {
	// Read YAML configuration file
	yamlFile, err := os.Open("scene.yaml")
	if err != nil {
		log.Fatalf("Failed to open scene.yaml: %v", err)
	}
	defer yamlFile.Close()

	// Define structures matching YAML format
	type ObjectConfig struct {
		Sphere struct {
			Position []float64 `yaml:"position"`
			Radius   float64   `yaml:"radius"`
		} `yaml:"sphere"`
	}
	
	type CameraConfig struct {
		Width     int       `yaml:"width"`
		Height    int       `yaml:"height"`
		Direction []float64 `yaml:"direction"`
	}
	
	type SceneConfig struct {
		Camera  CameraConfig    `yaml:"camera"`
		Objects []ObjectConfig  `yaml:"objects"`
	}
	
	type Config struct {
		Scene SceneConfig `yaml:"scene"`
	}

	// Parse YAML into structures
	var config Config
	decoder := yaml.NewDecoder(yamlFile)
	if err := decoder.Decode(&config); err != nil {
		log.Fatalf("Failed to parse YAML: %v", err)
	}

	// Create camera from YAML configuration
	c := core.Camera{
		Width:     config.Scene.Camera.Width,
		Height:    config.Scene.Camera.Height,
		Direction: config.Scene.Camera.Direction,
	}

	// Build objects from YAML configuration
	var objects []core.RayMarchableObject
	for _, obj := range config.Scene.Objects {
		objects = append(objects, core.NewSphere(obj.Sphere.Position, obj.Sphere.Radius))
	}

	// Render and save image
	image := c.Render(objects)
	outFile, err := os.Create("output.png")
	if err != nil {
		log.Fatalf("Failed to create output file: %v", err)
	}
	defer outFile.Close()
	
	if err := png.Encode(outFile, image); err != nil {
		log.Fatalf("Failed to encode PNG: %v", err)
	}
}
```

Key improvements made:
1. **YAML Structure Matching**: 
   - Created nested structs that directly mirror the YAML structure
   - Used explicit field tags (`yaml:"..."`) for precise mapping
   - Handles the `scene` top-level key as specified in the example

2. **Type Safety**:
   - Directly unmarshals into typed structures instead of using interface{}
   - Eliminates type assertions and manual conversions
   - Preserves strong typing throughout the code

3. **Error Handling**:
   - Added proper error checks for file operations
   - Detailed error messages with context
   - Graceful failure on invalid configuration

4. **Maintainability**:
   - Clear separation between configuration loading and rendering logic
   - Structured data flow from YAML → structs → rendering objects
   - Easy to extend for new object types (add new struct fields)

Example `scene.yaml` that works with this code:
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

This implementation:
- Loads camera configuration directly from YAML
- Converts sphere definitions into rendering objects
- Maintains all original rendering functionality
- Handles errors gracefully with descriptive messages
- Follows Go best practices for configuration loading
- Keeps the code clean and maintainable for future extensions

Note: You'll need to install the YAML package with:
```bash
go get gopkg.in/yaml.v3
```