# Gender Classification API

A simple API that predicts gender from names using the Genderize.io API.

## API Endpoint

`GET /api/classify?name={name}`

## Response Format

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-15T12:00:00Z"
  }
}