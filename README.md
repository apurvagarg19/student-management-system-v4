# 🎓 NovaMind Student Management System

An AI-powered Student Management System built using **FastAPI**, **SQLAlchemy**, **SQLite**, and **Streamlit**.

This project provides complete student record management with:
- Dashboard analytics
- AI-powered insights
- Ranking systems
- Search & filtering
- Subject-wise analysis
- Interactive frontend UI

---

# 🚀 Features

## ✅ Backend Features (FastAPI)

- Add Students
- Update Student Records
- Delete Students
- View Student Details
- Pagination Support
- Search & Filtering
- Grade Calculation
- Rank List Generation
- Subject-wise Analytics
- Dashboard Analytics
- Global Exception Handling
- Middleware Logging
- Rate Limiting
- Caching Support
- Audit Logging
- Unit Testing with Pytest
- AI-powered Insights

---

## 🎨 Frontend Features (Streamlit)

- Interactive Dashboard
- Add Student UI
- View Student Records
- Search & Filter Students
- Rank Leaderboard
- AI Insights Interface
- Responsive UI
- Custom CSS Styling

---

# 🤖 AI Features

Integrated AI analytics using external AI API.

Supports:
- Student Performance Summary
- Strength Analysis
- Weakness Detection
- Improvement Suggestions
- AI Chat Queries
- AI-generated Reports

---

# 🛠️ Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Frontend
- Streamlit
- Pandas

## AI Integration
- Requests API
- External AI Service

## Testing
- Pytest

---

# 📂 Project Structure

```bash
student-management-system/
│
├── app/
│   ├── api.py
│   ├── database.py
│
├── middleware/
│   ├── logging_middleware.py
│   ├── rate_limit.py
│
├── models/
│   ├── student.py
│   ├── subject.py
│   ├── student_marks.py
│   ├── audit_log.py
│
├── schemas/
│   ├── student_schema.py
│
├── services/
│   ├── student_service.py
│   ├── ai_service.py
│   ├── report_service.py
│
├── tests/
│   ├── test_student_service.py
│
├── utils/
│   ├── cache.py
│   ├── response.py
│
├── streamlit_app.py
├── init_db.py
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
```

---

# ⚙️ Installation Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/student-management-system.git
```

```bash
cd student-management-system
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
.\venv\Scripts\Activate.ps1
```

### Linux / Mac

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the root directory.

Example:

```env
ASI1_API_KEY=your_api_key_here
```

---

# 🗄️ Initialize Database

Run:

```bash
python init_db.py
```

This creates:
- students table
- subjects table
- student_marks table
- audit_logs table

---

# ▶️ Run Backend Server

```bash
uvicorn app.api:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🎨 Run Streamlit Frontend

```bash
streamlit run streamlit_app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# 📊 Dashboard Analytics

The dashboard provides:

- Total Students
- Pass Percentage
- Average Percentage
- Grade Distribution
- Top Performer

---

# 🔍 Search & Filtering

Supports:
- Search by Name
- Grade Filtering
- Percentage Filtering
- Failed Student Filtering

---

# 🏆 Ranking System

Students are ranked based on:
- Percentage
- Alphabetical order (tie-breaker)

---

# 🧪 Run Tests

```bash
pytest
```

---

# 📌 API Endpoints

## Student APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Add student |
| GET | `/students` | Get all students |
| GET | `/students/{student_id}` | Get single student |
| PUT | `/students/{student_id}` | Update student |
| DELETE | `/students/{student_id}` | Delete student |

---

## Analytics APIs

| Method | Endpoint |
|--------|----------|
| GET | `/students/topper` |
| GET | `/students/average` |
| GET | `/students/rank-list` |
| GET | `/students/dashboard` |
| GET | `/students/subject-analysis` |

---

## AI APIs

| Method | Endpoint |
|--------|----------|
| GET | `/students/{student_id}/insights` |
| POST | `/ai/query` |
| POST | `/ai/chat` |
| GET | `/ai/report` |

---

# 🧠 Key Concepts Used

- REST API Design
- ORM Relationships
- Middleware
- Dependency Injection
- Exception Handling
- Pagination
- Caching
- Rate Limiting
- AI Integration
- Unit Testing
- Analytics Processing

---

# 🔒 Security Features

- Request Validation
- Input Validation
- Rate Limiting
- Exception Handling

---

# 👨‍💻 Author

### Apurva Garg
