# API Contract Specification
> **Service Name:** {{SERVICE_NAME}}  
> **API Version:** v1  
> **Base URL:** `https://api.{{DOMAIN}}.com/api/v1`  
> **Protocol:** HTTPS / RESTful JSON  
> **Specification Standard:** OpenAPI 3.1.0 compatible  

---

## 1. Authentication & Headers

### 1.1 Authentication Scheme
All protected endpoints require an HTTP Authorization header containing a valid Bearer JWT:
```http
Authorization: Bearer <access_token>
```

### 1.2 Standard Request Headers
| Header | Type | Required? | Description |
| :--- | :--- | :--- | :--- |
| `Content-Type` | string | Yes (for POST/PUT) | Must be `application/json` |
| `Accept` | string | Yes | Must be `application/json` |
| `X-Request-ID` | uuid | Optional | Client correlation ID for distributed tracing |
| `Idempotency-Key`| string | Optional (Recommended for mutations) | Unique UUID to guarantee idempotency on retry |

### 1.3 Rate Limiting Headers
Responses contain the following rate limit indicators:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1720000000
```

---

## 2. Standard Response Envelopes & Error Model

### 2.1 Success Envelope (Single Entity)
```json
{
  "success": true,
  "data": {
    "id": 101,
    "name": "Sample Resource",
    "created_at": "2026-09-30T10:00:00Z"
  },
  "meta": {
    "request_id": "c1f7a0e2-8923-4e3b-b230-e37452d911b3",
    "timestamp": "2026-09-30T10:00:00Z"
  }
}
```

### 2.2 Success Envelope (Paginated Collection)
```json
{
  "success": true,
  "data": [
    { "id": 1, "name": "Item 1" },
    { "id": 2, "name": "Item 2" }
  ],
  "pagination": {
    "total_count": 150,
    "limit": 20,
    "cursor_next": "ZXhhbXBsZS1jdXJzb3ItMQ==",
    "has_more": true
  }
}
```

### 2.3 Error Envelope (RFC 7807 Compliant)
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested item was not found.",
    "details": [
      {
        "field": "item_id",
        "issue": "No record exists with ID 9999"
      }
    ],
    "request_id": "c1f7a0e2-8923-4e3b-b230-e37452d911b3"
  }
}
```

---

## 3. Endpoints Specification

### 3.1 `GET /api/v1/{{RESOURCES}}`
List and filter resources.

- **Query Parameters:**
  - `limit` (integer, default: 20, max: 100)
  - `cursor` (string, optional) - Pagination cursor
  - `search` (string, optional) - Keyword filter
  - `status` (string, optional) - Filter by lifecycle state
- **Responses:**
  - `200 OK`: Returns paginated list of resources.
  - `401 Unauthorized`: Missing or invalid bearer token.

---

### 3.2 `POST /api/v1/{{RESOURCES}}`
Create a new resource record.

- **Request Body:**
```json
{
  "name": "string (required, 2-100 chars)",
  "description": "string (optional)",
  "status": "active"
}
```
- **Responses:**
  - `201 Created`:
```json
{
  "success": true,
  "data": {
    "id": 102,
    "name": "Resource Name",
    "status": "active",
    "created_at": "2026-09-30T10:00:00Z"
  }
}
```
  - `400 Bad Request`: Payload validation failed.
  - `409 Conflict`: Resource with unique constraint already exists.

---

### 3.3 `GET /api/v1/{{RESOURCES}}/{id}`
Retrieve a single resource by its identifier.

- **Path Parameters:**
  - `id` (integer or UUID, required)
- **Responses:**
  - `200 OK`: Resource found and returned.
  - `404 Not Found`: No resource exists matching `id`.

---

### 3.4 `PUT /api/v1/{{RESOURCES}}/{id}`
Full update of an existing resource.

- **Path Parameters:**
  - `id` (integer or UUID, required)
- **Request Body:** Complete updated schema.
- **Responses:**
  - `200 OK`: Resource updated successfully.
  - `404 Not Found`: Resource does not exist.

---

### 3.5 `DELETE /api/v1/{{RESOURCES}}/{id}`
Soft or permanent deletion of a resource.

- **Path Parameters:**
  - `id` (integer or UUID, required)
- **Responses:**
  - `200 OK` or `204 No Content`: Resource deleted.
  - `404 Not Found`: Resource not found.

---

## 4. Idempotency Implementation Guidelines
For payment processing and state-altering mutations:
1. Client generates a unique UUID `Idempotency-Key` and includes it in request headers.
2. Server checks Redis key `idempotency:{key}`:
   - If key exists and is `IN_PROGRESS`, return `409 Conflict` (Concurrent request in flight).
   - If key exists and has cached response, return cached response with header `X-Cache-Lookup: HIT`.
   - If key does not exist, store key with status `IN_PROGRESS` (TTL: 120s), execute logic, cache result (TTL: 24h), and return response.
