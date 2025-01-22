# REST API Documentation

## API Overview

DevCrew provides a REST API for programmatic access to its functionality.

## Base URL

```
http://localhost:8000
```

## Authentication

All API endpoints require authentication using an API key header:

```
X-API-Key: your_api_key
```

## Endpoints

### Create Project

Creates a new development project.

```http
POST /projects/
Content-Type: application/json

{
    "requirements": "Create a modern web application with Next.js and TypeScript",
    "project_name": "my-app",
    "timeout": 3600
}
```

#### Parameters
- `requirements` (string, required) - Project requirements
- `project_name` (string, optional) - Custom project name
- `timeout` (integer, optional) - Custom timeout in seconds

#### Response
```json
{
    "project_id": "proj_123abc",
    "status": "created",
    "workspace": "/path/to/workspace"
}
```

### Get Project Status

Retrieves project status and details.

```http
GET /projects/{project_id}
```

#### Response
```json
{
    "project_id": "proj_123abc",
    "status": "in_progress",
    "current_task": "analyzing_requirements",
    "progress": 25,
    "created_at": "2024-01-22T10:00:00Z",
    "updated_at": "2024-01-22T10:05:00Z"
}
```

### Cancel Project

Cancels an ongoing project.

```http
POST /projects/{project_id}/cancel
```

#### Response
```json
{
    "project_id": "proj_123abc",
    "status": "cancelled",
    "cancelled_at": "2024-01-22T10:10:00Z"
}
```

## Status Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Server Error

## Error Responses

```json
{
    "error": {
        "code": "invalid_request",
        "message": "Invalid project requirements",
        "details": {
            "field": "requirements",
            "reason": "cannot be empty"
        }
    }
}
```

## Rate Limiting

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1640995200
```

## Webhooks

Configure webhooks for project updates:

```http
POST /webhooks
Content-Type: application/json

{
    "url": "https://your-server.com/webhook",
    "events": ["project.created", "project.completed"]
}
```