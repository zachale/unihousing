# Backend API

A simple Go API server with a hello world endpoint.

## Running the server

```bash
go run main.go
```

The server will start on port 8080.

## Endpoint

- `GET /hello` - Returns a JSON response with a hello world message

Example:
```bash
curl http://localhost:8080/hello
```

Response:
```json
{
  "message": "Hello, World!"
}
```

