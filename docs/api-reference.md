# API Reference — Student Guidance System

> Complete REST API documentation for the Course Counseling Platform

---

## Base URL

```
Development: http://localhost:8000/api/
Production:  https://api.yourdomain.com/api/
```

## Authentication

All endpoints except **Register** and **Login** require a JWT Bearer token:

```http
Authorization: Bearer <access_token>
```

### Token Lifecycle
- **Access Token**: Valid for 15 minutes
- **Refresh Token**: Valid for 7 days
- **Blacklisting**: Refresh tokens are blacklisted on logout

---

## Response Format

All responses follow this structure:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": { ... }
  }
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK — Successful GET/PUT/PATCH |
| 201 | Created — Successful POST |
| 204 | No Content — Successful DELETE |
| 400 | Bad Request — Validation error |
| 401 | Unauthorized — Missing/invalid token |
| 403 | Forbidden — Insufficient permissions |
| 404 | Not Found — Resource doesn't exist |
| 500 | Internal Server Error |

---

## 1. Authentication Endpoints

### 1.1 Register

Create a new student account.

```http
POST /auth/register/
```

**Request Body**:

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+977-9801234567"
}
```

**Response (201 Created)**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+977-9801234567",
    "role": "student"
  },
  "message": "User registered successfully"
}
```

**Validation Rules**:
- `email`: Must be unique, valid email format
- `password`: Minimum 8 characters, at least 1 uppercase, 1 number
- `password2`: Must match `password`
- `phone`: Must be unique, valid Nepal phone format (+977-XXXXXXXXXX)

---

### 1.2 Login

Obtain JWT access and refresh tokens.

```http
POST /auth/login/
```

**Request Body**:

```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "email": "john@example.com",
      "username": "john_doe",
      "first_name": "John",
      "last_name": "Doe",
      "role": "student"
    }
  },
  "message": "Login successful"
}
```

---

### 1.3 Logout

Blacklist the refresh token to prevent reuse.

```http
POST /auth/logout/
```

**Request Body**:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (204 No Content)**:

```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

---

### 1.4 Get Current User

Retrieve the authenticated user's profile.

```http
GET /auth/me/
```

**Headers**:

```http
Authorization: Bearer <access_token>
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+977-9801234567",
    "role": "student",
    "profile": {
      "bio": "Aspiring web developer",
      "image": "/media/profiles/john.jpg",
      "address": "Kathmandu, Nepal",
      "birth_date": "2000-05-15"
    }
  }
}
```

---

### 1.5 Update Profile

Update the authenticated user's profile.

```http
PUT /auth/me/
```

**Headers**:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+977-9801234567",
  "profile": {
    "bio": "Full-stack developer in training",
    "address": "Lalitpur, Nepal"
  }
}
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "profile": {
      "bio": "Full-stack developer in training",
      "address": "Lalitpur, Nepal"
    }
  },
  "message": "Profile updated successfully"
}
```

---

## 2. Courses Endpoints

### 2.1 List All Courses

Get all active courses with optional filtering.

```http
GET /courses/?category=web-development&level=beginner&search=mern
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | Filter by category slug |
| `level` | string | `beginner`, `intermediate`, `advanced` |
| `search` | string | Search in title and description |
| `page` | integer | Pagination page number |
| `page_size` | integer | Items per page (default: 10) |

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "count": 25,
    "next": "http://localhost:8000/api/courses/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "MERN Stack Development",
        "description": "Complete full-stack development with MongoDB, Express, React, and Node.js",
        "category": {
          "id": 1,
          "name": "Web Development",
          "slug": "web-development"
        },
        "level": "intermediate",
        "duration_weeks": 12,
        "price": 25000.00,
        "currency": "NPR",
        "instructor_name": "Rajesh Sharma",
        "skills_gained": ["React", "Node.js", "MongoDB", "Express", "REST API"],
        "career_opportunities": ["Full Stack Developer", "MERN Developer", "Web Application Developer"],
        "is_active": true,
        "total_batches": 3,
        "upcoming_batches": 2
      }
    ]
  }
}
```

