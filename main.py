# task_manager.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

# Initialize session state
if 'task_lists' not in st.session_state:
    st.session_state.task_lists = {}

# Function to add a new task to a specific list
def add_task(list_name, task_name, priority):
    task = {
        'Task': task_name,
        'Priority': priority,
        'Added': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Completed': False
    }
    st.session_state.task_lists[list_name].append(task)

# Function to complete a task in a specific list
def complete_task(list_name, task_index):
    st.session_state.task_lists[list_name][task_index]['Completed'] = True

# Function to delete a task in a specific list
def delete_task(list_name, task_index):
    st.session_state.task_lists[list_name].pop(task_index)

# Function for Pomodoro timer
def pomodoro_timer(minutes):
    end_time = datetime.now() + timedelta(minutes=minutes)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        st.write(f"Time remaining: {remaining_time}")
        time.sleep(1)
        st.experimental_rerun()

# Streamlit App Layout
def home_page():
    st.title("Task and Time Management Tool")
    st.header("Home Page")
    st.write("Welcome to the Task and Time Management Tool!")
    st.write("Use the navigation menu to create and manage your task lists, and track your tasks.")

def tasks_page():
    st.header("Tasks Management")

    # Create a new task list
    st.subheader("Type in current date")
    with st.form(key='create_task_list_form'):
        list_name = st.text_input("Date")
        create_button = st.form_submit_button("Enter")
        if create_button and list_name:
            st.session_state.task_lists[list_name] = []
            st.success(f"List '{list_name}' created!")
    
    # Select task list
    if st.session_state.task_lists:
        st.subheader("Manage List")
        list_name = st.selectbox("Select Date", list(st.session_state.task_lists.keys()))
        
        if list_name:
            # Add a new task
            with st.form(key='add_task_form'):
                task_name = st.text_input("Task Name")
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                add_task_button = st.form_submit_button("Add Task")
                if add_task_button and task_name:
                    add_task(list_name, task_name, priority)
                    st.success(f"Task '{task_name}' added to list '{list_name}'")
            
            # Display current tasks
            if st.session_state.task_lists[list_name]:
                st.subheader("Current Tasks")
                task_df = pd.DataFrame(st.session_state.task_lists[list_name])
                st.table(task_df)

                # Mark tasks as completed
                for i, task in enumerate(st.session_state.task_lists[list_name]):
                    if not task['Completed']:
                        if st.button(f"Complete Task {i+1}", key=f"complete_{list_name}_{i}"):
                            complete_task(list_name, i)

                # Delete tasks
                for i, task in enumerate(st.session_state.task_lists[list_name]):
                    if st.button(f"Delete Task {i+1}", key=f"delete_{list_name}_{i}"):
                        delete_task(list_name, i)
            else:
                st.write("No tasks added yet.")
    else:
        st.write("No task lists available. Please create a new task list.")

def timer_page():
    st.header("Pomodoro Timer")
    pomodoro_minutes = st.number_input("Pomodoro Duration (minutes)", min_value=1, max_value=60, value=25)
    if st.button("Start Pomodoro"):
        pomodoro_timer(pomodoro_minutes)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Tasks", "Timer"])

if page == "Home":
    home_page()
elif page == "Tasks":
    tasks_page()
elif page == "Timer":
    timer_page()