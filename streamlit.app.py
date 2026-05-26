import streamlit as st
import requests
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NovaMind Student System",
    page_icon="🎓",
    layout="wide"
)
BASE_URL = "https://student-management-system-kegr.onrender.com"

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

section[data-testid="stSidebar"] h1 {
    font-size: 26px !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] p {
    font-size: 18px !important;
    font-weight: 500 !important;
}

.title {
    font-size: 42px !important;
    font-weight: 800 !important;
    color: #111827;
    margin-bottom: 1rem;
}

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-bottom: 2rem;
    max-width: 100%! important;
}

div[data-testid="stHorizontalBlock"] > div {
    width: 100% !important;
}

div[data-testid="column"] {
    width: 100% !important;
}


section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #ddd;
}

.card {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    padding: 35px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 52px;
    font-weight: 800;
}

.metric-label {
    font-size: 20px;
    margin-top: 8px;
}

.student-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

.subject-box {
    background: #EEF2FF;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}

.stButton>button {
    background-color: #4F46E5;
    color: white;
    border-radius: 10px;
    border: none;
    height: 3em;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #3730A3;
    color: white;
}

.title {
    font-size: 56px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 1rem;
    line-height: 1.2;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# API HELPER
# =========================================================

def api_get(endpoint):

    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=30)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return {}

def api_post(endpoint, payload):

    try:
        response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=payload,timeout=30
    )
        return response
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None



# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Navigation")

