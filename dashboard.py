import streamlit as st
import pandas as pd
import json, os

DATA_FILE = "applications.json"

st.set_page_config(page_title="Recruiter Dashboard", layout="wide")
st.title("📊 Crypto Exchange Hiring Dashboard")

def load():
    if not os.path.exists(DATA_FILE):
        return []
    return json.load(open(DATA_FILE))

data = load()

if not data:
    st.warning("No applications yet.")
    st.stop()

df = pd.DataFrame(data)

# SIDEBAR
st.sidebar.header("Filters")
job = st.sidebar.selectbox("Position", ["All"] + list(df["job_title"].unique()))

if job != "All":
    df = df[df["job_title"] == job]

# SEARCH
search = st.text_input("🔍 Search (name/email/username)")
if search:
    df = df[df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]

st.dataframe(df, use_container_width=True)

# DETAILS
st.subheader("📄 Application Details")
idx = st.selectbox("Select Candidate", df.index)

row = df.loc[idx]

st.write(f"**Name:** {row['name']}")
st.write(f"**Email:** {row['email']}")
st.write(f"**Location:** {row['location']}")
st.write(f"**Job Status:** {row['job_status']}")
st.write(f"**Previous Salary:** {row['prev_salary']}")
st.write(f"**Expected Salary:** {row['expected_salary']}")
st.write(f"**Start Date:** {row['start_date']}")
st.write(f"**Social:** {row['social']}")
st.write(f"**Username:** @{row['username']}")
st.write(f"**Position:** {row['job_title']}")

if os.path.exists(row["resume_path"]):
    with open(row["resume_path"], "rb") as f:
        st.download_button("📄 Download Resume", f, "resume.pdf")