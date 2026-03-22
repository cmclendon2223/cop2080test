import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="To-Do List", page_icon="✅", layout="wide")
st.title("✅ To-Do List Manager")
# Check marks are Unicode characters that could be created  with a 
# print(“\u2705”) or similar print("\U0001F600")

def fetch_tasks():
    try:
        r = requests.get(f"{API_URL}/tasks")
        return r.json().get("tasks", [])
    except Exception:
        st.error("Cannot connect to FastAPI. Is the server running?")
        return []

def fetch_stats():
    try:
        r = requests.get(f"{API_URL}/stats")
        return r.json()
    except Exception:
        return {}

st.sidebar.header("Manage Tasks")

with st.sidebar.expander("➕ Add New Task", expanded=True):
    new_title = st.text_input("Title", key="new_title")
    new_desc  = st.text_area("Description", key="new_desc", height=80)
    if st.button("Add Task"):
        if new_title.strip():
            payload = {"title": new_title.strip(), "description": new_desc.strip()}
            r = requests.post(f"{API_URL}/tasks", json=payload)
            if r.status_code == 201:
                st.success(f"Task '{new_title}' added!")
                st.rerun()
        else:
            st.warning("Title cannot be empty.")

tasks = fetch_tasks()

if tasks:
    task_ids    = [t["id"] for t in tasks]
    task_titles = {t["id"]: t["title"] for t in tasks}

    with st.sidebar.expander("✏️ Update Task"):
        selected_id   = st.selectbox("Select task", task_ids,
                            format_func=lambda i: f"#{i} {task_titles[i]}")
        selected_task = next(t for t in tasks if t["id"] == selected_id)
        upd_title = st.text_input("New title",       value=selected_task["title"])
        upd_desc  = st.text_area("New description",  value=selected_task["description"])
        upd_done  = st.checkbox("Completed",         value=selected_task["completed"])
        if st.button("Update Task"):
            r = requests.put(f"{API_URL}/tasks/{selected_id}",
                             json={"title": upd_title,
                                   "description": upd_desc,
                                   "completed": upd_done})
            if r.status_code == 200:
                st.success("Task updated!")
                st.rerun()

    with st.sidebar.expander("🗑️ Delete Task"):
        delete_task_id = st.selectbox("Select task to delete", task_ids,
                     format_func=lambda i: f"#{i} {task_titles[i]}", key="delete_task_id") # streamlit passes each task_id/option into i
        if st.button("Delete Task", type="primary"):
            r = requests.delete(f"{API_URL}/tasks/{delete_task_id}")

            if r.status_code == 200:
                st.success("Task deleted!")
                st.rerun()

col1, col2 = st.columns([3, 2]) # divides gui into two columns

with col1:
    st.subheader("📋 All Tasks")
    if tasks:
        df = pd.DataFrame(tasks)[["id","title","description","completed","created_at"]]
        df["completed"] = df["completed"].map({True: "✅ Done", False: "⏳ Pending"})
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No tasks yet. Add one from the sidebar!")

stats = fetch_stats()

with col2:
    st.subheader("📊 Task Overview")

    if stats:
        # Chart 1 – Pie chart: completed vs pending
        completed = stats.get("completed", 0)
        pending   = stats.get("pending",   0)
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        if completed + pending > 0:
            ax1.pie([completed, pending],
                    labels=["Completed", "Pending"],
                    autopct="%1.0f%%",
                    colors=["#4CAF50", "#FF9800"],
                    startangle=90)
            ax1.set_title("Completed vs Pending")
        st.pyplot(fig1)

        # Chart 2 – Bar chart: tasks created per day
        creation_log = stats.get("creation_log", [])
        st.markdown("**Tasks Created Per Day**")
        if creation_log:
            import pandas as pd
            date_counts = pd.Series(creation_log).value_counts().sort_index()
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            ax2.bar(date_counts.index, date_counts.values, color="#2196F3")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Tasks Created")
            ax2.set_title("Daily Task Creation")
            plt.xticks(rotation=30, ha="right", fontsize=7)
            st.pyplot(fig2)
        else:
            st.info("No creation data yet.")
