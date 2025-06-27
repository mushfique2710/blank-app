import streamlit as st
import json
from datetime import time

st.title("Schedule & Weekend JSON Creator")

ALL_DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

# Initialize session state
if "working_block" not in st.session_state:
    st.session_state.working_block = None
if "selected_days" not in st.session_state:
    st.session_state.selected_days = []

# Sidebar form
st.sidebar.header("Define Working Hours")

with st.sidebar.form("working_hours_form"):
    selected_days = st.multiselect("Working Days", options=ALL_DAYS[:5], default=["MON", "TUE", "WED", "THU", "FRI"])
    start_time = st.time_input("Start Time", value=time(9, 0))
    end_time = st.time_input("End Time", value=time(17, 0))
    submit = st.form_submit_button("Set Working Hours")

# Save working block
if submit:
    if selected_days:
        st.session_state.working_block = {
            "days": selected_days,
            "time": [start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S")],
            "name": "Working Hours"
        }
        st.session_state.selected_days = selected_days
    else:
        st.warning("Please select at least one working day.")

# Construct Weekend block
used_days = set(st.session_state.selected_days)
weekend_days = [day for day in ALL_DAYS if day not in used_days]

weekend_block = {
    "days": weekend_days,
    "time": ["00:00:00", "23:59:59"],
    "name": "Weekend"
} if weekend_days else None

# Final Output
st.header("Generated Schedule JSON")

schedule = []
if st.session_state.working_block:
    schedule.append(st.session_state.working_block)
if weekend_block:
    schedule.append(weekend_block)

if schedule:
    st.json(schedule)

# Reset button
if st.button("Reset"):
    st.session_state.working_block = None
    st.session_state.selected_days = []
