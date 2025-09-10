
<answer>
To refactor the code to load the scene from a YAML file, follow these steps:

### Step 1: Define YAML Configuration Structs
Create structs that mirror the YAML structure to parse the configuration.

### Step 2: Read and Parse YAML
Use a YAML decoder to load and unmarshal the configuration into the defined structs.

### Step 3: Convert Config to Rendering Objects
Transform the parsed configuration into the rendering structures (`core.Camera` and `[]core.RayMarchableObject`).

### Refactored Code
```go
package main

import (
	"image/png"
	"log"
	"os"

	"gopkg.in/yaml.v3"
	"github.com/hnatekmarorg/sunshine/core"
)

// SceneConfig represents the YAML structure for the scene configuration.
type SceneConfig struct {
	Camera  CameraConfig  `yaml:"camera"`
	Objects []ObjectConfig `yaml:"objects"`
}

// CameraConfig holds camera parameters from YAML.
type CameraConfig struct {
	Width     int      `yaml:"width"`
	Height    int      `yaml:"height"`
	Direction []float64 `yaml:"direction"`
}

// ObjectConfig holds object parameters from YAML.
type ObjectConfig struct {
	Sphere SphereConfig `yaml:"sphere"`
}

// SphereConfig holds sphere parameters from YAML.
type SphereConfig struct {
	Position []float64 `yaml:"position"`
	Radius   float64   `yaml:"radius"`
}

func main() {
	// Load and parse YAML configuration
	configFile, err := os.Open("scene.yaml")
	if err != nil {
		log.Fatalf("Failed to open config file: %v", err)
	}
	defer configFile.Close()

	var sceneConfig SceneConfig
	decoder := yaml.NewDecoder(configFile)
	if err := decoder.Decode(&sceneConfig); err != nil {
		log.Fatalf("Failed to decode YAML: %v", err)
	}

	// Create camera from configuration
	camera := core.Camera{
		Width:     sceneConfig.Camera.Width,
		Height:    sceneConfig.Camera.Height,
		Direction: sceneConfig.Camera.Direction,
	}

	// Create renderable objects from configuration
	var objects []core.RayMarchableObject
	for _, objConfig := range sceneConfig.Objects {
		sphere := core.NewSphere(objConfig.Sphere.Position, objConfig.Sphere.Radius)
		objects = append(objects, sphere)
	}

	// Render the scene
	image := camera.Render(objects)

	// Save the rendered image to PNG
	outputFile, err := os.Create("output.png")
	if err != nil {
		log.Fatalf("Failed to create output file: %v", err)
	}
	defer outputFile.Close()

	if err := png.Encode(outputFile, image); err != nil {
		log.Fatalf("Failed to encode image to PNG: %v", err)
	}
}
```

### Explanation
1. **YAML Structs**: `SceneConfig`, `CameraConfig`, `ObjectConfig`, and `SphereConfig` are defined to match the YAML structure. These structs use YAML tags to map field names.
2. **Reading YAML**: The code opens `scene.yaml`, decodes it using `yaml.NewDecoder`, and unmarshals the data into `SceneConfig`.
3. **Object Creation**: The camera is created directly from `SceneConfig.Camera`. Objects are created by iterating over `SceneConfig.Objects`, converting each `SphereConfig` to a `core.Sphere`.
4. **Rendering and Saving**: The scene is rendered using the configured camera and objects, then saved to `output.png`.

### Example `scene.yaml`
Create a `scene.yaml` file with your desired configuration:
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

### Dependencies
Ensure you have the YAML package installed:
```bash
go get gopkg.in/yaml.v3
```

This refactored code separates configuration (YAML) from rendering logic, making it easier to modify the scene without changing the code.
</answer>