---

### 2.2 Get Course Detail

Get detailed information about a specific course including batches.

```http
GET /courses/<id>/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "MERN Stack Development",
    "description": "Complete full-stack development course...",
    "category": {
      "id": 1,
      "name": "Web Development",
      "slug": "web-development"
    },
    "level": "intermediate",
    "duration_weeks": 12,
    "price": 25000.00,
    "currency": "NPR",
    "instructor_name": "Rajesh Sharma",
    "prerequisites": ["Basic JavaScript", "HTML/CSS fundamentals"],
    "skills_gained": ["React", "Node.js", "MongoDB", "Express", "REST API", "JWT Auth"],
    "career_opportunities": ["Full Stack Developer", "MERN Developer", "Web Application Developer"],
    "syllabus": [
      {"week": 1, "topic": "JavaScript ES6+ Review", "description": "Arrow functions, destructuring, async/await"},
      {"week": 2, "topic": "Node.js & Express", "description": "Building REST APIs with Express"},
      {"week": 3, "topic": "MongoDB & Mongoose", "description": "NoSQL database design and ODM"},
      {"week": 4, "topic": "React Fundamentals", "description": "Components, props, state, hooks"},
      {"week": 5, "topic": "React Advanced", "description": "Context API, Redux, custom hooks"},
      {"week": 6, "topic": "Full Stack Integration", "description": "Connecting frontend to backend"}
    ],
    "batches": [
      {
        "id": 1,
        "start_date": "2026-08-01",
        "end_date": "2026-10-24",
        "max_seats": 25,
        "current_enrollments": 18,
        "available_seats": 7,
        "status": "upcoming",
        "schedule": {
          "days": ["Sunday", "Tuesday", "Thursday"],
          "time": "07:00 - 09:00"
        }
      }
    ]
  }
}
```

---

### 2.3 List Categories

Get all course categories.

```http
GET /courses/categories/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Web Development",
      "slug": "web-development",
      "description": "Frontend and backend web technologies",
      "course_count": 8
    },
    {
      "id": 2,
      "name": "Data Science",
      "slug": "data-science",
      "description": "Python, ML, data analysis",
      "course_count": 5
    },
    {
      "id": 3,
      "name": "Cybersecurity",
      "slug": "cybersecurity",
      "description": "Ethical hacking and network security",
      "course_count": 3
    }
  ]
}
```

---

### 2.4 Create Course (Staff Only)

Add a new course to the catalog.

```http
POST /courses/
```

**Headers**:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**:

```json
{
  "title": "Machine Learning Fundamentals",
  "description": "Introduction to ML with Python and scikit-learn",
  "category": 2,
  "level": "beginner",
  "duration_weeks": 10,
  "price": 30000.00,
  "currency": "NPR",
  "instructor_name": "Dr. Sita Gurung",
  "prerequisites": ["Basic Python", "Statistics fundamentals"],
  "skills_gained": ["Python", "scikit-learn", "pandas", "numpy", "data visualization"],
  "career_opportunities": ["Data Analyst", "ML Engineer", "AI Researcher"],
  "syllabus": [
    {"week": 1, "topic": "Python for Data Science", "description": "NumPy, Pandas basics"},
    {"week": 2, "topic": "Data Visualization", "description": "Matplotlib, Seaborn"}
  ]
}
```

**Response (201 Created)**:

```json
{
  "success": true,
  "data": {
    "id": 5,
    "title": "Machine Learning Fundamentals",
    "category": {
      "id": 2,
      "name": "Data Science"
    },
    "level": "beginner",
    "duration_weeks": 10,
    "price": 30000.00,
    "is_active": true
  },
  "message": "Course created successfully"
}
```

---

## 3. Assessment Endpoints

### 3.1 List Assessments

Get all available skill assessments.

```http
GET /assessments/
```

**Headers**:

