Here is the complete implementation of the `Init` method for initializing a 3D ray. The method creates a new `Ray` instance using the provided `origin` and `direction` vectors.

```go
func (r *Ray) Init(origin []float64, direction []float64) Ray {
	return Ray{
		origin:    origin,
		direction: direction,
	}
}
```

### Explanation:
1. **Input Parameters**:
   - `origin`: A slice of `float64` representing the starting point of the ray.
   - `direction`: A slice of `float64` representing the direction vector of the ray.

2. **Returning a New Ray**:
   - The `Init` method constructs a new `Ray` instance by initializing its fields `origin` and `direction` with the provided input slices.
   - It returns a new `Ray` struct, which is a value type in Go.

3. **Structure**:
   - The `Ray` struct has two fields: `origin` and `direction`, both of type `[]float64`.
   - The method uses inline initialization to create the new `Ray` and return it.

This implementation ensures that the `Init` method is concise, clear, and adheres to Go's idiomatic style.