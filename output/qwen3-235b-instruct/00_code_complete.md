```go
func (r *Ray) Init(origin []float64, direction []float64) Ray { 
	return Ray{
		origin: origin,
		direction: direction,
	}
}
```