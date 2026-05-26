import streamlit as st
import requests
import pandas as pd

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="NovaMind Student System",
    page_icon="🎓",
    layout="wide"
)

BASE_URL = "http://127.0.0.1:8000"

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.stButton>button {
    background-color: #4F46E5;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #3730A3;
    color: white;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.metric-card {
    background: linear-gradient(135deg,#6366F1,#8B5CF6);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
}

.title {
    font-size: 40px;
    font-weight: bold;
    color: #111827;
}

.subtitle {
    color: #6B7280;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.markdown(
    """
    <div class='title'>🎓 NovaMind Student Management</div>
    <div class='subtitle'>
    AI Powered Student Analytics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# ---------------- SIDEBAR ----------------

menu = st.sidebar.radio(
    "📚 Navigation",
    [
        "🏠 Dashboard",
        "➕ Add Student",
        "📋 View Students",
        "🔍 Search / Filter",
        "🏆 Rank List",
        "🤖 AI Insights"
    ]
)

# ---------------- DASHBOARD ----------------

if menu == "🏠 Dashboard":

    st.subheader("📊 Dashboard Overview")

    try:

        response = requests.get(
            f"{BASE_URL}/students/dashboard"
        )

        data = response.json()

        if data["success"]:

            dashboard = data["data"]

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>👨‍🎓</h2>
                    <h1>{dashboard['total_students']}</h1>
                    <p>Total Students</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>📈</h2>
                    <h1>{dashboard['average_percentage']:.2f}%</h1>
                    <p>Average Percentage</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>✅</h2>
                    <h1>{dashboard['pass_percentage']:.2f}%</h1>
                    <p>Pass Percentage</p>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>🏆</h2>
                    <h1>{dashboard['topper']}</h1>
                    <p>Topper</p>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(str(e))

# ---------------- ADD STUDENT ----------------

elif menu == "➕ Add Student":

    st.subheader("➕ Add New Student")

    student_id = st.text_input("🆔 Student ID").upper()
    name = st.text_input("👤 Student Name")

    st.markdown("### 📚 Add Subjects & Marks")

    # Session state for dynamic subjects
    if "subjects" not in st.session_state:
        st.session_state.subjects = []

    col1, col2 = st.columns([3, 1])

    with col1:
        subject_name = st.text_input(
            "Subject Name",
            key="subject_input"
        )

    with col2:
        marks = st.number_input(
            "Marks",
            0,
            100,
            0,
            key="marks_input"
        )

    # Add subject button
    if st.button("➕ Add Subject"):

        if subject_name.strip() == "":
            st.warning("Enter subject name")

        else:

            st.session_state.subjects.append({
                "subject": subject_name,
                "marks": marks
            })

            st.success(
                f"{subject_name} added successfully"
            )

    st.write("")

    # Show added subjects
    if st.session_state.subjects:

        st.markdown("### 📝 Added Subjects")

        for i, item in enumerate(
            st.session_state.subjects
        ):

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                st.info(f"📘 {item['subject']}")

            with col2:
                st.success(f"Marks: {item['marks']}")

            with col3:

                if st.button(
                    "❌",
                    key=f"delete_{i}"
                ):

                    st.session_state.subjects.pop(i)
                    st.rerun()

    st.write("")

    # Final submit
    if st.button("🚀 Create Student"):

        if not student_id or not name:

            st.error(
                "Student ID and Name required"
            )

        elif not st.session_state.subjects:

            st.error(
                "Add at least one subject"
            )

        else:

            marks_dict = {}

            for item in st.session_state.subjects:

                marks_dict[item["subject"]] = (
                    item["marks"]
                )

            payload = {
                "student_id": student_id,
                "name": name,
                "marks": marks_dict
            }

            try:

                response = requests.post(
                    f"{BASE_URL}/students",
                    json=payload
                )

                data = response.json()

                if data["success"]:

                    st.success(
                        "✅ Student Added Successfully"
                    )

                    st.balloons()

                    # clear subjects
                    st.session_state.subjects = []

                else:
                    st.error(data["message"])

            except Exception as e:
                st.error(str(e))

# ---------------- VIEW STUDENTS ----------------

elif menu == "📋 View Students":

    st.subheader("📋 Student Records")

    try:

        response = requests.get(
            f"{BASE_URL}/students"
        )

        data = response.json()

        if data["success"]:

            students = data["data"]["students"]

            if students:

                df = pd.DataFrame([
                    {
                        "ID": s["student_id"],
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

            else:
                st.warning("No students found")

    except Exception as e:
        st.error(str(e))

# ---------------- SEARCH ----------------

elif menu == "🔍 Search / Filter":

    st.subheader("🔍 Search Students")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Search by Name")

    with col2:
        grade = st.selectbox(
            "Select Grade",
            ["", "A", "B", "C", "D", "F"]
        )

    min_percentage = st.slider(
        "Minimum Percentage",
        0,
        100,
        0
    )

    if st.button("🔎 Search"):

        params = {
            "name": name,
            "grade": grade if grade else None,
            "min_percentage": min_percentage
        }

        try:

            response = requests.get(
                f"{BASE_URL}/students",
                params=params
            )

            data = response.json()

            if data["success"]:

                students = data["data"]["students"]

                if students:

                    df = pd.DataFrame([
                        {
                            "ID": s["student_id"],
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

                else:
                    st.warning("No matching students found")

        except Exception as e:
            st.error(str(e))

# ---------------- RANK LIST ----------------

elif menu == "🏆 Rank List":

    st.subheader("🏆 Student Leaderboard")

    try:

        response = requests.get(
            f"{BASE_URL}/students/rank-list"
        )

        data = response.json()

        if data["success"]:

            students = data["data"]

            rank_data = []

            for i, s in enumerate(students, start=1):

                medal = "🥇"

                if i == 2:
                    medal = "🥈"

                elif i == 3:
                    medal = "🥉"

                rank_data.append({
                    "Rank": f"{medal} {i}",
                    "Name": s["name"],
                    "Percentage": f"{s['percentage']:.2f}%",
                    "Grade": s["grade"]
                })

            df = pd.DataFrame(rank_data)

            st.dataframe(
                df,
                use_container_width=True
            )

    except Exception as e:
        st.error(str(e))

# ---------------- AI INSIGHTS ----------------

elif menu == "🤖 AI Insights":

    st.subheader("🤖 AI Performance Insights")

    student_id = st.text_input(
        "Enter Student ID"
    )

    if st.button("✨ Generate AI Insights"):

        try:

            response = requests.get(
                f"{BASE_URL}/students/{student_id}/insights"
            )

            data = response.json()

            if data["success"]:

                insights = data["data"]

                st.markdown("""
                <div class='card'>
                """, unsafe_allow_html=True)

                st.subheader("📄 Summary")
                st.write(insights.get("summary"))

                st.subheader("💪 Strengths")

                for item in insights.get("strengths", []):
                    st.success(item)

                st.subheader("⚠ Weaknesses")

                for item in insights.get("weaknesses", []):
                    st.warning(item)

                st.subheader("💡 Suggestions")

                for item in insights.get("suggestions", []):
                    st.info(item)

                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.error(data["message"])

        except Exception as e:
            st.error(str(e))
