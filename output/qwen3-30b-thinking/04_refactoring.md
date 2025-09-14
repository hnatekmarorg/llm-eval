To refactor the code to load the scene from a YAML file, we'll define the necessary structs to represent the scene configuration, use the `yaml.v3` package for parsing, and update the main function to read and process the YAML file. Here's the complete solution:

```go
package main

import (
	"github.com/hnatekmarorg/sunshine/core"
	"gopkg.in/yaml.v3"
	"image/png"
	"os"
)

type SceneConfig struct {
	Camera  CameraConfig  `yaml:"camera"`
	Objects []ObjectConfig `yaml:"objects"`
}

type CameraConfig struct {
	Width     int      `yaml:"width"`
	Height    int      `yaml:"height"`
	Direction []float64 `yaml:"direction"`
}

type ObjectConfig struct {
	Sphere SphereConfig `yaml:"sphere"`
}

type SphereConfig struct {
	Position []float64 `yaml:"position"`
	Radius   float64   `yaml:"radius"`
}

func main() {
	// Read YAML configuration file
	data, err := os.ReadFile("scene.yaml")
	if err != nil {
		panic(err)
	}

	var config SceneConfig
	if err := yaml.Unmarshal(data, &config); err != nil {
		panic(err)
	}

	// Configure camera
	c := core.Camera{
		Width:     config.Camera.Width,
		Height:    config.Camera.Height,
		Direction: config.Camera.Direction,
	}

	// Configure scene objects
	var objects []core.RayMarchableObject
	for _, obj := range config.Objects {
		objects = append(objects, core.NewSphere(obj.Sphere.Position, obj.Sphere.Radius))
	}

	// Render scene
	image := c.Render(objects)

	// Save output image
	f, err := os.Create("output.png")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	if err := png.Encode(f, image); err != nil {
		panic(err)
	}
}
```

**Key changes made:**

1. **Added YAML configuration structs:**
   - `SceneConfig`: Top-level scene structure
   - `CameraConfig`: Camera parameters
   - `ObjectConfig`: Object configuration (with sphere-specific fields)
   - `SphereConfig`: Sphere parameters

2. **Updated main function:**
   - Reads `scene.yaml` file
   - Unmarshals YAML into configuration structs
   - Configures camera using parsed values
   - Converts YAML object definitions to ray marchable objects
   - Renders and saves the image

3. **Error handling:**
   - Added proper error checking for file operations
   - Added error handling for YAML unmarshaling
   - Used `panic` for simplicity (in real applications, consider proper error handling)

**Example `scene.yaml` file:**
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

**To use this solution:**
1. Save the code as `main.go`
2. Create a `scene.yaml` file with your scene configuration
3. Run the program: `go run main.go`

**Note:** This solution requires the `gopkg.in/yaml.v3` package. Install it with:
```bash
go get gopkg.in/yaml.v3
```

The refactored code now:
- Separates scene configuration from code
- Makes scene definitions easily modifiable without recompiling
- Follows the specified YAML structure
- Maintains the same rendering functionality
- Includes proper error handling for critical operations