menu = st.sidebar.radio(
    "Go To",
    [
        "🏠 Dashboard",
        "➕ Add Student",
        "👨‍🎓 View Students",
        "🔍 Search Students",
        "🏆 Rank List",
        "🧠 AI Insights"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown(
        '<p class="title">📊 Dashboard</p>',
        unsafe_allow_html=True
    )

    try:

        result = api_get("/students/dashboard")

        dashboard = result.get("data", {})

        total_students = dashboard.get("total_students", 0)
        pass_percentage = dashboard.get("pass_percentage", 0)
        average_percentage = dashboard.get("average_percentage", 0)
        topper = dashboard.get("topper", "N/A")
        grades = dashboard.get("grades", {})

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="metric-value">{total_students}</div>
                <div class="metric-label">Students</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="metric-value">{pass_percentage}%</div>
                <div class="metric-label">Pass Rate</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="metric-value">{average_percentage}%</div>
                <div class="metric-label">Average</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="card">
                <div class="metric-value">🏆</div>
                <div class="metric-label">{topper}</div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("📈 Grade Distribution")

        grade_df = pd.DataFrame({
            "Grade": list(grades.keys()),
            "Count": list(grades.values())
        })

        st.bar_chart(grade_df.set_index("Grade"))

    except Exception as e:
        st.error(str(e))

# =========================================================
# ADD STUDENT
# =========================================================

elif menu == "➕ Add Student":

    st.markdown(
        '<p class="title">➕ Add Student</p>',
        unsafe_allow_html=True
    )

    student_id = st.text_input("Student ID")
    student_name = st.text_input("Student Name")

    st.subheader("📚 Subjects")

    count = st.number_input(
        "Number of Subjects",
        min_value=1,
        max_value=10,
        value=3
    )

    marks_dict = {}

    for i in range(count):

        col1, col2 = st.columns(2)

        with col1:
            subject = st.text_input(
                f"Subject {i+1}",
                key=f"sub{i}"
            )

        with col2:
            marks = st.number_input(
                f"Marks {i+1}",
                min_value=0,
                max_value=100,
                key=f"marks{i}"
            )

        if subject:
            marks_dict[subject] = marks

    if st.button("Create Student"):

        payload = {
            "student_id": student_id,
            "name": student_name,
            "marks": marks_dict
        }

        response = api_post(
            "/students",
            payload
        )

        result = response.json()

        if response.status_code in [200, 201]:
            st.success("✅ Student Added Successfully")
        else:
            st.error(result.get("message"))

# =========================================================
# VIEW STUDENTS
# =========================================================

elif menu == "👨‍🎓 View Students":

    st.markdown(
        '<p class="title">👨‍🎓 Student Records</p>',
        unsafe_allow_html=True
    )

    try:

        result = api_get("/students")

        students = result.get("data", {}).get("students", [])

        if not students:
            st.warning("No students found")

        for student in students:

            st.markdown(
                '<div class="student-box">',
                unsafe_allow_html=True
            )

            st.subheader(student["name"])

            st.write(f"🆔 ID: {student['student_id']}")
            st.write(f"📊 Percentage: {student['percentage']}%")
            st.write(f"🏆 Grade: {student['grade']}")

            st.write("### Subjects")

            for subject in student["marks"]:

                st.markdown(f"""
                <div class="subject-box">
                    {subject['subject']} : {subject['marks']}
                </div>
                """, unsafe_allow_html=True)

            if st.button(
                f"Delete {student['student_id']}",
                key=student['student_id']
            ):

                requests.delete(
                    f"{BASE_URL}/students/{student['student_id']}"
                )

                st.success("Student Deleted")
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(str(e))

# =========================================================
# SEARCH
# =========================================================

elif menu == "🔍 Search Students":

    st.markdown(
        '<p class="title">🔍 Search Students</p>',
        unsafe_allow_html=True
    )

    search_name = st.text_input("Search by Name")

    grade = st.selectbox(
        "Grade",
        ["All", "A", "B", "C", "D", "F"]
    )

    minimum = st.slider(
        "Minimum Percentage",
        0,
        100,
        0
    )

    if st.button("Search"):

        params = {
            "name": search_name,
            "min_percentage": minimum
        }

        if grade != "All":
            params["grade"] = grade

        response = requests.get(
            f"{BASE_URL}/students",
            params=params
        )

        result = response.json()

        students = result.get("data", {}).get("students", [])

        if not students:
            st.warning("No students found")

        else:

            df = pd.DataFrame([
                {
                    "Student ID": s["student_id"],
                    "Name": s["name"],
                    "Percentage": s["percentage"],
                    "Grade": s["grade"]
                }
                for s in students
            ])

            st.dataframe(
                df,
                use_container_width=True
            )

# =========================================================
# RANK LIST
# =========================================================

elif menu == "🏆 Rank List":

    st.markdown(
        '<p class="title">🏆 Rank List</p>',
        unsafe_allow_html=True
    )

    try:

        result = api_get("/students/rank-list")

        students = result.get("data", [])

        df = pd.DataFrame([
            {
                "Rank": i + 1,
                "Student ID": s["student_id"],
                "Name": s["name"],
                "Percentage": s["percentage"],
                "Grade": s["grade"]
            }
            for i, s in enumerate(students)
        ])

        st.dataframe(
            df,
            use_container_width=True
        )

    except Exception as e:
        st.error(str(e))

# =========================================================
# AI INSIGHTS
# =========================================================

elif menu == "🧠 AI Insights":

    st.markdown(
        '<p class="title">🧠 AI Insights</p>',
        unsafe_allow_html=True
    )

    student_id = st.text_input("Enter Student ID")

    if st.button("Generate AI Insights"):

        try:

            result = api_get(
                f"/students/{student_id}/insights"
            )

            analysis = result.get("data", {})

            st.subheader("📝 Summary")

            st.info(
                analysis.get(
                    "summary",
                    "No summary available"
                )
            )

            st.subheader("💪 Strengths")

            for item in analysis.get("strengths", []):
                st.success(item)

            st.subheader("⚠ Weaknesses")

            for item in analysis.get("weaknesses", []):
                st.warning(item)

            st.subheader("📌 Suggestions")

            for item in analysis.get("suggestions", []):
                st.write("✅", item)

        except Exception as e:
            st.error(str(e))