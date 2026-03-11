# 🎓 Student Management System - Academic Project

A comprehensive Student Management System developed as a 3rd Semester Academic Project, built with Python, Streamlit, and Pandas. This system provides complete student data management, academic tracking, and performance analytics for educational institutions.

## 📌 Project Overview

This Student Management System is developed as part of the 3rd Semester Computer Science curriculum. It serves as a complete solution for educational institutions to manage student records, academic performance, attendance, and administrative tasks through an intuitive web interface.

### 🎯 Project Objectives

- Develop a complete CRUD application for student data management
- Implement academic tracking and grading systems
- Create interactive data visualizations for performance analysis
- Build a user-friendly web interface using Streamlit
- Demonstrate proficiency in Python, data handling, and web development

---

## ✨ Key Features

### 📋 Core Management Modules

| Module                | Features                                                | Status      |
| --------------------- | ------------------------------------------------------- | ----------- |
| 👤 Student Profiles   | Add, view, edit, delete students with complete profiles | ✅ Complete |
| 📚 Course Management  | Manage courses, credits, instructors, departments       | ✅ Complete |
| 🎯 Enrollment System  | Track course registrations and student enrollments      | ✅ Complete |
| ✅ Attendance Tracker | Record and monitor attendance with analytics            | ✅ Complete |
| 📝 Grade Management   | Enter grades, calculate GPA, generate transcripts       | ✅ Complete |
| 📋 Assignments        | Create assignments, track deadlines and submissions     | ✅ Complete |
| 📅 Timetable          | Schedule classes with day/time/room assignments         | ✅ Complete |
| 📄 Transcripts        | Generate official academic transcripts                  | ✅ Complete |
| 📈 Reports            | Comprehensive performance analytics                     | ✅ Complete |
| 📤 Data Import/Export | Bulk data operations via CSV/Excel                      | ✅ Complete |

### 📊 Advanced Features

- Interactive Dashboard with real-time statistics
- Search & Filter across all data modules
- Automatic Grade Calculation with GPA computation
- Data Validation to prevent duplicates
- Visual Analytics with charts and graphs
- Backup & Restore functionality
- Responsive UI with intuitive navigation

---

## 🛠️ Technology Stack

### Frontend

- Streamlit - Web application framework
- Plotly - Interactive data visualizations
- CSS Styling - Custom UI enhancements

### Backend

- Python 3.8+ - Core programming language
- Pandas - Data manipulation and analysis
- JSON - Data storage and serialization

### Data Processing

- CSV/Excel Import/Export - Bulk data operations
- Data Validation - Input validation and error handling
- Statistical Analysis - Performance metrics calculation

---

## 📁 Project Structure

student-management-system/
│
├── app.py # Main application entry point
│
├── data/ # Data storage directory
│ ├── students.json # Student records database
│ ├── courses.json # Course catalog database
│ ├── enrollments.json # Enrollment records
│ ├── attendance.json # Attendance records
│ ├── grades.json # Academic grades
│ ├── assignments.json # Assignment records
│ └── timetable.json # Class schedules
│
├── requirements.txt # Python dependencies
├── README.md # Project documentation
│
├── sample_files/ # Sample data templates
│ ├── students_sample.csv # Student import template
│ ├── courses_sample.csv # Course import template
│ └── timetable_sample.csv # Schedule import template
│
└── screenshots/ # Application screenshots
├── dashboard.png
├── student_management.png
└── analytics.png

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation Guide

#### Method 1: Quick Setup (Recommended)

1. Clone the repository

git clone https://github.com/IKRAM-UL-HAQ63/student-management-system.git
cd student-management-system

2. Install the required libraries:

pip install -r requirements.txt

3. Run the Streamlit app:

streamlit run app.py
