# 🎓 Student Management System with AI Integration

An AI-powered Student Management System built using **FastAPI**, **SQLAlchemy**, and **SQLite**.  
The project provides complete student management functionalities along with analytics, AI-generated insights, caching, logging, rate limiting, and testing support.

---

# 🚀 Features

## 📚 Student Management
- Add students with subject-wise marks
- Update student records and marks
- Delete student records
- Fetch single student details
- Fetch all students with pagination

---

## 📊 Analytics
- Get class topper
- Generate rank list
- Calculate class average
- Dashboard statistics
- Subject-wise analysis
- Pass/Fail filtering

---

## 🤖 AI Features
- AI-generated student insights
- AI-powered academic chatbot
- AI-generated class performance report
- Restricted academic query handling
- Prompt validation and response formatting

---

## ⚡ Performance & Security
- In-memory caching
- Request logging middleware
- Rate limiting middleware
- Global exception handling
- Optimistic locking using versioning

---

## 🧪 Testing
- Pytest unit testing
- In-memory SQLite testing
- Audit log validation

---

# 🛠️ Tech Stack

## Backend
- FastAPI
- Python
- SQLAlchemy
- SQLite

## AI Integration
- ASI1 AI API

## Testing
- Pytest

---

# 📁 Project Structure

```bash
student-management-system/
│
├── app/
│   ├── api.py
│   └── database.py
│
├── middleware/
│   ├── logging_middleware.py
│   └── rate_limit.py
│
├── models/
│   ├── student.py
│   ├── student_marks.py
│   ├── subject.py
│   └── audit_log.py
│
├── schemas/
│   └── student_schema.py
│
├── services/
│   ├── ai_service.py
│   ├── report_service.py
│   └── student_service.py
│
├── utils/
│   ├── cache.py
│   └── response.py
│
├── tests/
│   └── test_student_service.py
│
├── students.db
├── student_management.log
├── .env
├── init_db.py
├── pytest.ini
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/apurvagarg19/student-management-system-v4.git
cd student-management-system-v4
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 3️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
ASI1_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./students.db
```

---

# 🗄️ Initialize Database

```bash
python init_db.py
```

---

# ▶️ Run Application

```bash
uvicorn app.api:app --reload
```

Application will run at:

```bash
http://127.0.0.1:8000
```

Swagger Documentation:

```bash
http://127.0.0.1:8000/docs
```

---

# 📌 API Endpoints

## 👨‍🎓 Student APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students` | Add student |
| GET | `/students` | Get all students |
| GET | `/students/{student_id}` | Get student by ID |
| PUT | `/students/{student_id}` | Update student |
| DELETE | `/students/{student_id}` | Delete student |

---

## 📈 Analytics APIs

| Method | Endpoint |
|---|---|
| GET | `/students/topper` |
| GET | `/students/average` |
| GET | `/students/rank-list` |
| GET | `/students/dashboard` |
| GET | `/students/subject-analysis` |

---

## 🤖 AI APIs

| Method | Endpoint |
|---|---|
| GET | `/students/{student_id}/insights` |
| POST | `/ai/query` |
| POST | `/ai/chat` |
| GET | `/ai/report` |

---

# 📥 Sample Request

## Add Student

```json
{
  "student_id": "S101",
  "name": "Apurva",
  "marks": {
    "math": 90,
    "science": 85,
    "english": 88
  }
}
```

---

# 🤖 Sample AI Response

```json
{
  "summary": "The student is performing consistently well academically.",
  "strengths": [
    "Strong analytical skills",
    "Excellent performance in Mathematics"
  ],
  "weaknesses": [
    "Needs improvement in Science"
  ],
  "suggestions": [
    "Practice more numerical problems",
    "Improve conceptual understanding"
  ]
}
```

---

# ✨ Recent Enhancements

- Added AI-powered academic chatbot
- Implemented AI-generated student insights
- Added AI class performance report generation
- Implemented caching for AI responses
- Added request logging middleware
- Added rate limiting middleware
- Improved API response handling
- Added optimistic locking using version control
- Added pytest unit testing support

---

# 🧪 Run Tests

```bash
pytest
```

---

# 🧠 Key Concepts Used

- FastAPI Dependency Injection
- SQLAlchemy ORM
- REST API Development
- Middleware Handling
- AI Prompt Engineering
- Pagination & Filtering
- Optimistic Locking
- Caching Mechanism
- Exception Handling
- Unit Testing

---

# 👨‍💻 Author

**Apurva Garg**

GitHub:  
https://github.com/apurvagarg19

---
