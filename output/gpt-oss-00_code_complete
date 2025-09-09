```go
func (r *Ray) Init(origin []float64, direction []float64) Ray {
	// copy origin slice to avoid external mutation
	r.origin = make([]float64, len(origin))
	copy(r.origin, origin)

	// copy direction slice
	dir := make([]float64, len(direction))
	copy(dir, direction)

	// normalize direction vector
	var sum float64
	for _, v := range dir {
		sum += v * v
	}
	lenDir := math.Sqrt(sum)
	if lenDir != 0 {
		for i := range dir {
			dir[i] /= lenDir
		}
	}
	r.direction = dir

	return *r
}
```