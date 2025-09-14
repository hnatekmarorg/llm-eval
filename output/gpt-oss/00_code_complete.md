```go
func (r *Ray) Init(origin []float64, direction []float64) Ray {
	// Validate dimensionality (optional)
	if len(origin) != 3 || len(direction) != 3 {
		panic("origin and direction must be 3‑dimensional vectors")
	}

	// Copy origin to protect against external changes
	r.origin = make([]float64, 3)
	copy(r.origin, origin)

	// Normalize direction and store a copy
	normDir := vek.Normalize(direction)
	r.direction = make([]float64, 3)
	copy(r.direction, normDir)

	return *r
}
```