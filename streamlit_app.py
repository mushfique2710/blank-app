import streamlit as st
from datetime import time, datetime, timedelta

st.title("Weekly Schedule Creator (Sun - Sat)")

schedule = {}
hex_schedule = {}

st.subheader("Set Start and End Times for Each Day")

# Days of the week (Sunday to Saturday)
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
for day in days:
    with st.expander(f"{day}"):
        start = st.time_input(f"Start time for {day}", value=time(9, 0), key=f"{day}_start")
        end = st.time_input(f"End time for {day}", value=time(17, 0), key=f"{day}_end")

        if start >= end:
            st.warning(f"⚠️ End time should be after start time for {day}.")
        else:
            schedule[day] = {"Start": start.strftime("%H:%M"), "End": end.strftime("%H:%M")}

            # Generate 96-slot binary schedule (15-minute intervals)
            binary_slots = []
            current = datetime.combine(datetime.today(), time(0, 0))
            end_of_day = current + timedelta(hours=24)

            while current < end_of_day:
                slot_time = current.time()
                if start <= slot_time < end:
                    binary_slots.append(1)
                else:
                    binary_slots.append(0)
                current += timedelta(minutes=15)

            # Convert every 4 binary slots to a hex digit
            hex_digits = []
            for i in range(0, len(binary_slots), 4):
                chunk = binary_slots[i:i+4]
                binary_str = ''.join(map(str, chunk))
                hex_digit = hex(int(binary_str, 2))[2:]  # remove '0x'
                hex_digits.append(hex_digit.upper())

            hex_schedule[day] = ''.join(hex_digits)

# Display the schedule table
if schedule:
    st.subheader("📅 Your Weekly Schedule")
    st.table(schedule)

# Display single combined hex string
if hex_schedule:
    st.subheader("🧮 Single Hexadecimal Schedule String (7 days × 24 hex digits = 168 chars)")
    combined_hex_string = ''.join(hex_schedule[day] for day in days)
    st.code(combined_hex_string, language='text')
