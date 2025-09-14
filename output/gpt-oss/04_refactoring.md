Below is a **complete, self‑contained example** that shows how to move the hard‑coded scene into a **YAML file** and load it at run‑time.

It contains three parts:

1. **`scene.yaml`** – the scene description (you can add more objects later).
2. **`main.go`** – the refactored program that reads the YAML, builds the `core.Camera` and the slice of `core.RayMarchableObject`, and renders the image.
3. **Explanation** – why we need a custom `UnmarshalYAML` implementation for the polymorphic objects and a few tips for extending the format.

---

## 1️⃣ `scene.yaml`

```yaml
scene:
  camera:
    width: 512
    height: 512
    direction: [0, 0, 1]   # look‑forward vector
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

*Feel free to add other object types (plane, box, …) – you’ll just need a matching struct and a case in `Object.UnmarshalYAML`.*

---

## 2️⃣ `main.go`

```go
// main.go
package main

import (
	"fmt"
	"image/png"
	"os"

	"github.com/hnatekmarorg/sunshine/core"
	"gopkg.in/yaml.v3"
)

// ---------------------------------------------------------------------
// 1. YAML structures – these map 1:1 to the file format.
// ---------------------------------------------------------------------

type SceneFile struct {
	Scene Scene `yaml:"scene"`
}

type Scene struct {
	Camera  CameraConfig   `yaml:"camera"`
	Objects []ObjectConfig `yaml:"objects"`
}

// CameraConfig mirrors the fields expected by core.Camera.
type CameraConfig struct {
	Width     int       `yaml:"width"`
	Height    int       `yaml:"height"`
	Direction []float64 `yaml:"direction"`
}

// ObjectConfig is a **polymorphic** wrapper – an object can be a sphere,
// a plane, a mesh … the concrete type is decided at Unmarshal time.
type ObjectConfig struct {
	// The concrete type that was found in the YAML (e.g. "sphere").
	Type string

	// Only one of the following pointers will be non‑nil after unmarshalling.
	Sphere *SphereConfig
	// Future types could be added here, e.g. Plane *PlaneConfig
}

// SphereConfig holds the data needed by core.NewSphere.
type SphereConfig struct {
	Position []float64 `yaml:"position"`
	Radius   float64   `yaml:"radius"`
}

// ---------------------------------------------------------------------
// 2. Custom Unmarshalling – we need to look at the *key* of the map
//    (e.g. "sphere") to decide which concrete struct to decode into.
// ---------------------------------------------------------------------

func (o *ObjectConfig) UnmarshalYAML(node *yaml.Node) error {
	/*
	   Expected YAML shape:

	   - sphere:
	       position: [0,0,-2]
	       radius: 1
	*/

	if node.Kind != yaml.MappingNode || len(node.Content) != 2 {
		return fmt.Errorf("object definition must be a map with a single key")
	}

	// The map has exactly two children: keyNode, valueNode.
	keyNode := node.Content[0]
	valNode := node.Content[1]

	switch keyNode.Value {
	case "sphere":
		o.Type = "sphere"
		var s SphereConfig
		if err := valNode.Decode(&s); err != nil {
			return fmt.Errorf("failed to decode sphere: %w", err)
		}
		o.Sphere = &s
	// Add more cases here for other object types.
	default:
		return fmt.Errorf("unknown object type %q", keyNode.Value)
	}
	return nil
}

// ---------------------------------------------------------------------
// 3. Helper to convert the parsed scene into the core types.
// ---------------------------------------------------------------------

func buildCamera(cfg CameraConfig) core.Camera {
	// No validation here – core.Camera will panic later if something is off.
	return core.Camera{
		Width:     cfg.Width,
		Height:    cfg.Height,
		Direction: cfg.Direction,
	}
}

// Convert a slice of ObjectConfig into []core.RayMarchableObject.
func buildObjects(objs []ObjectConfig) ([]core.RayMarchableObject, error) {
	var result []core.RayMarchableObject
	for i, oc := range objs {
		switch oc.Type {
		case "sphere":
			if oc.Sphere == nil {
				return nil, fmt.Errorf("object %d: sphere config missing", i)
			}
			s := core.NewSphere(oc.Sphere.Position, oc.Sphere.Radius)
			result = append(result, s)
		// case "plane":   // future extension
		//     // result = append(result, core.NewPlane(...))
		default:
			return nil, fmt.Errorf("object %d: unsupported type %q", i, oc.Type)
		}
	}
	return result, nil
}

