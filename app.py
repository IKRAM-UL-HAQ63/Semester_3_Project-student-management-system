import json
import os
import pandas as pd
import streamlit as st
from datetime import datetime, date, time
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

# ------------------- FILE PATHS -------------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")
ENROLLMENTS_FILE = os.path.join(DATA_DIR, "enrollments.json")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.json")
GRADES_FILE = os.path.join(DATA_DIR, "grades.json")
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.json")
TIMETABLE_FILE = os.path.join(DATA_DIR, "timetable.json")

# ------------------- DATA FUNCTIONS -------------------
def load_data(filename):
    """Load JSON data safely"""
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(filename, data):
    """Save data to JSON"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def init_sample_data():
    """Initialize with sample data"""
    if not load_data(STUDENTS_FILE):
        sample_students = [
            {"id": "S001", "name": "John Doe", "roll_no": "2024001", 
             "email": "john@email.com", "phone": "1234567890", 
             "program": "Computer Science", "status": "Active",
             "address": "123 Main St", "dob": "2000-01-01"},
            {"id": "S002", "name": "Jane Smith", "roll_no": "2024002",
             "email": "jane@email.com", "phone": "0987654321",
             "program": "Engineering", "status": "Active",
             "address": "456 Oak Ave", "dob": "2000-02-15"}
        ]
        save_data(STUDENTS_FILE, sample_students)
    
    if not load_data(COURSES_FILE):
        sample_courses = [
            {"code": "CS101", "name": "Programming Basics", "credits": 3, 
             "instructor": "Dr. Smith", "department": "Computer Science"},
            {"code": "MATH101", "name": "Calculus I", "credits": 4, 
             "instructor": "Prof. Johnson", "department": "Mathematics"},
            {"code": "ENG101", "name": "English Composition", "credits": 3,
             "instructor": "Prof. Williams", "department": "English"},
            {"code": "PHY101", "name": "Physics I", "credits": 4,
             "instructor": "Dr. Brown", "department": "Physics"},
            {"code": "BUS101", "name": "Introduction to Business", "credits": 3,
             "instructor": "Prof. Davis", "department": "Business"}
        ]
        save_data(COURSES_FILE, sample_courses)
    
    if not load_data(TIMETABLE_FILE):
        sample_timetable = [
            {"course_code": "CS101", "course_name": "Programming Basics",
             "day": "Monday", "start_time": "09:00", "end_time": "10:30",
             "room": "Room 101", "instructor": "Dr. Smith", "type": "Lecture"},
            {"course_code": "CS101", "course_name": "Programming Basics",
             "day": "Wednesday", "start_time": "09:00", "end_time": "10:30",
             "room": "Room 101", "instructor": "Dr. Smith", "type": "Lecture"},
            {"course_code": "MATH101", "course_name": "Calculus I",
             "day": "Tuesday", "start_time": "11:00", "end_time": "12:30",
             "room": "Room 201", "instructor": "Prof. Johnson", "type": "Lecture"},
            {"course_code": "ENG101", "course_name": "English Composition",
             "day": "Thursday", "start_time": "14:00", "end_time": "15:30",
             "room": "Room 301", "instructor": "Prof. Williams", "type": "Lecture"}
        ]
        save_data(TIMETABLE_FILE, sample_timetable)

def safe_get(data, key, default=""):
    """Safely get value from dictionary"""
    if isinstance(data, dict):
        return data.get(key, default)
    return default

def calculate_grade(marks):
    """Calculate grade from marks"""
    try:
        marks = float(marks)
        if marks >= 90: return "A"
        elif marks >= 80: return "B"
        elif marks >= 70: return "C"
        elif marks >= 60: return "D"
        else: return "F"
    except:
        return "F"

def calculate_gpa(grade):
    """Calculate GPA from grade"""
    grade_points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
    return grade_points.get(grade, 0.0)

def calculate_cgpa(grades_list):
    """Calculate CGPA from list of grades"""
    if not grades_list:
        return 0.0
    total_points = sum(calculate_gpa(grade) for grade in grades_list)
    return total_points / len(grades_list)

# ------------------- IMPORT/EXPORT FUNCTIONS -------------------
def import_dataframe(df, data_type):
    """Import data from DataFrame"""
    try:
        df = df.where(pd.notnull(df), None)
        
        if data_type == "Students":
            required_cols = ['name', 'roll_no']
            if not all(col in df.columns for col in required_cols):
                return False, f"Missing required columns. Need: {required_cols}"
            
            current_data = load_data(STUDENTS_FILE)
            imported = df.to_dict('records')
            
            # Add IDs if not present
            for i, record in enumerate(imported):
                if 'id' not in record:
                    record['id'] = f"S{len(current_data) + i + 1:03d}"
                if 'status' not in record:
                    record['status'] = 'Active'
                if 'created' not in record:
                    record['created'] = str(date.today())
            
            current_data.extend(imported)
            save_data(STUDENTS_FILE, current_data)
            return True, f"Successfully imported {len(imported)} students"
            
        elif data_type == "Courses":
            required_cols = ['code', 'name']
            if not all(col in df.columns for col in required_cols):
                return False, f"Missing required columns. Need: {required_cols}"
            
            current_data = load_data(COURSES_FILE)
            imported = df.to_dict('records')
            current_data.extend(imported)
            save_data(COURSES_FILE, current_data)
            return True, f"Successfully imported {len(imported)} courses"
            
        elif data_type == "Timetable":
            required_cols = ['course_code', 'day', 'start_time']
            if not all(col in df.columns for col in required_cols):
                return False, f"Missing required columns. Need: {required_cols}"
            
            current_data = load_data(TIMETABLE_FILE)
            imported = df.to_dict('records')
            current_data.extend(imported)
            save_data(TIMETABLE_FILE, current_data)
            return True, f"Successfully imported {len(imported)} timetable entries"
            
        elif data_type == "Enrollments":
            required_cols = ['student_roll', 'course_code']
            if not all(col in df.columns for col in required_cols):
                return False, f"Missing required columns. Need: {required_cols}"
            
            current_data = load_data(ENROLLMENTS_FILE)
            imported = df.to_dict('records')
            
            # Add date if not present
            for record in imported:
                if 'date' not in record:
                    record['date'] = str(date.today())
                if 'status' not in record:
                    record['status'] = 'Registered'
            
            current_data.extend(imported)
            save_data(ENROLLMENTS_FILE, current_data)
            return True, f"Successfully imported {len(imported)} enrollments"
            
        elif data_type == "Grades":
            required_cols = ['student_roll', 'course_code', 'marks']
            if not all(col in df.columns for col in required_cols):
                return False, f"Missing required columns. Need: {required_cols}"
            
            current_data = load_data(GRADES_FILE)
            imported = df.to_dict('records')
            
            # Calculate grades if not provided
            for record in imported:
                if 'grade' not in record and 'marks' in record:
                    record['grade'] = calculate_grade(record['marks'])
                if 'date' not in record:
                    record['date'] = str(date.today())
            
            current_data.extend(imported)
            save_data(GRADES_FILE, current_data)
            return True, f"Successfully imported {len(imported)} grades"
            
        elif data_type == "Assignments":
            required_cols = ['title', 'course']
            if not all(col in df.columns for col in required_cols):
                return False, f"Missing required columns. Need: {required_cols}"
            
            current_data = load_data(ASSIGNMENTS_FILE)
            imported = df.to_dict('records')
            
            # Add created date if not present
            for record in imported:
                if 'created' not in record:
                    record['created'] = str(date.today())
                if 'due_date' in record:
                    # Convert date if it's string
                    if isinstance(record['due_date'], str):
                        try:
                            record['due_date'] = pd.to_datetime(record['due_date']).strftime('%Y-%m-%d')
                        except:
                            pass
            
            current_data.extend(imported)
            save_data(ASSIGNMENTS_FILE, current_data)
            return True, f"Successfully imported {len(imported)} assignments"
        
        return False, "Unknown data type"
        
    except Exception as e:
        return False, f"Error importing data: {str(e)}"

# ------------------- MAIN APP -------------------
def main():
    st.set_page_config(
        page_title="Student Management System",
        page_icon="🎓",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1e3a8a;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
    }
    .data-table {
        font-size: 0.9rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🎓 Student Management System</h1>', unsafe_allow_html=True)
    
    # Initialize sample data
    init_sample_data()
    
    # Load all data
    students = load_data(STUDENTS_FILE)
    courses = load_data(COURSES_FILE)
    enrollments = load_data(ENROLLMENTS_FILE)
    attendance = load_data(ATTENDANCE_FILE)
    grades = load_data(GRADES_FILE)
    assignments = load_data(ASSIGNMENTS_FILE)
    timetable = load_data(TIMETABLE_FILE)
    
    # ------------------- SIDEBAR -------------------
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=80)
        st.title("Navigation")
        
        feature = st.selectbox(
            "Select Feature",
            ["📊 Dashboard", "👤 Student Profiles", "📚 Course Management", 
             "🎯 Enrollment Tracking", "✅ Attendance", "📝 Grades", 
             "📋 Assignments", "📅 Timetable", "📄 Transcripts", 
             "📈 Performance Reports", "📤 Import Data", "📥 Export Data"]
        )
        
        st.divider()
        
        # Quick stats
        st.subheader("Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Students", len(students))
        with col2:
            st.metric("Courses", len(courses))
        
        if grades:
            total_gpa = sum(calculate_gpa(g.get('grade', 'F')) for g in grades)
            avg_gpa = total_gpa / len(grades) if grades else 0
            st.metric("Avg GPA", f"{avg_gpa:.2f}")
    
    # # ------------------- 1. DASHBOARD -------------------
    # if feature == "📊 Dashboard":
    #     st.header("📊 Dashboard Overview")
        
    #     # Metrics
    #     col1, col2, col3, col4 = st.columns(4)
    #     with col1:
    #         active_students = len([s for s in students if s.get('status') == 'Active'])
    #         st.metric("Active Students", active_students)
    #     with col2:
    #         st.metric("Total Courses", len(courses))
    #     with col3:
    #         st.metric("Enrollments", len(enrollments))
    #     with col4:
    #         pending_assignments = len([a for a in assignments if 'due_date' in a])
    #         st.metric("Assignments", pending_assignments)
        
    #     st.divider()
        
    #     # Quick Actions
    #     st.subheader("🚀 Quick Actions")
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         if st.button("👤 Add New Student", use_container_width=True):
    #             st.session_state.page = "Student Profiles"
    #     with col2:
    #         if st.button("📅 View Timetable", use_container_width=True):
    #             st.session_state.page = "Timetable"
    #     with col3:
    #         if st.button("📈 View Reports", use_container_width=True):
    #             st.session_state.page = "Performance Reports"
        
    #     st.divider()
        
    #     # Recent Activity
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.subheader("📈 Recent Students")
    #         if students:
    #             df_students = pd.DataFrame(students[-5:])
    #             if not df_students.empty:
    #                 st.dataframe(df_students[['name', 'roll_no', 'program', 'status']], 
    #                             use_container_width=True, hide_index=True)
    #         else:
    #             st.info("No students yet")
        
    #     with col2:
    #         st.subheader("📚 Recent Courses")
    #         if courses:
    #             df_courses = pd.DataFrame(courses[-5:])
    #             if not df_courses.empty:
    #                 st.dataframe(df_courses[['code', 'name', 'instructor', 'credits']], 
    #                             use_container_width=True, hide_index=True)
    #         else:
    #             st.info("No courses yet")
    
    # ------------------- 1. DASHBOARD -------------------
    if feature == "📊 Dashboard":
        st.header("📊 Dashboard Overview")
        
        # Metrics with safe data handling
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # Count active students safely
            active_students = 0
            for s in students:
                if isinstance(s, dict) and s.get('status') == 'Active':
                    active_students += 1
            st.metric("Active Students", active_students)
        with col2:
            st.metric("Total Courses", len(courses))
        with col3:
            st.metric("Enrollments", len(enrollments))
        with col4:
            # Count assignments with due dates safely
            pending_assignments = 0
            for a in assignments:
                if isinstance(a, dict) and 'due_date' in a:
                    pending_assignments += 1
            st.metric("Assignments", pending_assignments)
        
        st.divider()
        
        # # Quick Actions
        # st.subheader("🚀 Quick Actions")
        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     if st.button("👤 Add New Student", use_container_width=True):
        #         st.session_state.page = "Student Profiles"
        # with col2:
        #     if st.button("📅 View Timetable", use_container_width=True):
        #         st.session_state.page = "Timetable"
        # with col3:
        #     if st.button("📈 View Reports", use_container_width=True):
        #         st.session_state.page = "Performance Reports"
        
        # st.divider()
        
        # Recent Activity - FIXED VERSION
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Recent Students")
            if students:
                # Create DataFrame safely
                student_data = []
                for s in students[-5:]:  # Last 5 students
                    if isinstance(s, dict):
                        student_data.append({
                            'name': s.get('name', 'Unknown'),
                            'roll_no': s.get('roll_no', 'N/A'),
                            'program': s.get('program', 'N/A'),
                            'status': s.get('status', 'N/A')
                        })
                
                if student_data:
                    df_students = pd.DataFrame(student_data)
                    st.dataframe(df_students, use_container_width=True, hide_index=True)
                else:
                    st.info("No student data available")
            else:
                st.info("No students yet")
        
        with col2:
            st.subheader("📚 Recent Courses")
            if courses:
                # Create DataFrame safely
                course_data = []
                for c in courses[-5:]:  # Last 5 courses
                    if isinstance(c, dict):
                        course_data.append({
                            'code': c.get('code', 'N/A'),
                            'name': c.get('name', 'Unknown'),
                            'instructor': c.get('instructor', 'N/A'),
                            'credits': c.get('credits', 'N/A')
                        })
                
                if course_data:
                    df_courses = pd.DataFrame(course_data)
                    st.dataframe(df_courses, use_container_width=True, hide_index=True)
                else:
                    st.info("No course data available")
            else:
                st.info("No courses yet")
    # ------------------- 2. STUDENT PROFILES -------------------
    elif feature == "👤 Student Profiles":
        st.header("👤 Student Profile Management")
        
        tab1, tab2, tab3 = st.tabs(["Add Student", "View Students", "Search/Filter"])
        
        with tab1:
            with st.form("add_student_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Full Name *", placeholder="Enter full name")
                    roll_no = st.text_input("Roll Number *", placeholder="e.g., 2024001")
                    email = st.text_input("Email *", placeholder="student@email.com")
                    phone = st.text_input("Phone *", placeholder="1234567890")
                
                with col2:
                    program = st.selectbox("Program *", 
                                         ["Computer Science", "Engineering", "Business", "Arts", "Science"])
                    dob = st.date_input("Date of Birth", min_value=date(1990, 1, 1))
                    address = st.text_area("Address", placeholder="Enter address")
                    status = st.radio("Status", ["Active", "Inactive"], horizontal=True)
                
                if st.form_submit_button("➕ Add Student", use_container_width=True):
                    if name and roll_no and email:
                        new_student = {
                            "id": f"S{len(students)+1:03d}",
                            "name": name,
                            "roll_no": roll_no,
                            "email": email,
                            "phone": phone,
                            "program": program,
                            "dob": str(dob),
                            "address": address,
                            "status": status,
                            "created": str(date.today())
                        }
                        students.append(new_student)
                        save_data(STUDENTS_FILE, students)
                        st.success(f"✅ Student '{name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields (*)")
        
        with tab2:
            if students:
                # Display all students in a nice table
                df = pd.DataFrame(students)
                
                # Show statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Students", len(df))
                with col2:
                    active = len(df[df['status'] == 'Active'])
                    st.metric("Active", active)
                with col3:
                    programs = df['program'].nunique() if 'program' in df.columns else 0
                    st.metric("Programs", programs)
                
                # Data table
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Export button
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Export Students Data",
                    csv_data,
                    "students_export.csv",
                    "text/csv",
                    use_container_width=True
                )
            else:
                st.info("No students found. Add some students first!")
        
        with tab3:
            if students:
                search_col, filter_col = st.columns(2)
                with search_col:
                    search_term = st.text_input("🔍 Search students", 
                                              placeholder="Search by name, roll no, or email")
                
                with filter_col:
                    program_filter = st.selectbox("Filter by Program", 
                                                ["All"] + list(set(s.get('program', '') for s in students)))
                
                # Filter students
                filtered = students
                if search_term:
                    filtered = [s for s in filtered if 
                              search_term.lower() in s.get('name', '').lower() or
                              search_term.lower() in s.get('roll_no', '').lower() or
                              search_term.lower() in s.get('email', '').lower()]
                
                if program_filter != "All":
                    filtered = [s for s in filtered if s.get('program') == program_filter]
                
                if filtered:
                    st.write(f"Found {len(filtered)} student(s)")
                    for student in filtered:
                        with st.container():
                            col1, col2, col3 = st.columns([3, 2, 1])
                            with col1:
                                st.write(f"**{student.get('name')}** ({student.get('roll_no')})")
                                st.write(f"📧 {student.get('email')} | 📞 {student.get('phone')}")
                            with col2:
                                st.write(f"🎓 {student.get('program')}")
                                st.write(f"📅 Joined: {student.get('created', 'N/A')}")
                            with col3:
                                status_color = "🟢" if student.get('status') == 'Active' else "🔴"
                                st.write(f"{status_color} {student.get('status')}")
                            st.divider()
                else:
                    st.info("No students found matching your criteria")
            else:
                st.info("No students to search")
    
    # ------------------- 3. COURSE MANAGEMENT -------------------
    elif feature == "📚 Course Management":
        st.header("📚 Course Management")
        
        tab1, tab2 = st.tabs(["Add Course", "View Courses"])
        
        with tab1:
            with st.form("add_course_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    code = st.text_input("Course Code *", placeholder="e.g., CS101")
                    name = st.text_input("Course Name *", placeholder="e.g., Introduction to Programming")
                    credits = st.number_input("Credits *", 1, 6, 3)
                    department = st.text_input("Department", placeholder="Computer Science")
                
                with col2:
                    instructor = st.text_input("Instructor *", placeholder="Dr. John Smith")
                    schedule = st.text_input("Schedule", placeholder="Mon/Wed 10-11:30")
                    room = st.text_input("Room", placeholder="Room 101")
                    prerequisites = st.text_input("Prerequisites", placeholder="None or list of course codes")
                
                description = st.text_area("Description", placeholder="Course description...")
                
                if st.form_submit_button("➕ Add Course", use_container_width=True):
                    if code and name and instructor:
                        new_course = {
                            "code": code.upper(),
                            "name": name,
                            "credits": credits,
                            "instructor": instructor,
                            "department": department,
                            "schedule": schedule,
                            "room": room,
                            "prerequisites": prerequisites,
                            "description": description
                        }
                        courses.append(new_course)
                        save_data(COURSES_FILE, courses)
                        st.success(f"✅ Course '{name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields (*)")
        
        with tab2:
            if courses:
                df = pd.DataFrame(courses)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Export button
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Export Courses Data",
                    csv_data,
                    "courses_export.csv",
                    "text/csv",
                    use_container_width=True
                )
            else:
                st.info("No courses found. Add some courses first!")
    
    # ------------------- 4. ENROLLMENT TRACKING -------------------
    elif feature == "🎯 Enrollment Tracking":
        st.header("🎯 Enrollment Tracking")
        
        if not students or not courses:
            st.warning("Please add students and courses first")
        else:
            tab1, tab2 = st.tabs(["Enroll Student", "View Enrollments"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    student = st.selectbox("Select Student", 
                                         [f"{s.get('roll_no')} - {s.get('name')}" for s in students])
                with col2:
                    course = st.selectbox("Select Course", 
                                        [f"{c.get('code')} - {c.get('name')}" for c in courses])
                
                semester = st.selectbox("Semester", ["Fall 2024", "Spring 2024", "Summer 2024", "Winter 2024"])
                
                if st.button("Enroll Student", use_container_width=True):
                    if student and course:
                        roll_no = student.split(" - ")[0]
                        course_code = course.split(" - ")[0]
                        
                        # Check if already enrolled
                        already_enrolled = any(
                            e.get('student_roll') == roll_no and 
                            e.get('course_code') == course_code 
                            for e in enrollments
                        )
                        
                        if already_enrolled:
                            st.warning("⚠️ Student is already enrolled in this course")
                        else:
                            new_enrollment = {
                                "student_roll": roll_no,
                                "course_code": course_code,
                                "semester": semester,
                                "enrollment_date": str(date.today()),
                                "status": "Enrolled"
                            }
                            enrollments.append(new_enrollment)
                            save_data(ENROLLMENTS_FILE, enrollments)
                            st.success("✅ Student enrolled successfully!")
                            st.rerun()
            
            with tab2:
                if enrollments:
                    # Create enriched enrollment data
                    enriched = []
                    for e in enrollments:
                        student = next((s for s in students if s.get('roll_no') == e.get('student_roll')), {})
                        course = next((c for c in courses if c.get('code') == e.get('course_code')), {})
                        enriched.append({
                            "Student Name": student.get('name', 'Unknown'),
                            "Roll No": e.get('student_roll', ''),
                            "Course Name": course.get('name', 'Unknown'),
                            "Course Code": e.get('course_code', ''),
                            "Semester": e.get('semester', 'N/A'),
                            "Enrollment Date": e.get('enrollment_date', 'N/A'),
                            "Status": e.get('status', 'N/A')
                        })
                    
                    df = pd.DataFrame(enriched)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Enrollments", len(df))
                    with col2:
                        enrolled = len(df[df['Status'] == 'Enrolled'])
                        st.metric("Currently Enrolled", enrolled)
                    with col3:
                        unique_students = df['Roll No'].nunique()
                        st.metric("Unique Students", unique_students)
                    
                    # Export button
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Export Enrollments",
                        csv_data,
                        "enrollments_export.csv",
                        "text/csv",
                        use_container_width=True
                    )
                else:
                    st.info("No enrollments yet. Enroll some students first!")
    
    # ------------------- 5. ATTENDANCE -------------------
    elif feature == "✅ Attendance":
        st.header("✅ Attendance Management")
        
        if not students:
            st.info("Add students first")
        else:
            tab1, tab2 = st.tabs(["Mark Attendance", "View Attendance"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    att_date = st.date_input("Date", date.today())
                with col2:
                    course = st.selectbox("Course", ["All"] + [c.get('name') for c in courses])
                
                st.write("### Mark Attendance for Students")
                
                attendance_data = []
                for student in students:
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{student.get('name')}** ({student.get('roll_no')})")
                    with col2:
                        status = st.selectbox(
                            "Status",
                            ["Present", "Absent", "Late", "Excused"],
                            key=f"att_{student.get('roll_no')}"
                        )
                    with col3:
                        remarks = st.text_input("Remarks", key=f"rem_{student.get('roll_no')}", 
                                               placeholder="Optional")
                    
                    attendance_data.append({
                        "roll_no": student.get('roll_no'),
                        "name": student.get('name'),
                        "status": status,
                        "remarks": remarks
                    })
                
                if st.button("💾 Save Attendance", use_container_width=True):
                    new_record = {
                        "date": str(att_date),
                        "course": course,
                        "records": attendance_data,
                        "marked_at": datetime.now().isoformat()
                    }
                    attendance.append(new_record)
                    save_data(ATTENDANCE_FILE, attendance)
                    st.success("✅ Attendance saved successfully!")
            
            with tab2:
                if attendance:
                    # Show recent attendance records
                    for record in attendance[-5:]:
                        with st.expander(f"📅 {record.get('date')} - {record.get('course')}"):
                            # Calculate stats
                            total = len(record.get('records', []))
                            present = len([r for r in record.get('records', []) 
                                         if r.get('status') == 'Present'])
                            percentage = (present / total * 100) if total > 0 else 0
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total", total)
                            with col2:
                                st.metric("Present", present)
                            with col3:
                                st.metric("Attendance %", f"{percentage:.1f}%")
                            
                            # Show detailed records
                            df = pd.DataFrame(record.get('records', []))
                            if not df.empty:
                                st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No attendance records yet")
    
    # ------------------- 6. GRADES -------------------
    elif feature == "📝 Grades":
        st.header("📝 Grade Management")
        
        if not students or not courses:
            st.info("Add students and courses first")
        else:
            tab1, tab2 = st.tabs(["Enter Grades", "View Grades"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    student = st.selectbox("Select Student", 
                                         [f"{s.get('roll_no')} - {s.get('name')}" for s in students])
                with col2:
                    course = st.selectbox("Select Course", 
                                        [f"{c.get('code')} - {c.get('name')}" for c in courses])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    assignments = st.number_input("Assignments (30%)", 0.0, 30.0, 20.0)
                with col2:
                    midterm = st.number_input("Midterm (30%)", 0.0, 30.0, 20.0)
                with col3:
                    final = st.number_input("Final (40%)", 0.0, 40.0, 30.0)
                
                total = assignments + midterm + final
                grade = calculate_grade(total)
                gpa = calculate_gpa(grade)
                
                st.info(f"**Total:** {total:.1f}/100 | **Grade:** {grade} | **GPA:** {gpa}")
                
                if st.button("💾 Save Grade", use_container_width=True):
                    roll_no = student.split(" - ")[0]
                    course_code = course.split(" - ")[0]
                    
                    # Remove existing grade
                    grades[:] = [g for g in grades 
                               if not (g.get('student_roll') == roll_no and 
                                      g.get('course_code') == course_code)]
                    
                    new_grade = {
                        "student_roll": roll_no,
                        "course_code": course_code,
                        "assignments": assignments,
                        "midterm": midterm,
                        "final": final,
                        "total": total,
                        "grade": grade,
                        "gpa": gpa,
                        "graded_date": str(date.today())
                    }
                    
                    grades.append(new_grade)
                    save_data(GRADES_FILE, grades)
                    st.success("✅ Grade saved successfully!")
            
            with tab2:
                if grades:
                    # Create enriched grade data
                    enriched = []
                    for g in grades:
                        student = next((s for s in students if s.get('roll_no') == g.get('student_roll')), {})
                        course = next((c for c in courses if c.get('code') == g.get('course_code')), {})
                        enriched.append({
                            "Student Name": student.get('name', 'Unknown'),
                            "Roll No": g.get('student_roll', ''),
                            "Course": course.get('name', 'Unknown'),
                            "Total Marks": f"{g.get('total', 0):.1f}",
                            "Grade": g.get('grade', 'N/A'),
                            "GPA": g.get('gpa', 0.0),
                            "Graded Date": g.get('graded_date', 'N/A')
                        })
                    
                    df = pd.DataFrame(enriched)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Statistics
                    if not df.empty:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            avg_total = df['Total Marks'].str.replace('/100', '').astype(float).mean()
                            st.metric("Avg Marks", f"{avg_total:.1f}")
                        with col2:
                            avg_gpa = df['GPA'].astype(float).mean()
                            st.metric("Avg GPA", f"{avg_gpa:.2f}")
                        with col3:
                            passing = len([g for g in grades if g.get('grade') != 'F'])
                            st.metric("Passing", f"{passing}/{len(grades)}")
                else:
                    st.info("No grades recorded yet")
    
    # ------------------- 7. ASSIGNMENTS -------------------
    elif feature == "📋 Assignments":
        st.header("📋 Assignment Management")
        
        tab1, tab2 = st.tabs(["Create Assignment", "View Assignments"])
        
        with tab1:
            with st.form("create_assignment", clear_on_submit=True):
                title = st.text_input("Assignment Title *", placeholder="e.g., Programming Assignment 1")
                course = st.selectbox("Course *", ["All"] + [c.get('name') for c in courses])
                due_date = st.date_input("Due Date *", min_value=date.today())
                total_marks = st.number_input("Total Marks *", 10, 100, 100)
                description = st.text_area("Description", placeholder="Assignment instructions...")
                
                if st.form_submit_button("➕ Create Assignment", use_container_width=True):
                    if title and course:
                        new_assignment = {
                            "title": title,
                            "course": course,
                            "due_date": str(due_date),
                            "total_marks": total_marks,
                            "description": description,
                            "created": str(date.today()),
                            "status": "Active"
                        }
                        assignments.append(new_assignment)
                        save_data(ASSIGNMENTS_FILE, assignments)
                        st.success("✅ Assignment created successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields (*)")
        
        with tab2:
            if assignments:
                # Show upcoming assignments
                today = date.today()
                upcoming = []
                overdue = []
                
                for a in assignments:
                    due = datetime.strptime(a.get('due_date'), '%Y-%m-%d').date()
                    days_left = (due - today).days
                    
                    if days_left >= 0:
                        upcoming.append((a, days_left))
                    else:
                        overdue.append((a, abs(days_left)))
                
                if overdue:
                    st.subheader("⚠️ Overdue Assignments")
                    for assignment, days_overdue in overdue:
                        with st.container():
                            st.error(f"**{assignment.get('title')}** - Overdue by {days_overdue} days")
                            st.caption(f"Course: {assignment.get('course')} | Due: {assignment.get('due_date')}")
                
                if upcoming:
                    st.subheader("📅 Upcoming Assignments")
                    for assignment, days_left in upcoming:
                        with st.container():
                            if days_left <= 3:
                                st.warning(f"**{assignment.get('title')}** - Due in {days_left} days")
                            else:
                                st.info(f"**{assignment.get('title')}** - Due in {days_left} days")
                            st.caption(f"Course: {assignment.get('course')} | Due: {assignment.get('due_date')}")
                            st.divider()
                
                # All assignments
                st.subheader("All Assignments")
                df = pd.DataFrame(assignments)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No assignments created yet")
    
    # ------------------- 8. TIMETABLE -------------------
    elif feature == "📅 Timetable":
        st.header("📅 Timetable & Scheduling")
        
        tab1, tab2, tab3 = st.tabs(["Add Schedule", "View Timetable", "Weekly View"])
        
        with tab1:
            with st.form("add_schedule_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    course = st.selectbox("Course", 
                                        [f"{c.get('code')} - {c.get('name')}" for c in courses])
                    day = st.selectbox("Day", 
                                     ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                    class_type = st.selectbox("Class Type", ["Lecture", "Lab", "Tutorial", "Seminar", "Exam"])
                
                with col2:
                    start_time = st.time_input("Start Time", time(9, 0))
                    end_time = st.time_input("End Time", time(10, 30))
                    room = st.text_input("Room Number", placeholder="Room 101")
                    instructor = st.text_input("Instructor", placeholder="Instructor name")
                
                if st.form_submit_button("➕ Add to Schedule", use_container_width=True):
                    course_code = course.split(" - ")[0]
                    course_name = course.split(" - ")[1] if " - " in course else ""
                    
                    new_schedule = {
                        "course_code": course_code,
                        "course_name": course_name,
                        "day": day,
                        "start_time": start_time.strftime("%H:%M"),
                        "end_time": end_time.strftime("%H:%M"),
                        "room": room,
                        "instructor": instructor,
                        "type": class_type,
                        "added_date": str(date.today())
                    }
                    
                    timetable.append(new_schedule)
                    save_data(TIMETABLE_FILE, timetable)
                    st.success("✅ Schedule added successfully!")
                    st.rerun()
        
        with tab2:
            if timetable:
                # Display timetable in a table
                df = pd.DataFrame(timetable)
                
                # Allow filtering
                col1, col2 = st.columns(2)
                with col1:
                    day_filter = st.selectbox("Filter by Day", 
                                            ["All"] + sorted(set(t.get('day') for t in timetable)))
                with col2:
                    course_filter = st.selectbox("Filter by Course", 
                                               ["All"] + sorted(set(t.get('course_name') for t in timetable)))
                
                # Apply filters
                filtered_df = df
                if day_filter != "All":
                    filtered_df = filtered_df[filtered_df['day'] == day_filter]
                if course_filter != "All":
                    filtered_df = filtered_df[filtered_df['course_name'] == course_filter]
                
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                
                # Export button
                csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Export Timetable",
                    csv_data,
                    "timetable.csv",
                    "text/csv",
                    use_container_width=True
                )
            else:
                st.info("No timetable entries yet. Add some schedules!")
        
        with tab3:
            if timetable:
                # Create weekly view
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                
                for day in days:
                    day_classes = [t for t in timetable if t.get('day') == day]
                    if day_classes:
                        st.subheader(f"📅 {day}")
                        
                        # Sort by start time
                        day_classes.sort(key=lambda x: x.get('start_time', '00:00'))
                        
                        for cls in day_classes:
                            col1, col2, col3 = st.columns([3, 2, 1])
                            with col1:
                                st.write(f"**{cls.get('course_name')}** ({cls.get('course_code')})")
                                st.write(f"👨‍🏫 {cls.get('instructor')}")
                            with col2:
                                st.write(f"🕐 {cls.get('start_time')} - {cls.get('end_time')}")
                                st.write(f"🏫 {cls.get('room')}")
                            with col3:
                                st.write(f"📚 {cls.get('type')}")
                            st.divider()
            else:
                st.info("No timetable to display")
    
    # ------------------- 9. TRANSCRIPTS -------------------
    elif feature == "📄 Transcripts":
        st.header("📄 Transcript Generation")
        
        if not students:
            st.info("Add students first")
        else:
            student = st.selectbox("Select Student", 
                                 [f"{s.get('roll_no')} - {s.get('name')}" for s in students])
            
            if student:
                roll_no = student.split(" - ")[0]
                student_data = next((s for s in students if s.get('roll_no') == roll_no), {})
                
                # Get student's grades
                student_grades = [g for g in grades if g.get('student_roll') == roll_no]
                
                # Display transcript
                st.write("---")
                st.write("### 🎓 OFFICIAL TRANSCRIPT")
                st.write(f"**Student:** {student_data.get('name')}")
                st.write(f"**Roll No:** {student_data.get('roll_no')}")
                st.write(f"**Program:** {student_data.get('program')}")
                st.write(f"**Date Issued:** {date.today()}")
                st.write("---")
                
                if student_grades:
                    # Calculate CGPA
                    total_gpa = sum(calculate_gpa(g.get('grade', 'F')) for g in student_grades)
                    cgpa = total_gpa / len(student_grades) if student_grades else 0
                    
                    # Display grades in table
                    grade_data = []
                    for g in student_grades:
                        course = next((c for c in courses if c.get('code') == g.get('course_code')), {})
                        grade_data.append({
                            "Course Code": g.get('course_code'),
                            "Course Name": course.get('name', 'Unknown'),
                            "Credits": course.get('credits', 0),
                            "Grade": g.get('grade'),
                            "GPA": calculate_gpa(g.get('grade'))
                        })
                    
                    df = pd.DataFrame(grade_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    st.write("---")
                    st.write(f"### **Cumulative GPA (CGPA): {cgpa:.2f}**")
                    
                    # Download transcript
                    transcript_text = f"""
                    OFFICIAL TRANSCRIPT
                    
                    Student: {student_data.get('name')}
                    Roll Number: {student_data.get('roll_no')}
                    Program: {student_data.get('program')}
                    Date Issued: {date.today()}
                    
                    COURSE GRADES:
                    """
                    
                    for item in grade_data:
                        transcript_text += f"\n{item['Course Code']} - {item['Course Name']}: {item['Grade']} (GPA: {item['GPA']})"
                    
                    transcript_text += f"\n\nCUMULATIVE GPA (CGPA): {cgpa:.2f}"
                    
                    st.download_button(
                        "📥 Download Transcript (TXT)",
                        transcript_text,
                        f"transcript_{roll_no}.txt",
                        "text/plain",
                        use_container_width=True
                    )
                else:
                    st.info("No grades available for this student")
    
    # ------------------- 10. PERFORMANCE REPORTS -------------------
    elif feature == "📈 Performance Reports":
        st.header("📈 Academic Performance Reports")
        
        if not students:
            st.info("Add students first")
            return
        
        tab1, tab2, tab3 = st.tabs(["Student Report", "Course Report", "System Analytics"])
        
        with tab1:
            st.subheader("📊 Individual Student Report")
            
            student = st.selectbox("Select Student for Report", 
                                 [f"{s.get('roll_no')} - {s.get('name')}" for s in students])
            
            if student:
                roll_no = student.split(" - ")[0]
                student_data = next((s for s in students if s.get('roll_no') == roll_no), {})
                
                # Get all data for this student
                student_grades = [g for g in grades if g.get('student_roll') == roll_no]
                student_enrollments = [e for e in enrollments if e.get('student_roll') == roll_no]
                student_attendance = []
                
                # Calculate attendance from records
                for att_record in attendance:
                    for record in att_record.get('records', []):
                        if record.get('roll_no') == roll_no:
                            student_attendance.append({
                                'date': att_record.get('date'),
                                'status': record.get('status'),
                                'course': att_record.get('course', 'N/A')
                            })
                
                # Display comprehensive report
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    ### Student Information
                    - **Name:** {student_data.get('name')}
                    - **Roll No:** {student_data.get('roll_no')}
                    - **Program:** {student_data.get('program')}
                    - **Email:** {student_data.get('email')}
                    - **Status:** {student_data.get('status')}
                    - **Date of Birth:** {student_data.get('dob', 'N/A')}
                    """)
                
                with col2:
                    # Academic summary
                    if student_grades:
                        total_marks = sum(g.get('total', 0) for g in student_grades)
                        avg_marks = total_marks / len(student_grades) if student_grades else 0
                        grades_list = [g.get('grade', 'F') for g in student_grades]
                        cgpa = calculate_cgpa(grades_list)
                        
                        st.metric("Average Marks", f"{avg_marks:.1f}")
                        st.metric("CGPA", f"{cgpa:.2f}")
                        st.metric("Courses Taken", len(student_grades))
                
                st.divider()
                
                # Academic Performance
                st.subheader("📈 Academic Performance")
                
                if student_grades:
                    # Grade distribution chart
                    grade_counts = {}
                    for g in student_grades:
                        grade = g.get('grade', 'F')
                        grade_counts[grade] = grade_counts.get(grade, 0) + 1
                    
                    if grade_counts:
                        fig = px.pie(
                            values=list(grade_counts.values()),
                            names=list(grade_counts.keys()),
                            title="Grade Distribution",
                            color_discrete_sequence=px.colors.sequential.RdBu
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Course-wise performance table
                    st.write("#### Course-wise Performance")
                    grade_table = []
                    for g in student_grades:
                        course = next((c for c in courses if c.get('code') == g.get('course_code')), {})
                        grade_table.append({
                            "Course": course.get('name', g.get('course_code')),
                            "Code": g.get('course_code'),
                            "Marks": f"{g.get('total', 0):.1f}",
                            "Grade": g.get('grade', 'N/A'),
                            "GPA": f"{calculate_gpa(g.get('grade', 'F')):.2f}"
                        })
                    
                    st.dataframe(pd.DataFrame(grade_table), use_container_width=True, hide_index=True)
                else:
                    st.info("No grades recorded for this student")
                
                st.divider()
                
                # Attendance Analysis
                st.subheader("✅ Attendance Analysis")
                
                if student_attendance:
                    total_classes = len(student_attendance)
                    present = len([a for a in student_attendance if a.get('status') == 'Present'])
                    attendance_rate = (present / total_classes * 100) if total_classes > 0 else 0
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Classes", total_classes)
                    with col2:
                        st.metric("Present", present)
                    with col3:
                        st.metric("Absent", total_classes - present)
                    with col4:
                        st.metric("Attendance %", f"{attendance_rate:.1f}%")
                    
                    # Recent attendance
                    st.write("#### Recent Attendance")
                    recent_attendance = student_attendance[-10:] if len(student_attendance) > 10 else student_attendance
                    att_df = pd.DataFrame(recent_attendance)
                    st.dataframe(att_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No attendance records for this student")
                
                st.divider()
                
                # Enrollment Status
                st.subheader("🎯 Course Enrollment")
                
                if student_enrollments:
                    st.write(f"**Total Enrolled Courses:** {len(student_enrollments)}")
                    for e in student_enrollments:
                        course = next((c for c in courses if c.get('code') == e.get('course_code')), {})
                        st.write(f"- {course.get('name', e.get('course_code'))} ({e.get('semester', 'N/A')}) - {e.get('status', 'N/A')}")
                else:
                    st.info("No course enrollments for this student")
        
        with tab2:
            st.subheader("📚 Course Performance Report")
            
            if not courses:
                st.info("Add courses first")
            else:
                course = st.selectbox("Select Course", 
                                    [f"{c.get('code')} - {c.get('name')}" for c in courses])
                
                if course:
                    course_code = course.split(" - ")[0]
                    course_data = next((c for c in courses if c.get('code') == course_code), {})
                    
                    # Get all grades for this course
                    course_grades = [g for g in grades if g.get('course_code') == course_code]
                    course_enrollments = [e for e in enrollments if e.get('course_code') == course_code]
                    
                    st.markdown(f"""
                    ### Course Information
                    - **Course:** {course_data.get('name')}
                    - **Code:** {course_data.get('code')}
                    - **Instructor:** {course_data.get('instructor')}
                    - **Credits:** {course_data.get('credits')}
                    - **Department:** {course_data.get('department', 'N/A')}
                    """)
                    
                    st.divider()
                    
                    # Course Statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Students", len(course_enrollments))
                    with col2:
                        st.metric("Grades Recorded", len(course_grades))
                    with col3:
                        if course_grades:
                            avg_marks = sum(g.get('total', 0) for g in course_grades) / len(course_grades)
                            st.metric("Avg Marks", f"{avg_marks:.1f}")
                        else:
                            st.metric("Avg Marks", "N/A")
                    with col4:
                        if course_grades:
                            passing = len([g for g in course_grades if g.get('grade') != 'F'])
                            st.metric("Pass Rate", f"{(passing/len(course_grades)*100):.1f}%")
                        else:
                            st.metric("Pass Rate", "N/A")
                    
                    if course_grades:
                        # Grade distribution
                        st.subheader("Grade Distribution")
                        grade_counts = {}
                        for g in course_grades:
                            grade = g.get('grade', 'F')
                            grade_counts[grade] = grade_counts.get(grade, 0) + 1
                        
                        fig = px.bar(
                            x=list(grade_counts.keys()),
                            y=list(grade_counts.values()),
                            title="Grade Distribution",
                            labels={'x': 'Grade', 'y': 'Number of Students'},
                            color=list(grade_counts.keys()),
                            color_discrete_sequence=px.colors.sequential.Viridis
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Top performers
                        st.subheader("Top Performers")
                        sorted_grades = sorted(course_grades, key=lambda x: x.get('total', 0), reverse=True)[:5]
                        top_table = []
                        for g in sorted_grades:
                            student = next((s for s in students if s.get('roll_no') == g.get('student_roll')), {})
                            top_table.append({
                                "Student": student.get('name', g.get('student_roll')),
                                "Roll No": g.get('student_roll'),
                                "Marks": f"{g.get('total', 0):.1f}",
                                "Grade": g.get('grade', 'N/A')
                            })
                        
                        st.dataframe(pd.DataFrame(top_table), use_container_width=True, hide_index=True)
        
        with tab3:
            st.subheader("📊 System-wide Analytics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Students", len(students))
            with col2:
                st.metric("Total Courses", len(courses))
            with col3:
                st.metric("Total Grades", len(grades))
            
            st.divider()
            
            # Student distribution by program
            if students:
                st.subheader("📊 Student Distribution by Program")
                program_counts = {}
                for s in students:
                    program = s.get('program', 'Unknown')
                    program_counts[program] = program_counts.get(program, 0) + 1
                
                if program_counts:
                    fig = px.pie(
                        values=list(program_counts.values()),
                        names=list(program_counts.keys()),
                        title="Students by Program",
                        hole=0.3
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Overall grade distribution
            if grades:
                st.subheader("📈 Overall Grade Distribution")
                grade_counts = {}
                for g in grades:
                    grade = g.get('grade', 'F')
                    grade_counts[grade] = grade_counts.get(grade, 0) + 1
                
                if grade_counts:
                    fig = px.bar(
                        x=list(grade_counts.keys()),
                        y=list(grade_counts.values()),
                        title="Overall Grade Distribution",
                        labels={'x': 'Grade', 'y': 'Count'},
                        color=list(grade_counts.keys()),
                        color_discrete_sequence=px.colors.sequential.Plasma
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    # ------------------- 11. IMPORT DATA -------------------
    elif feature == "📤 Import Data":
        st.header("📤 Import Data from Files")
        
        tab1, tab2, tab3 = st.tabs(["Import CSV", "Import Excel", "Templates"])
        
        with tab1:
            st.info("Upload CSV files to import data")
            
            uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
            
            if uploaded_file:
                # Auto-detect data type from filename
                filename = uploaded_file.name.lower()
                if 'student' in filename:
                    default_type = "Students"
                elif 'course' in filename:
                    default_type = "Courses"
                elif 'timetable' in filename or 'schedule' in filename:
                    default_type = "Timetable"
                elif 'enroll' in filename:
                    default_type = "Enrollments"
                elif 'grade' in filename:
                    default_type = "Grades"
                elif 'assign' in filename:
                    default_type = "Assignments"
                else:
                    default_type = "Students"
                
                data_type = st.selectbox("Select data type", 
                                       ["Students", "Courses", "Timetable", "Enrollments", "Grades", "Assignments"],
                                       index=["Students", "Courses", "Timetable", "Enrollments", "Grades", "Assignments"].index(default_type))
                
                # Preview data
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success(f"File loaded: {len(df)} rows")
                    
                    with st.expander("📋 Preview Data"):
                        st.dataframe(df.head(), use_container_width=True)
                    
                    if st.button("🚀 Import Data", type="primary", use_container_width=True):
                        success, message = import_dataframe(df, data_type)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        with tab2:
            st.info("Upload Excel files to import data")
            
            uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
            
            if uploaded_file:
                data_type = st.selectbox("Select data type to import", 
                                       ["Students", "Courses", "Timetable", "Enrollments", "Grades", "Assignments"])
                
                # Preview data
                try:
                    df = pd.read_excel(uploaded_file)
                    st.success(f"File loaded: {len(df)} rows")
                    
                    with st.expander("📋 Preview Data"):
                        st.dataframe(df.head(), use_container_width=True)
                    
                    if st.button("🚀 Import Data", type="primary", use_container_width=True):
                        success, message = import_dataframe(df, data_type)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        with tab3:
            st.info("Download templates for importing data")
            
            # Create sample templates
            sample_students = pd.DataFrame({
                'name': ['John Doe', 'Jane Smith'],
                'roll_no': ['2024001', '2024002'],
                'email': ['john@email.com', 'jane@email.com'],
                'phone': ['1234567890', '0987654321'],
                'program': ['Computer Science', 'Engineering'],
                'status': ['Active', 'Active'],
                'address': ['123 Main St', '456 Oak Ave'],
                'dob': ['2000-01-01', '2000-02-15']
            })
            
            sample_courses = pd.DataFrame({
                'code': ['CS101', 'MATH101'],
                'name': ['Programming Basics', 'Calculus I'],
                'credits': [3, 4],
                'instructor': ['Dr. Smith', 'Prof. Johnson'],
                'department': ['Computer Science', 'Mathematics']
            })
            
            sample_timetable = pd.DataFrame({
                'course_code': ['CS101', 'MATH101'],
                'course_name': ['Programming Basics', 'Calculus I'],
                'day': ['Monday', 'Tuesday'],
                'start_time': ['09:00', '11:00'],
                'end_time': ['10:30', '12:30'],
                'room': ['Room 101', 'Room 201'],
                'instructor': ['Dr. Smith', 'Prof. Johnson'],
                'type': ['Lecture', 'Lecture']
            })
            
            col1, col2, col3 = st.columns(3)
            with col1:
                csv = sample_students.to_csv(index=False)
                st.download_button(
                    "📥 Students Template",
                    csv,
                    "students_template.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col2:
                csv = sample_courses.to_csv(index=False)
                st.download_button(
                    "📥 Courses Template",
                    csv,
                    "courses_template.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col3:
                csv = sample_timetable.to_csv(index=False)
                st.download_button(
                    "📥 Timetable Template",
                    csv,
                    "timetable_template.csv",
                    "text/csv",
                    use_container_width=True
                )
    
    # ------------------- 12. EXPORT DATA -------------------
    elif feature == "📥 Export Data":
        st.header("📥 Export System Data")
        
        # Export all data in CSV format
        st.info("Export all system data in CSV format")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            if students:
                csv = pd.DataFrame(students).to_csv(index=False)
                st.download_button(
                    "📊 Students",
                    csv,
                    "students.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col2:
            if courses:
                csv = pd.DataFrame(courses).to_csv(index=False)
                st.download_button(
                    "📚 Courses",
                    csv,
                    "courses.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col3:
            if timetable:
                csv = pd.DataFrame(timetable).to_csv(index=False)
                st.download_button(
                    "📅 Timetable",
                    csv,
                    "timetable.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col4:
            if enrollments:
                csv = pd.DataFrame(enrollments).to_csv(index=False)
                st.download_button(
                    "🎯 Enrollments",
                    csv,
                    "enrollments.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col5:
            if grades:
                csv = pd.DataFrame(grades).to_csv(index=False)
                st.download_button(
                    "📝 Grades",
                    csv,
                    "grades.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col6:
            if assignments:
                csv = pd.DataFrame(assignments).to_csv(index=False)
                st.download_button(
                    "📋 Assignments",
                    csv,
                    "assignments.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        st.divider()
        
        # Backup all data
        st.subheader("🔒 Backup All Data")
        
        if st.button("💾 Create Backup", use_container_width=True):
            backup_dir = os.path.join(DATA_DIR, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_files = []
            
            for filepath, data in [
                (STUDENTS_FILE, students),
                (COURSES_FILE, courses),
                (TIMETABLE_FILE, timetable),
                (ENROLLMENTS_FILE, enrollments),
                (GRADES_FILE, grades),
                (ASSIGNMENTS_FILE, assignments),
                (ATTENDANCE_FILE, attendance)
            ]:
                if data:
                    backup_file = os.path.join(backup_dir, f"{os.path.basename(filepath)}_{timestamp}.json")
                    save_data(backup_file, data)
                    backup_files.append(backup_file)
            
            st.success(f"✅ Backup created with {len(backup_files)} files!")

if __name__ == "__main__":
    main()