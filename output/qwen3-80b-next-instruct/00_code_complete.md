```go
func (r *Ray) Init(origin []float64, direction []float64) Ray { 
    r.origin = make([]float64, len(origin))
    copy(r.origin, origin)
    r.direction = make([]float64, len(direction))
    copy(r.direction, direction)
    return *r
}
```