```http
Authorization: Bearer <access_token>
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Tech Career Path Finder",
      "description": "Discover which tech career suits you best",
      "category": "career_guidance",
      "question_count": 12,
      "estimated_time_minutes": 10,
      "is_active": true
    },
    {
      "id": 2,
      "title": "Programming Aptitude Test",
      "description": "Test your logical thinking and problem-solving skills",
      "category": "aptitude",
      "question_count": 15,
      "estimated_time_minutes": 15,
      "is_active": true
    }
  ]
}
```

---

### 3.2 Get Assessment Detail

Get a single assessment with its questions.

```http
GET /assessments/<id>/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Tech Career Path Finder",
    "description": "Discover which tech career suits you best",
    "category": "career_guidance",
    "estimated_time_minutes": 10,
    "questions": [
      {
        "id": 1,
        "text": "Do you enjoy solving logic puzzles and mathematical problems?",
        "type": "single_choice",
        "options": [
          {"id": "a", "text": "Yes, I love them!", "value": "yes_love"},
          {"id": "b", "text": "Sometimes", "value": "sometimes"},
          {"id": "c", "text": "Not really", "value": "no"}
        ]
      },
      {
        "id": 2,
        "text": "Which activity sounds most appealing to you?",
        "type": "single_choice",
        "options": [
          {"id": "a", "text": "Building websites and apps", "value": "web_dev"},
          {"id": "b", "text": "Analyzing data and finding patterns", "value": "data_science"},
          {"id": "c", "text": "Protecting systems from hackers", "value": "cybersecurity"},
          {"id": "d", "text": "Designing user interfaces", "value": "ui_ux"}
        ]
      }
    ]
  }
}
```

---

### 3.3 Submit Assessment

Submit answers and get results with course recommendations.

```http
POST /assessments/<id>/submit/
```

**Headers**:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**:

```json
{
  "answers": [
    {"question_id": 1, "selected_option": "yes_love"},
    {"question_id": 2, "selected_option": "web_dev"},
    {"question_id": 3, "selected_option": "team_work"}
  ]
}
```

**Response (201 Created)**:

```json
{
  "success": true,
  "data": {
    "id": 15,
    "assessment": {
      "id": 1,
      "title": "Tech Career Path Finder"
    },
    "score": 85,
    "category_scores": {
      "programming": 90,
      "data_analysis": 45,
      "security": 30,
      "design": 60
    },
    "recommended_courses": [
      {
        "course": {
          "id": 1,
          "title": "MERN Stack Development",
          "category": "Web Development"
        },
        "match_score": 92,
        "reason": "Your answers show strong programming aptitude and interest in web development."
      },
      {
        "course": {
          "id": 3,
          "title": "Django Web Framework",
          "category": "Web Development"
        },
        "match_score": 78,
        "reason": "You enjoy backend logic and Python ecosystem."
      }
    ],
    "completed_at": "2026-07-14T10:30:00Z"
  },
  "message": "Assessment submitted successfully"
}
```

---

### 3.4 Get My Assessment Results

Get all assessment results for the current student.

```http
GET /assessments/results/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": [
    {
      "id": 15,
      "assessment_title": "Tech Career Path Finder",
      "score": 85,
      "completed_at": "2026-07-14T10:30:00Z",
      "top_recommendation": {
        "course_title": "MERN Stack Development",
        "match_score": 92
      }
    }
  ]
}
```

---

## 4. Counseling Endpoints

### 4.1 Request Counseling Session

Book a session with a staff counselor.

```http
POST /counseling/request/
```

**Headers**:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**:

```json
{
  "preferred_date": "2026-07-20",
  "preferred_time": "14:00",
  "notes": "I'm confused between MERN Stack and Django. Need guidance on job market in Nepal."
}
```

**Response (201 Created)**:

