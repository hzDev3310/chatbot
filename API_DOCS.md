# API Documentation

This document provides detailed information about the available API endpoints in the application.

## Authentication

Most endpoints require authentication using JWT (JSON Web Token). Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Endpoints

### Authentication

#### Register User
- **URL**: `/auth/register`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Success Response** (201):
  ```json
  {
    "message": "User registered successfully",
    "user_id": "string"
  }
  ```
- **Error Response** (400):
  ```json
  {
    "error": "Email already registered"
  }
  ```

#### Login
- **URL**: `/auth/login`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Success Response** (200):
  ```json
  {
    "user_id": "string"
  }
  ```
- **Error Response** (401):
  ```json
  {
    "error": "Invalid email or password"
  }
  ```

### Chat

#### Generate Response
- **URL**: `/chat/generate`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "prompt": "string",
    "chat_id": "string" (optional)
  }
  ```
- **Success Response** (200):
  ```json
  {
    "response": "string",
    "chat_id": "string",
    "success": true
  }
  ```
- **Error Response** (400):
  ```json
  {
    "error": "Missing required fields"
  }
  ```

#### Get Chat History
- **URL**: `/chat/history`
- **Method**: `GET`
- **Authentication**: Required
- **Success Response** (200):
  ```json
  {
    "history": {
      "chat_id": [
        {
          "message": "string",
          "type": "string",
          "timestamp": "string"
        }
      ]
    }
  }
  ```

#### Clear Chat History
- **URL**: `/chat/clear`
- **Method**: `POST`
- **Authentication**: Required
- **Success Response** (200):
  ```json
  {
    "message": "Chat history cleared successfully"
  }
  ```

#### Rate Message
- **URL**: `/chat/rate`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "message_id": "string",
    "rating": "number"
  }
  ```
- **Success Response** (200):
  ```json
  {
    "message": "Rating saved successfully",
    "average_rating": "number"
  }
  ```
- **Error Response** (400):
  ```json
  {
    "error": "Message ID and rating are required"
  }
  ```

## Error Handling

All endpoints follow a consistent error response format:
```json
{
  "error": "Error message description"
}
```

Common HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 500: Internal Server Error