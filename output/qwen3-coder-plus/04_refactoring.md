Here's the refactored code that loads the scene from a YAML file:

```go
package main

import (
	"gopkg.in/yaml.v2"
	"github.com/hnatekmarorg/sunshine/core"
	"image/png"
	"os"
)

type SceneConfig struct {
	Camera struct {
		Width     int     `yaml:"width"`
		Height    int     `yaml:"height"`
		Direction []float64 `yaml:"direction"`
	} `yaml:"camera"`
	Objects []ObjectConfig `yaml:"objects"`
}

type ObjectConfig struct {
	Sphere struct {
		Position []float64 `yaml:"position"`
		Radius   float64   `yaml:"radius"`
	} `yaml:"sphere"`
}

func loadScene(filename string) (*SceneConfig, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var config SceneConfig
	decoder := yaml.NewDecoder(file)
	err = decoder.Decode(&config)
	if err != nil {
		return nil, err
	}

	return &config, nil
}

func main() {
	config, err := loadScene("scene.yaml")
	if err != nil {
		panic(err)
	}

	c := core.Camera{
		Width:     config.Camera.Width,
		Height:    config.Camera.Height,
		Direction: config.Camera.Direction,
	}

	var objects []core.RayMarchableObject
	for _, obj := range config.Objects {
		sphere := core.NewSphere(obj.Sphere.Position, obj.Sphere.Radius)
		objects = append(objects, sphere)
	}

	image := c.Render(objects)
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

You'll also need to create a `scene.yaml` file with the following content:

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

Key changes made:
1. Added YAML parsing using `gopkg.in/yaml.v2`
2. Created `SceneConfig` and `ObjectConfig` structs to match the YAML structure
3. Added `loadScene` function to read and parse the YAML file
4. Modified the main function to use the parsed configuration
5. Added proper error handling for file operations and YAML decoding
6. The scene loading now supports multiple objects of the same type (spheres in this case)

Note: You'll need to install the YAML library with:
```bash
go get gopkg.in/yaml.v2
```