```json
{
  "success": true,
  "data": {
    "id": 7,
    "student": {
      "id": 1,
      "name": "John Doe"
    },
    "scheduled_at": "2026-07-20T14:00:00Z",
    "status": "scheduled",
    "notes": "I'm confused between MERN Stack and Django...",
    "counselor": null,
    "created_at": "2026-07-14T10:45:00Z"
  },
  "message": "Counseling session requested successfully"
}
```

---

### 4.2 List My Sessions

Get all counseling sessions for the current student.

```http
GET /counseling/sessions/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": [
    {
      "id": 7,
      "scheduled_at": "2026-07-20T14:00:00Z",
      "status": "scheduled",
      "counselor": {
        "id": 5,
        "name": "Priya Karki",
        "role": "staff"
      },
      "notes": "I'm confused between MERN Stack and Django...",
      "recommended_courses": []
    }
  ]
}
```

---

### 4.3 Complete Session (Staff Only)

Mark a counseling session as completed with notes and recommendations.

```http
POST /counseling/sessions/<id>/complete/
```

**Headers**:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**:

```json
{
  "notes": "Student has strong JavaScript background. Recommended MERN Stack due to higher job demand in Kathmandu.",
  "recommended_courses": [1, 3]
}
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "id": 7,
    "status": "completed",
    "notes": "Student has strong JavaScript background...",
    "recommended_courses": [
      {
        "id": 1,
        "title": "MERN Stack Development"
      },
      {
        "id": 3,
        "title": "Django Web Framework"
      }
    ]
  },
  "message": "Session marked as completed"
}
```

---

### 4.4 Get My Recommendations

Get AI-generated course recommendations based on assessment.

```http
GET /counseling/recommendations/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": [
    {
      "id": 12,
      "course": {
        "id": 1,
        "title": "MERN Stack Development",
        "category": "Web Development",
        "level": "intermediate",
        "duration_weeks": 12,
        "price": 25000
      },
      "match_score": 92,
      "reason": {
        "skill_alignment": "Your programming aptitude (90%) aligns with this course's requirements",
        "interest_match": "You showed high interest in web development",
        "career_goal": "Matches your goal of becoming a Full Stack Developer",
        "market_demand": "High demand for MERN developers in Nepal"
      },
      "is_accepted": false,
      "created_at": "2026-07-14T10:30:00Z"
    },
    {
      "id": 13,
      "course": {
        "id": 5,
        "title": "Python for Data Science",
        "category": "Data Science",
        "level": "beginner",
        "duration_weeks": 8,
        "price": 20000
      },
      "match_score": 65,
      "reason": {
        "skill_alignment": "Good Python foundation detected",
        "interest_match": "Moderate interest in data analysis"
      },
      "is_accepted": false,
      "created_at": "2026-07-14T10:30:00Z"
    }
  ]
}
```

---

### 4.5 Accept Recommendation

Accept a course recommendation to proceed with enrollment.

```http
POST /counseling/recommendations/<id>/accept/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "id": 12,
    "course": {
      "id": 1,
      "title": "MERN Stack Development"
    },
    "is_accepted": true,
    "accepted_at": "2026-07-14T11:00:00Z"
  },
  "message": "Recommendation accepted. Proceed to enrollment."
}
```

---

## 5. Enrollment Endpoints

### 5.1 Create Enrollment

Enroll in a specific course batch.

```http
POST /enrollments/
```

**Headers**:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**:

```json
{
  "course_batch": 1,
  "payment_method": "esewa"
}
```

**Response (201 Created)**:

```json
{
  "success": true,
  "data": {
    "id": 20,
    "student": {
      "id": 1,
      "name": "John Doe"
    },
    "course_batch": {
      "id": 1,
      "course": {
        "id": 1,
        "title": "MERN Stack Development"
      },
      "start_date": "2026-08-01",
      "end_date": "2026-10-24"
    },
    "status": "pending",
    "payment_status": "pending",
    "enrolled_at": "2026-07-14T11:15:00Z"
  },
  "message": "Enrollment created. Please complete payment to confirm."
}
```

---

### 5.2 List My Enrollments

Get all enrollments for the current student.

