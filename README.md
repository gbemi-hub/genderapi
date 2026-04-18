


 Gender Profile API

API that predicts gender, age, and nationality from names using:
- Genderize API
- Agify API  
- Nationalize API

## Endpoints

### POST /api/profiles
Create a new profile or get existing if name already exists

**Request:**
```json
{"name": "emmanuel"}
Response (201 Created):

json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "emmanuel",
    "gender": "male",
    "gender_probability": 0.99,
    "sample_size": 45379,
    "age": 49,
    "age_group": "adult",
    "country_id": "NG",
    "country_probability": 0.85,
    "created_at": "2026-04-17T12:00:00Z"
  }
}
Response if already exists (200 OK):

json
{
  "status": "success",
  "message": "Profile already exists",
  "data": {...}
}
GET /api/profiles/{id}
Get a single profile by ID

Response (200 OK):

json
{
  "status": "success",
  "data": {...}
}
GET /api/profiles
Get all profiles with optional filters

Query parameters: gender, country_id, age_group (case-insensitive)

Example: /api/profiles?gender=male&country_id=NG

Response (200 OK):

json
{
  "status": "success",
  "count": 2,
  "data": [...]
}
DELETE /api/profiles/{id}
Delete a profile

Response: 204 No Content

Error Responses
All errors follow this format:

json
{"status": "error", "message": "error message"}
Status Code	Description
400	Missing or empty name
422	Invalid type
404	Profile not found
502	External API error