// ---------------------------------------------------------------------
// 4. Entry point – read YAML, build the scene, render and save.
// ---------------------------------------------------------------------

func main() {
	// --------------------------------------------------------------
	// (a) Load the YAML file. By default we look for "scene.yaml".
	// --------------------------------------------------------------
	yamlPath := "scene.yaml"
	if len(os.Args) > 1 {
		yamlPath = os.Args[1] // allow custom path: go run . myscene.yaml
	}
	yBytes, err := os.ReadFile(yamlPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "cannot read %s: %v\n", yamlPath, err)
		os.Exit(1)
	}

	var file SceneFile
	if err := yaml.Unmarshal(yBytes, &file); err != nil {
		fmt.Fprintf(os.Stderr, "invalid YAML: %v\n", err)
		os.Exit(1)
	}

	// --------------------------------------------------------------
	// (b) Convert YAML structs to core structs.
	// --------------------------------------------------------------
	cam := buildCamera(file.Scene.Camera)

	objects, err := buildObjects(file.Scene.Objects)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error building objects: %v\n", err)
		os.Exit(1)
	}

	// --------------------------------------------------------------
	// (c) Render the scene.
	// --------------------------------------------------------------
	img := cam.Render(objects)

	// --------------------------------------------------------------
	// (d) Write PNG.
	// --------------------------------------------------------------
	f, err := os.Create("output.png")
	if err != nil {
		fmt.Fprintf(os.Stderr, "cannot create output.png: %v\n", err)
		os.Exit(1)
	}
	defer f.Close()

	if err := png.Encode(f, img); err != nil {
		fmt.Fprintf(os.Stderr, "png encode failed: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("✅ rendered scene → output.png")
}
```

### How it works

| Step | What happens |
|------|---------------|
| **YAML → structs** | `yaml.Unmarshal` fills `SceneFile`. The custom `UnmarshalYAML` on `ObjectConfig` looks at the *key* (`sphere`) and decodes the inner map into the right concrete struct (`SphereConfig`). |
| **Structs → core types** | Helper functions `buildCamera` and `buildObjects` translate the config structs into the actual `core.Camera` and the slice of `core.RayMarchableObject`. |
| **Render** | The original `core.Camera.Render` call stays untouched – only the data source changed. |
| **Write PNG** | Same as before. |

---

## 3️⃣ Extending the format

If you want to support more shapes, just follow the pattern:

1. **Add a config struct** (e.g. `type PlaneConfig struct { ... }`).
2. **Add a field** in `ObjectConfig` (`Plane *PlaneConfig`).
3. **Add a case** in `ObjectConfig.UnmarshalYAML`:

   ```go
   case "plane":
       o.Type = "plane"
       var p PlaneConfig
       if err := valNode.Decode(&p); err != nil { … }
       o.Plane = &p
   ```

4. **Add a case** in `buildObjects` that creates the appropriate `core.NewPlane(...)` (or your own constructor) and appends it to the result slice.

Because the YAML representation is *type‑tagged* (`- sphere: …`), adding new object types never breaks existing scenes – unknown types simply raise a clear error.

---

## 4️⃣ Running the example

```bash
# 1️⃣ Install the yaml package (once)
go get gopkg.in/yaml.v3

# 2️⃣ Build & run (assuming you saved main.go and scene.yaml in the same folder)
go run .
# or, with a custom file:
go run . my_custom_scene.yaml
```

You should see:

```
✅ rendered scene → output.png
```

…and `output.png` will contain the three large spheres and the tiny one, exactly like the original hard‑coded version.

---

### TL;DR

* Define Go structs that mirror the YAML.
* Use a custom `UnmarshalYAML` on a wrapper (`ObjectConfig`) to handle the **type‑tagged** objects.
* Convert the parsed configuration into the existing `core` types.
* The rendering code stays unchanged – only the *source* of the scene data moved to a clean, editable YAML file.