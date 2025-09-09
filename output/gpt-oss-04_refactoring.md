Below is a **complete, self‑contained example** that loads a scene description from a YAML file, builds the `core.Camera` and the list of `core.RayMarchableObject`s, renders the image and writes it to `output.png`.

---

## 1️⃣  Directory layout

```
my‑ray‑marcher/
├─ go.mod
├─ main.go
└─ scene.yaml      ← your scene description
```

---

## 2️⃣  `go.mod`

```go
module my-ray-marcher

go 1.22   // or whatever version you use

require (
    github.com/hnatekmarorg/sunshine v0.0.0-2024xxxxxx // whatever version you use
    gopkg.in/yaml.v3 v3.0.1
)
```

Run `go mod tidy` after you create the file – it will fetch the YAML package.

---

## 3️⃣  `scene.yaml`  (you can extend it as you like)

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

The `objects` list can contain any number of objects.  
At the moment we only support **spheres** – adding a new type is a one‑line change (see the comment in the code).

---

## 4️⃣  `main.go`

```go
package main

import (
	"fmt"
	"image/png"
	"log"
	"os"

	"github.com/hnatekmarorg/sunshine/core"
	"gopkg.in/yaml.v3"
)

/* -------------------------------------------------------------------------
   YAML → Go structures
   -------------------------------------------------------------------------*/

type sceneFile struct {
	Scene scene `yaml:"scene"`
}

type scene struct {
	Camera  camConfig      `yaml:"camera"`
	Objects []objectConfig `yaml:"objects"`
}

/*--- Camera --------------------------------------------------------------*/
type camConfig struct {
	Width     int       `yaml:"width"`
	Height    int       `yaml:"height"`
	Direction []float64 `yaml:"direction"`
}

/*--- Objects -------------------------------------------------------------*/
/*
   Each entry in the YAML list looks like

   - sphere:
       position: [x, y, z]
       radius:   r

   The struct below has a field for every object type we want to support.
   Only the field that matches the key in the YAML will be non‑nil after
   unmarshalling.
*/
type objectConfig struct {
	Sphere *sphereConfig `yaml:"sphere,omitempty"` // add more fields for other types
	// Cube   *cubeConfig   `yaml:"cube,omitempty"`   // example for future extensions
}

type sphereConfig struct {
	Position []float64 `yaml:"position"` // must be length 3
	Radius   float64   `yaml:"radius"`
}

/* -------------------------------------------------------------------------
   Helper: turn the generic object configs into core.RayMarchableObject
   -------------------------------------------------------------------------*/

func buildObjects(cfgs []objectConfig) []core.RayMarchableObject {
	var objs []core.RayMarchableObject

	for i, cfg := range cfgs {
		switch {
		case cfg.Sphere != nil:
			s := cfg.Sphere
			if len(s.Position) != 3 {
				log.Printf("object %d – sphere position must have 3 components, got %d – skipping",
					i, len(s.Position))
				continue
			}
			objs = append(objs, core.NewSphere(s.Position, s.Radius))

		// case cfg.Cube != nil:
		//   // future object types go here
		default:
			log.Printf("object %d – unknown object type (fields are all nil) – skipping", i)
		}
	}
	return objs
}

/* -------------------------------------------------------------------------
   Main – load YAML, build scene, render, write PNG
   -------------------------------------------------------------------------*/

func main() {
	// --------------------------------------------------------------
	// 1️⃣  Load and parse the YAML file
	// --------------------------------------------------------------
	ymlData, err := os.ReadFile("scene.yaml")
	if err != nil {
		log.Fatalf("cannot read scene.yaml: %v", err)
	}

	var file sceneFile
	if err := yaml.Unmarshal(ymlData, &file); err != nil {
		log.Fatalf("cannot parse scene.yaml: %v", err)
	}

	// --------------------------------------------------------------
	// 2️⃣  Build the camera from the config
	// --------------------------------------------------------------
	camCfg := file.Scene.Camera
	if len(camCfg.Direction) != 3 {
		log.Fatalf("camera.direction must contain exactly three floats, got %d", len(camCfg.Direction))
	}
	cam := core.Camera{
		Width:     camCfg.Width,
		Height:    camCfg.Height,
		Direction: camCfg.Direction,
	}

	// --------------------------------------------------------------
	// 3️⃣  Build the objects slice
	// --------------------------------------------------------------
	objs := buildObjects(file.Scene.Objects)

	// --------------------------------------------------------------
	// 4️⃣  Render
	// --------------------------------------------------------------
	img := cam.Render(objs)

	// --------------------------------------------------------------
	// 5️⃣  Write the PNG file
	// --------------------------------------------------------------
	out, err := os.Create("output.png")
	if err != nil {
		log.Fatalf("cannot create output.png: %v", err)
	}
	defer out.Close()

	if err := png.Encode(out, img); err != nil {
		log.Fatalf("png encode failed: %v", err)
	}

	fmt.Println("✅  Rendered image saved to output.png")
}
```

### What changed?

| Old code | New code |
|----------|----------|
| Camera and objects were built **hard‑coded** in Go. | A **YAML file** (`scene.yaml`) now contains the whole scene description. |
| The list of objects was a literal `[]core.RayMarchableObject{ … }`. | We parse a slice of `objectConfig`, then turn each entry into the appropriate `core.New…` call (`buildObjects`). |
| No external data source. | The program now **fails fast** with a clear message if the YAML is malformed or missing required fields. |
| Adding a new object type required editing the Go source and the literal list. | To add another primitive (e.g. a cube) you only need to: <br>1. Add a struct (`cubeConfig`) and a pointer field in `objectConfig`. <br>2. Extend `buildObjects` with a case for it. <br>3. Use the new type in `scene.yaml`. No changes to the main rendering flow. |

---

## 5️⃣  Extending the loader (quick guide)

Suppose you want to support a **cube** with fields `center: [x y z]` and `size: s`.

1. **Add a Go struct**

   ```go
   type cubeConfig struct {
       Center []float64 `yaml:"center"`
       Size   float64   `yaml:"size"`
   }
   ```

2. **Add a pointer field to `objectConfig`**

   ```go
   type objectConfig struct {
       Sphere *sphereConfig `yaml:"sphere,omitempty"`
       Cube   *cubeConfig   `yaml:"cube,omitempty"` // NEW
   }
   ```

3. **Add a case in `buildObjects`**

   ```go
   case cfg.Cube != nil:
       c := cfg.Cube
       if len(c.Center) != 3 {
           log.Printf("cube %d – center must have 3 components – skipping", i)
           continue
       }
       objs = append(objs, core.NewCube(c.Center, c.Size)) // whatever API you have
   ```

4. **Use it in YAML**

   ```yaml
   - cube:
       center: [0, -1, -3]
       size: 2
   ```

That’s it – the loader automatically recognises the new type without any other code changes.

---

## 6️⃣  Running the program

```bash
# from the project root
go run .
# or build a binary
go build -o raymarcher .
./raymarcher
```

You should see:

```
✅  Rendered image saved to output.png
```

…and `output.png` will contain the rendered scene defined in `scene.yaml`.

---

### TL;DR

*Define a small set of Go structs that mirror the YAML layout, unmarshal the file, translate the generic config structs into concrete `core.NewSphere` (or other) objects, then render exactly as before.* The code above does that, is easy to extend, and keeps the rendering logic untouched. Happy ray‑marching!