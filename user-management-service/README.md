# User Management Service Endpoints Design Document

## Overview
User Management Service offers a set of endpoints for users to register and manage their account information. It will also serve as a service for user authentication and log in.

## Base URL
The base URL for all endpoints is: `http://localhost:8000/api/{versionId}`


### 1. Register
- URL: `/register`
- Method: POST
- Description: used to create a new user
- Request Body:
   ```json
   {
      "username": "johndoe123", //required, unique
      "forenames": "john", //required
      "surname": "doe", //required
      "email": "john_doe@email.com", //required
      "password": "password123" // required
   }
   ```
- Response:
    - 201 Created:
        ```json
        {
            "success": true,
            "response": {
               "userId": 1
            },
            "message": "User successfully created."
        }
        ```
    - 400 Bad Request:
        ```json
        {
            "success": false,
            "response": {},
            "message": "Bad request, missing fields or invalid request parameter"
        }
        ```
    - 409 Conflict:
        ```json
        {
            "success": false,
            "response": {},
            "message": "username or email already exists"   
        }
        ```
    

### 2. Login
- URL: `/login`
- Method: POST
- Description: used to authenticate user and return JWT token
- Request Body:
    ```json
    {
        "username": "johndoe123", // required
        "password": "password123" // required
    }
    ```
- Response:
    - 200 OK: Login successful, returns an access token.
        ```json
        {
            "success": true,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c", 
            "message": "successful login"
        }
        ```
    - 400 Bad Request: Invalid request parameters or missing required fields.
        ```json
        {
            "success": false,
            "token": null,
            "message": "Invalid request parameters or missing fields"
        }
        ```
    - 401 Unauthorized: Invalid username or password.
        ```json
        {
            "success": false,
            "token": null,
            "message": "Invalid username or password"
        }
        ```

### 3. Get User
- URL: `/users/{id}`
- Method: GET
- Description: returns user information
- URL Parameters: `id` int (required)
- Response:
    - 200 OK: Returns the user profile information.
        ```json
        {
            "success": true,
            "response": {
                {
                    "id": 1,
                    "username": "johndoe123",
                    "forenames": "john",
                    "surname": "doe",
                    "email": "john_doe@email.com",
                    "bio": "Bio message",
                    "displayName": "john_doe",
                    "createdAt": "01-01-2023 00:00:00",
                    "updatedAt": "01-01-2023 00:00:00"
                }
            },
            "message": null
        }
        ```
    - 404 Not Found: User not found.
        ```json
        {
            "success": false,
            "response": {},
            "message": "User not found"
        }
        ```

### 4. Update User
- URL: `/users/{id}`
- Method: PUT
- URL Parameters: `id` int required 
- Description: Update user profile
- Request Body:
    ```json
        {
            "forenames": "john", //optional
            "surname": "doe", //optional
            "email": "john_doe@email.com", //optional
            "bio": "new bio", //optional
            "displayName": "john_doe" //optional
        }
    ```
- Response:
    - 200 OK: User profile successfully updated.
        ```json
        {
            "success": true,
            "response": {
                "id": 1
            },
            "message": "successfully update profile"
        }
        ```
    - 400 Bad Request: Invalid request parameters.
        ```json
        {
            "success": false,
            "response": {},
            "message": "Invalid request parameters"
        }
        ```
    - 404 Not Found: User not found.
        ```json
        {
            "success": false,
            "response": {},
            "message": "No user Found"
        }
        ```

### 5. Delete User
- URL: `/users/{id}`
- Method: DELETE
- URL Parameter: `id` int (required)
- Description: Deletes user from database
- Response:
    - 204 No Content: User account successfully deleted.
    - 404 Not Found: User not found.
        ```json
        {
            "success": false,
            "message": "User not found"
        }
        ```
## Password Reset
### 6. Password Reset Request
- URL: `/password/reset-request`
- Method: POST
- Description: Initiate a password reset request by providing the user's email.
- Request Body:
   ```json
   {
      "email": "john_doe@email.com" // required
   }
   ```
- Response:
    - 200 OK: Password reset Initiated (email reset link sent to user's email)
    - 400 Bad Request: Invalid Request parameters
        ```json
        {
        "success": false,
        "response": {},
        "message": "Invalid request parameters or missing fields"
        }
        ```
    - 404 Not Found: User not found
        ```json
        {
        "success": false,
        "response": {},
        "message": "User not found"
        }

        ```

### 7. Password Reset Confirmation
- URL: `/password/reset-confirm`
- Method: POST
- Description: Confirm the password reset request by providing the reset token and the new password.
- Request Body:
   ```json
   {
      "reset_token": "token_received_in_email", // required
      "new_password": "new_password123" // required
   }
- Response:
    - 200 OK: Password reset successful
        ```json
        {
        "success": true,
        "response": {},
        "message": "Password reset successful"
        }
        ```
    - 400 Bad Request: Invalid request parameters or missing fields
        ```json
        {
        "success": false,
        "response": {},
        "message": "Invalid request parameters or missing fields"
        }
        ```
    - 401 Unauthorized: Invalid or expired reset token
        ```json
        {
        "success": false,
        "response": {},
        "message": "Invalid or expired reset token"
        }

        ```
    - 404 Not Found: User not found
        ```json
        {
        "success": false,
        "response": {},
        "message": "User not found"
        }

        ```
## Error Handling
The User Management Service follows standard HTTP status codes and provides appropriate error responses for various scenarios. Common error responses include:

- 400 Bad Request: Invalid request parameters or missing required fields.
- 401 Unauthorized: Invalid authentication credentials.
- 404 Not Found: Resource not found.
- 409 Conflict: Conflict with an existing resource.
- 500 Internal Server Error: Server-side error occurred.

## Authentication and Security
Authentication is token-based using JWT (JSON Web Tokens).
User passwords are securely hashed and stored in the database.
Endpoints that require authentication will validate the access token before processing the request.

## Rate Limiting
To prevent abuse and protect against brute force attacks, rate limiting mechanisms will be implemented to restrict the number of requests per user or IP address within a certain time frame.

## Versioning
API versioning will be implemented to allow for future changes and enhancements to the User Management Service. Versioning will be indicated in the URL or request headers.