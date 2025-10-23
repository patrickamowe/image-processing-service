# Image Processing Service

## Description
**Image Processing Service** is a backend system designed for uploading, transforming, and retrieving images in various formats efficiently.  

Inspired by the project on [roadmap.sh: Image Processing Service](https://roadmap.sh/projects/image-processing-service).

---

## Project Structure

```
image-processing-service/
├── main.py                 # Entry point of the FastAPI app
├── routes/                 # Contains API route handlers
│   ├── user_routes.py
│   ├── auth_routes.py
│   └── image_routes.py
├── models/                 # SQLAlchemy models for database tables
│   └── models.py
├── schemas/                # Pydantic schemas for request/response validation
│   ├── user_schema.py
│   ├── image_schema.py
│   └── token_schema.py
├── db/               # Database configuration and session
│   └── database.py
├── utils/
│   ├── auth_utils.py    # Helper functions (e.g., image processing logic, acess token creation)
│   └── image_utils.py
├── uploads/             # Directory for uploaded images automatically create if not exist
├── tests/                # Unit tests for routes and logic
│   ├── test_users.py
│   ├── test_auth.py
│   └── test_images.py
├── .gitignore              # Files and directorys to exclude from git
├── .env.example            # Environment variable sample
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Installation

### Steps to Install

1. **Clone the repository**
   ```bash
   git clone https://github.com/patrickamowe/image-processing-service.git
   ```
   Open the repository in your favorite code editor (IDE).

2. **Create and activate a virtual environment**

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running and Testing

### Run the API Server
```bash
  fastapi dev main.py
```
This command starts the server locally at `http://127.0.0.1:8000`.

---

## Testing the API Endpoints

### User Endpoints

#### 1. Create a new user (Sign Up)
**POST** `/users/sign-up`
```json
{
  "username": "your-username",
  "password": "your-password"
}
```
**Response:**
```json
{
  "user_id": 1,
  "username": "your-username",
  "created_at": "current-time-date"
}
```

#### 2. Get user details  
**GET** `/users/{user_id}`  
**Response:**
```json
{
  "user_id": 1,
  "username": "your-username",
  "created_at": "current-time-date"
}
```

---

### Authentication Endpoints

#### 1. Login user
**POST** `/auth/login`

**Form Data:**
```
username: <select text> your-username
password: <select text> your-password
```

**Response:**
```json
{
  "access_token": "your-access-token",
  "token_type": "bearer"
}
```

---

### Image Endpoints

#### 1. Upload image  
**POST** `/images`  
**Headers:**
```
Authorization: Bearer <access_token>
```
**Form Data:**
```
file: <select file> pick image
```

**Response:**
```json
{
  "url": "uploads/unique-file-name.extension",
  "meta_data": {},
  "created_at": "current-time-date"
}
```

---

#### 2. Get image  
**GET** `/images/{image_id}`  
**Response:**
```json
{
  "url": "uploads/unique-file-name.extension",
  "meta_data": {},
  "created_at": "current-time-date"
}
```

---

#### 3. Get paginated images  
**GET** `/images?page_no=<num>&page_limit=<limit>`  
**Response:**
```json
[
  {
    "url": "uploads/unique-file-name.extension",
    "meta_data": {},
    "created_at": "current-time-date"
  },
  {
    "url": "uploads/unique-file-name.extension",
    "meta_data": {},
    "created_at": "current-time-date"
  }
]
```

---

#### 4. Transform image  
**POST** `/images/{image_id}/transform`

The **image-processing-service** currently supports the following transformations:

| Transformation | Description                                                               |
|----------------|---------------------------------------------------------------------------|
| **Resize**     | Adjusts the image dimensions to specified width and height.               |
| **Crop**       | Removes unwanted outer areas from an image based on given coordinates.    |
| **Rotate**     | Rotates the image by a specific angle (e.g., 90°, 180°, 270°).            |
| **Flip**       | Flips the image vertically (top to bottom).                               |
| **Mirror**     | Flips the image horizontally (left to right).                             |
| **Compress**   | Reduces file size by adjusting image quality without changing dimensions. |
| **Format**     | Converts the image to a different format (e.g., PNG, JPEG, WEBP).         |
| **Filter**     | Applies visual effects such as blur, sharpen, contour, or grayscale.      |
| **Watermark**  | Adds a text watermark to protect or brand the image.                      |

---

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example Transformations:**
```json
{
    "resize": { "width": 300, "height": 200 },
    "crop": { "width": 100, "height": 100, "x": 10, "y": 10 },
    "rotate": 90,
    "flip": true,
    "mirror": true,
    "compress": true,
    "format": "JPEG",
    "filters": {
      "grayscale": true,
      "sepia": false
    },
    "watermark": "optional text"
}
```

**Response:**
```json
{
  "url": "uploads/unique-file-name.extension",
  "meta_data": {},
  "created_at": "current-time-date"
}
```

---

## License
This project is licensed under the **MIT License**.
