

To refactor the original Go program so that the scene is loaded from a YAML file, we need to:

1. **Define a YAML structure** that mirrors the hard-coded scene configuration.
2. **Create Go structs** to unmarshal the YAML into.
3. **Parse the YAML file** and construct the scene.
4. **Convert the YAML data** into the appropriate `core.Camera` and `core.RayMarchableObject` types.
5. **Render the scene** and save the output as a PNG image.

---

### ✅ YAML Structure

The YAML file should look like this:

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

### 📦 Go Struct Definitions

We define structs to represent the YAML structure:

```go
type Camera struct {
    Width    int       `yaml:"width"`
    Height   int       `yaml:"height"`
    Direction []float64 `yaml:"direction"`
}

type Scene struct {
    Camera  Camera  `yaml:"camera"`
    Objects []map[string]interface{} `yaml:"objects"`
}
```

The `Objects` field is a slice of maps, where each map has one key (e.g., `"sphere"`) and a value that is another map of object properties.

---

### 🧱 Object Parsing Logic

We'll loop through each object in the scene and parse it based on its type. For now, we only support `"sphere"`.

```go
for _, obj := range scene.Objects {
    for objType, objParams := range obj {
        switch objType {
        case "sphere":
            params := objParams.(map[string]interface{})
            positionRaw := params["position"].([]interface{})
            position := make([]float64, len(positionRaw))
            for i, v := range positionRaw {
                position[i] = v.(float64)
            }
            radius := params["radius"].(float64)
            rayObjects = append(rayObjects, core.NewSphere(position, radius))
        default:
            panic("unsupported object type: " + objType)
        }
    }
}
```

---

### 🧾 Full Refactored Code

Here is the complete refactored version of the program:

```go
package main

import (
    "image/png"
    "os"

    "github.com/hnatekmarorg/sunshine/core"
    "gopkg.in/yaml.v3"
)

// Structs for YAML unmarshaling
type Camera struct {
    Width    int       `yaml:"width"`
    Height   int       `yaml:"height"`
    Direction []float64 `yaml:"direction"`
}

type Scene struct {
    Camera  Camera  `yaml:"camera"`
    Objects []map[string]interface{} `yaml:"objects"`
}

func main() {
    // Load YAML scene file
    yamlData, err := os.ReadFile("scene.yaml")
	if err != nil {
		panic(err)
	}

	var scene Scene
	err = yaml.Unmarshal(yamlData, &scene)
	if err != nil {
		panic(err)
	}

	// Create camera
	c := core.Camera{
		Width:     scene.Camera.Width,
		Height:    scene.Camera.Height,
		Direction: scene.Camera.Direction,
	}

	// Parse objects from YAML
	var rayObjects []core.RayMarchableObject
	for _, obj := range scene.Objects {
		for objType, objParams := range obj {
			switch objType {
			case "sphere":
				params := objParams.(map[string]interface{})
				positionRaw := params["position"].([]interface{})
				position := make([]float64, len(positionRaw))
				for i, v := range positionRaw {
					position[i] = v.(float64)
				}
				radius := params["radius"].(float64)
				rayObjects = append(rayObjects, core.NewSphere(position, radius))
			default:
				panic("unsupported object type: " + objType)
			}
		}
	}

	// Render the scene
	image := c.Render(rayObjects)

	// Save to PNG
	f, err := os.Create("output.png")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	err = png.Encode(f, image)
	if err != nil {
		panic(err)
	}
}
```

---

### 📌 Notes

- **Error Handling**: The code uses `panic` for simplicity. In production, consider using proper error handling with `log.Fatal`, `errors.Wrap`, or returning errors.
- **Extensibility**: This structure is easy to extend to support more object types (e.g., planes, boxes) by adding more cases to the `switch` statement.
- **YAML Package**: This example uses the popular `gopkg.in/yaml.v3` package. Make sure to install it:

```bash
go get gopkg.in/yaml.v3
```

---

### 🧪 Example Output

Running this code with the provided YAML file will generate an image file `output.png` containing the rendered scene with four spheres.

---

### ✅ Summary

This refactoring moves the scene configuration from hard-coded values to a flexible YAML file, making it easy to modify the scene without changing the code. The program now reads the scene from `scene.yaml`, constructs the camera and objects accordingly, and renders the image as before.