import streamlit as st
import pandas as pd

st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="centered")

st.title("🎓 GPA and CGPA Calculator")

st.write("""
Enter your **marks for each subject** below to calculate your **GPA** for this semester, 
and optionally enter your **previous CGPA and total credit hours** to calculate your new **CGPA**.
""")

# --- Define function to convert marks to grade points ---
def marks_to_gpa(marks):
    if marks >= 85:
        return 4.0
    elif marks >= 80:
        return 3.7
    elif marks >= 75:
        return 3.3
    elif marks >= 70:
        return 3.0
    elif marks >= 65:
        return 2.7
    elif marks >= 61:
        return 2.3
    elif marks >= 58:
        return 2.0
    elif marks >= 55:
        return 1.7
    elif marks >= 50:
        return 1.0
    else:
        return 0.0

# --- Input section ---
st.header("📘 Current Semester Marks")

num_subjects = st.number_input("Enter number of subjects this semester:", min_value=1, max_value=15, value=5, step=1)

subjects = []
total_points = 0
total_credits = 0

st.write("### Enter your marks and credit hours for each subject")

for i in range(num_subjects):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        subject = st.text_input(f"Subject {i+1} name:", key=f"sub_{i}")
    with col2:
        marks = st.number_input(f"Marks ({subject or f'Subject {i+1}'})", 0, 100, 75, key=f"marks_{i}")
    with col3:
        credits = st.number_input(f"Credit hours", 1, 5, 3, key=f"credits_{i}")

    gpa = marks_to_gpa(marks)
    subjects.append({
        "Subject": subject or f"Subject {i+1}",
        "Marks": marks,
        "Credit Hours": credits,
        "Grade Point": gpa,
        "Quality Points": gpa * credits
    })
    total_points += gpa * credits
    total_credits += credits

# --- GPA Calculation ---
if total_credits > 0:
    current_gpa = total_points / total_credits
else:
    current_gpa = 0

# --- Display current GPA ---
st.subheader("📊 Current Semester GPA")
st.write(f"**Your GPA for this semester:** `{current_gpa:.2f}`")

# --- Previous CGPA Section ---
st.header("📚 CGPA Calculation (Optional)")
st.write("If you have previous CGPA and total credit hours, enter them below:")

col1, col2 = st.columns(2)
with col1:
    prev_cgpa = st.number_input("Previous CGPA", 0.0, 4.0, 0.0, step=0.01)
with col2:
    prev_credits = st.number_input("Total Credit Hours Completed Previously", 0, 200, 0, step=1)

# --- CGPA Calculation ---
if prev_credits > 0:
    new_cgpa = ((prev_cgpa * prev_credits) + (current_gpa * total_credits)) / (prev_credits + total_credits)
else:
    new_cgpa = current_gpa

st.subheader("🎯 Updated CGPA")
st.write(f"**Your updated CGPA:** `{new_cgpa:.2f}`")

# --- Show detailed table ---
df = pd.DataFrame(subjects)
st.write("### Detailed Results")
st.dataframe(df, use_container_width=True)

st.success("✅ GPA and CGPA calculated successfully!")

