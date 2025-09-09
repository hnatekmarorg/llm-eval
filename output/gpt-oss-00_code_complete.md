```go
func (r *Ray) Init(origin []float64, direction []float64) Ray {
	// copy origin slice to keep the ray independent of the caller's data
	r.origin = make([]float64, len(origin))
	copy(r.origin, origin)

	// ensure the direction is a unit vector
	// vek.Normalize returns a new, normalized slice
	r.direction = vek.Normalize(direction)

	return *r
}
```