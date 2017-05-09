**USER API**
----
## hostname: http://dmytrokaminskiy92.pythonanywhere.com
## root api path = /api/v1
## headers: "content-type: application/json"

### Registrate user
#### url = auth/register

* **Method:**
  `POST`
  
*  **BODY Params**
{
"phone": "380935786917"
}

* **Success Response:**
{
  "message": "Successfully registered.",
  "phone_code": "3370",
  "success": true
}

### Login user
#### url = auth/login

* **Method:**
  `POST`
  
*  **BODY Params**
{
"phone_code": "3370",
"phone": "380935786917"
}

* **Success Response:**
{
  "message": "Successfully logged in.",
  "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0OTQzMjc4NTAsInN1YiI6MSwiaWF0IjoxNDk0MzI3ODQ1fQ.ll-HgbkzYt4NShf4qEyaMI1jqmE_x62jGPxcxQuRLPw",
  "success": true
}

### Status user
#### url = auth/status
### Headers - Authorization: %auth_token%

* **Method:**
  `GET`

* **Success Response:**
{
  "data": {
    "user_id": 1,
    "registered_on": "2017-05-09T07:33:56.071049",
    "admin": false,
    "email": "test@gmail.com"
  },
  "success": true
}

### Logout user
#### url = auth/logout
### Headers - Authorization: %auth_token%

* **Method:**
  `POST`

* **Success Response:**
{
  "message": "Successfully logged out.",
  "success": true
}
