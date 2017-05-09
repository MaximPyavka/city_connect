**USER API**
----
## hostname: http://dmytrokaminskiy92.pythonanywhere.com
## root api path = /api/v1
## headers: "content-type: application/json"

### Registrate user
#### url = auth/register

* **Method:**
  `POST`
  
*  **URL Params**
{
"login": "test_user",
"email": "test@gmail.com",
"password": "password"
}

* **Success Response:**
{
"message": "Successfully registered.",
"success": true,
"auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTQzMTUyNDEsImlhdCI6MTQ5NDMxNTIzNiwic3ViIjoxfQ.YCVYPNtpKn8nhK-Vpw0enArM37SqVWfjQW4zbk0LkNs"
}

### Login user
#### url = auth/login

* **Method:**
  `POST`
  
*  **URL Params**
{
"login": "test_user",
"email": "test@gmail.com",
"password": "password",
"auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTQzMTUyNDEsImlhdCI6MTQ5NDMxNTIzNiwic3ViIjoxfQ.YCVYPNtpKn8nhK-Vpw0enArM37SqVWfjQW4zbk0LkNs"
}

* **Success Response:**
{
  "message": "Successfully logged in.",
  "success": true,
  "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTQzMTYwMjQsImlhdCI6MTQ5NDMxNjAxOSwic3ViIjoxfQ.8Ss7-plkasM11jfCAsO4L94FlMThxOgTC7KumGMvf1w"
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
