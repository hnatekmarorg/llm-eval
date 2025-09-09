```go
func (r *Ray) Init(origin []float64, direction []float64) Ray {
	r.origin = origin
	r.direction = direction
	return *r
}
```