```http
GET /enrollments/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": [
    {
      "id": 20,
      "course": {
        "id": 1,
        "title": "MERN Stack Development"
      },
      "batch": {
        "start_date": "2026-08-01",
        "end_date": "2026-10-24",
        "schedule": {
          "days": ["Sunday", "Tuesday", "Thursday"],
          "time": "07:00 - 09:00"
        }
      },
      "status": "confirmed",
      "payment_status": "completed",
      "enrolled_at": "2026-07-14T11:15:00Z",
      "progress": {
        "overall_completion": 0,
        "modules_completed": 0,
        "total_modules": 12
      }
    }
  ]
}
```

---

### 5.3 Get Enrollment Detail

Get detailed information about a specific enrollment.

```http
GET /enrollments/<id>/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "id": 20,
    "course": {
      "id": 1,
      "title": "MERN Stack Development",
      "description": "Complete full-stack development...",
      "instructor_name": "Rajesh Sharma"
    },
    "batch": {
      "start_date": "2026-08-01",
      "end_date": "2026-10-24",
      "max_seats": 25,
      "schedule": {
        "days": ["Sunday", "Tuesday", "Thursday"],
        "time": "07:00 - 09:00"
      }
    },
    "status": "confirmed",
    "payment_status": "completed",
    "enrolled_at": "2026-07-14T11:15:00Z"
  }
}
```

---

### 5.4 Get Progress

Get detailed progress for an enrollment.

```http
GET /enrollments/<id>/progress/
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "enrollment_id": 20,
    "course_title": "MERN Stack Development",
    "overall_completion": 25,
    "last_accessed": "2026-07-20T09:30:00Z",
    "modules": [
      {
        "name": "JavaScript ES6+ Review",
        "completed": true,
        "completed_at": "2026-07-18",
        "duration_hours": 6
      },
      {
        "name": "Node.js & Express",
        "completed": true,
        "completed_at": "2026-07-20",
        "duration_hours": 8
      },
      {
        "name": "MongoDB & Mongoose",
        "completed": false,
        "completed_at": null,
        "duration_hours": 8
      },
      {
        "name": "React Fundamentals",
        "completed": false,
        "completed_at": null,
        "duration_hours": 10
      }
    ]
  }
}
```

---

### 5.5 Update Progress

Mark a module as completed or update overall progress.

```http
PATCH /enrollments/<id>/progress/
```

**Headers**:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**:

```json
{
  "module_name": "MongoDB & Mongoose",
  "completed": true
}
```

**Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "enrollment_id": 20,
    "overall_completion": 33,
    "modules_completed": 3,
    "total_modules": 12,
    "updated_module": {
      "name": "MongoDB & Mongoose",
      "completed": true,
      "completed_at": "2026-07-21T10:00:00Z"
    }
  },
  "message": "Progress updated successfully"
}
```

---

## Error Reference

### Common Error Codes

| Code | Message | HTTP Status |
|------|---------|-------------|
| `VALIDATION_ERROR` | Invalid input data | 400 |
| `AUTHENTICATION_FAILED` | Invalid credentials | 401 |
| `TOKEN_EXPIRED` | Access token has expired | 401 |
| `PERMISSION_DENIED` | Insufficient permissions | 403 |
| `RESOURCE_NOT_FOUND` | Requested resource not found | 404 |
| `METHOD_NOT_ALLOWED` | HTTP method not allowed | 405 |
| `RATE_LIMITED` | Too many requests | 429 |
| `INTERNAL_ERROR` | Something went wrong | 500 |

### Validation Error Example

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["This field is required."],
      "password": ["Password must be at least 8 characters."],
      "phone": ["Phone number already exists."]
    }
  }
}
```

---

## Rate Limiting

| Endpoint Group | Limit | Window |
|----------------|-------|--------|
| Authentication | 5 requests | 1 minute |
| All other endpoints | 100 requests | 1 minute |

---

*Document Version: 1.0 | Last Updated: 2026-07-14*
