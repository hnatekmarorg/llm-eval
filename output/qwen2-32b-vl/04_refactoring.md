To refactor the code so that the scene is loaded from a YAML file, we need to parse the YAML configuration and extract the necessary information to initialize the camera and objects. Below is the refactored version of the code:

### Refactored Code

```go
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/hnatekmarorg/sunshine/core"
	"gopkg.in/yaml.v3"
	"image/png"
	"os"
)

// Scene struct to hold the YAML configuration
type Scene struct {
	Camera struct {
		Width     int     `yaml:"width"`
		Height    int     `yaml:"height"`
		Direction []float64 `yaml:"direction"`
	} `yaml:"camera"`
	Objects []Object `yaml:"objects"`
}

// Object interface to represent different 3D objects
type Object interface {
	core.RayMarchableObject
}

// SphereConfig struct to represent a sphere object in the YAML
type SphereConfig struct {
	Position []float64 `yaml:"position"`
	Radius   float64   `yaml:"radius"`
}

// ConvertSphere converts SphereConfig to a core.Sphere
func (s *SphereConfig) ConvertSphere() core.Sphere {
	return core.NewSphere(s.Position, s.Radius)
}

// ParseScene parses the YAML file and returns a Scene struct
func ParseScene(filename string) (*Scene, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to read YAML file: %w", err)
	}

	scene := &Scene{}
	err = yaml.Unmarshal(data, scene)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal YAML: %w", err)
	}

	return scene, nil
}

// ConvertObjects converts the objects in the Scene to a slice of core.RayMarchableObject
func ConvertObjects(objects []Object) []core.RayMarchableObject {
	result := make([]core.RayMarchableObject, 0, len(objects))
	for _, obj := range objects {
		result = append(result, obj.(core.RayMarchableObject))
	}
	return result
}

func main() {
	// Step 1: Load the YAML scene file
	sceneFile := "scene.yaml"
	scene, err := ParseScene(sceneFile)
	if err != nil {
		fmt.Println("Error parsing scene:", err)
		return
	}

	// Step 2: Extract camera parameters
	c := core.Camera{
		Width:     scene.Camera.Width,
		Height:    scene.Camera.Height,
		Direction: scene.Camera.Direction,
	}

	// Step 3: Convert YAML objects to core.RayMarchableObject
	var objects []core.RayMarchableObject
	for _, obj := range scene.Objects {
		switch obj := obj.(type) {
		case *SphereConfig:
			objects = append(objects, obj.ConvertSphere())
		default:
			fmt.Printf("Unknown object type: %T\n", obj)
		}
	}

	// Step 4: Render the scene
	image := c.Render(objects)

	// Step 5: Save the image to a file
	f, err := os.Create("output.png")
	if err != nil {
		fmt.Println("Error creating output file:", err)
		return
	}
	defer f.Close()

	if err := png.Encode(f, image); err != nil {
		fmt.Println("Error encoding PNG:", err)
		return
	}

	fmt.Println("Rendering complete. Image saved as output.png")
}
```

### Explanation of Changes

1. **Scene Struct**:
   - A `Scene` struct is defined to hold the YAML configuration. It includes fields for the camera and objects.
   - The `Objects` field is a slice of `Object`, which is an interface for 3D objects.

2. **Object Interface**:
   - An `Object` interface is defined to represent different 3D objects. In this case, we only support spheres, but this can be extended to other objects like cubes, etc.

3. **SphereConfig**:
   - A `SphereConfig` struct is defined to hold the YAML representation of a sphere. It includes `Position` and `Radius`.

4. **ParseScene Function**:
   - The `ParseScene` function reads the YAML file, unmarshals it into the `Scene` struct, and returns the parsed scene.

5. **ConvertSphere Method**:
   - The `ConvertSphere` method converts a `SphereConfig` to a `core.Sphere` object by calling `core.NewSphere`.

6. **ConvertObjects Function**:
   - The `ConvertObjects` function iterates over the objects in the scene and converts them to `core.RayMarchableObject`.

7. **Main Logic**:
   - The `main` function loads the YAML file, extracts the camera parameters and objects, renders the scene, and saves the output as a PNG file.

### Example YAML File (`scene.yaml`)

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

### Key Points

- **YAML Parsing**: The `gopkg.in/yaml.v3` library is used to parse the YAML file.
- **Dynamic Object Handling**: The `Object` interface allows for easy extension to support different 3D objects.
- **Error Handling**: Errors are propagated and handled gracefully.

This refactoring makes the code more modular, maintainable, and extensible. The scene configuration can now be easily modified by editing the YAML file without changing the Go code.