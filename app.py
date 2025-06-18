import streamlit as st
import csv
import os

# Define the path to the CSV file
CSV_FILE = "tasks.csv"

# Load tasks from CSV (returns list of tuples: [(task, completed), ...])
def load_tasks():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        return [(row[0], row[1] == "True") for row in reader]

# Save tasks to CSV
def save_tasks(task_list):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([[task, str(done)] for task, done in task_list])

# Display tasks with checkboxes
def display(task_list):
    st.write("### 📋 Current Tasks:")
    for i, (task, done) in enumerate(task_list):
        col1, col2, col3 = st.columns([0.7, 0.2, 0.1])
        with col1:
            if done:
                st.markdown(f"<span style='color:gray;text-decoration:line-through;'>{task}</span>", unsafe_allow_html=True)
            else:
                st.write(task)
        with col2:
            # Toggle completion
            if st.checkbox("Done", value=done, key=f"done_{i}"):
                task_list[i] = (task, True)
            else:
                task_list[i] = (task, False)
        with col3:
            # Delete task
            if st.button("❌", key=f"delete_{i}"):
                task_list.pop(i)
                save_tasks(task_list)
                st.experimental_rerun()

def main():
    st.set_page_config(page_title="To-Do List", page_icon="📝")
    st.title("📝 To-Do List")

    # Background
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.pexels.com/photos/2387793/pexels-photo-2387793.jpeg");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    task_list = load_tasks()

    # Input for adding a task
    st.subheader("Add a new task:")
    new_task = st.text_input("Task", key="new_task_input")
    if st.button("➕ Add Task"):
        if new_task.strip():
            task_list.append((new_task.strip(), False))
            save_tasks(task_list)
            st.experimental_rerun()
        else:
            st.warning("Please enter a task before adding.")

    st.divider()

    # Display tasks
    if task_list:
        display(task_list)
    else:
        st.info("No tasks yet. Add some!")

    st.divider()

    # Clear completed tasks
    if st.button("🧹 Clear Completed Tasks"):
        task_list = [task for task in task_list if not task[1]]
        save_tasks(task_list)
        st.experimental_rerun()

    # Clear all tasks
    if st.button("🚮 Clear All Tasks"):
        task_list.clear()
        save_tasks(task_list)
        st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    main()
