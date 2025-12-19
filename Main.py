import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import io
from contextlib import redirect_stdout

sys.path.append("Task 1")
sys.path.append("Task 1/Test")
sys.path.append("Task 2")
sys.path.append("Task 3")
sys.path.append("Task 3/Test/Test_1")
sys.path.append("Task 3/Test/Test_2")
sys.path.append("Task 4")
sys.path.append("Task 5")
sys.path.append("Task 5/Test Cases")
sys.path.append("Task 6")
sys.path.append("Task 7")

from task1 import display_task1
from task2 import display_task2
from task3 import display_task3
from task4 import display_task4
from task5 import display_task5
from task6 import display_task6
from task7 import display_task7

try:
    from QuanTest1 import QuantizationTest1
except ImportError:
    st.error("Could not import QuantizationTest1. Ensure the file exists at Task 3/Test/QuanTest1.py")
    QuantizationTest1 = None

try:
    from QuanTest2 import QuantizationTest2
except ImportError:
    st.error("Could not import QuantizationTest2. Ensure the file exists at Task 3/Test/Test_2/QuanTest2.py")
    QuantizationTest2 = None

st.set_page_config(page_title="Digital Signal Processing Tasks GUI", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if 'page' in st.query_params:
    st.session_state['current_page'] = st.query_params['page']
    del st.query_params['page']
    st.rerun()

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

def read_signal_from_file(filename):
    indices = []
    values = []
    with open(filename, "r") as f:
        lines = f.readlines()
        lines = lines[2:]
        N = int(lines[0].strip())
        for line in lines[1:1 + N]:
            idx, val = map(int, line.strip().split())
            indices.append(idx)
            values.append(val)
    return indices, values

t1, signal1 = read_signal_from_file(r"Signals\Signal1.txt")
t2, signal2 = read_signal_from_file(r"Signals\Signal2.txt")

tasks = [
    {"id": "task1", "number": "1", "name": "Signal Operations", "color": "blue"},
    {"id": "task2", "number": "2", "name": "Generate Signals", "color": "purple"},
    {"id": "task3", "number": "3", "name": "Quantization", "color": "orange"},
    {"id": "task4", "number": "4", "name": "Filters & Convolution", "color": "green"},
    {"id": "task5", "number": "5", "name": "DFT & IDFT", "color": "pink"},
    {"id": "task6", "number": "6", "name": "Correlation & Time Analysis", "color": "yellow"},
    {"id": "task7", "number": "7", "name": "(Practical Task) FIR Filter Design", "color": "red"}
]

if st.session_state['current_page'] == 'home':
    st.markdown("<h1 class='main-title'>Digital Signal Processing Tasks GUI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Select a task to begin signal processing</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='task-grid'>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, task in enumerate(tasks):
        with cols[idx % 3]:
            st.markdown(f"""
                <a href="?page={task['id']}" target="_self" style="text-decoration: none; display: block;">
                    <div class='task-box-wrapper'>
                        <div class='task-box task-{task["color"]}'>
                            <div class='task-number'>Task {task["number"]}</div>
                            <div class='task-name'>{task["name"]}</div>
                        </div>
                    </div>
                </a>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

else:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("Home", use_container_width=True):
            st.session_state['current_page'] = 'home'
            st.rerun()
    
    with col2:
        current_task = next((t for t in tasks if t['id'] == st.session_state['current_page']), None)
        if current_task:
            st.markdown(f"<h2 class='task-header'>Task {current_task['number']}: {current_task['name']}</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state['current_page'] == 'task1':
        display_task1(t1, signal1, t2, signal2)
    elif st.session_state['current_page'] == 'task2':
        display_task2()
    elif st.session_state['current_page'] == 'task3':
        display_task3(t1, signal1, QuantizationTest1, QuantizationTest2)
    elif st.session_state['current_page'] == 'task4':
        display_task4()
    elif st.session_state['current_page'] == 'task5':
        display_task5()
    elif st.session_state['current_page'] == 'task6':
        display_task6()
    elif st.session_state['current_page'] == 'task7':
        display_task7()