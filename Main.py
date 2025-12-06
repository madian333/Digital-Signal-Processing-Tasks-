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

from task1 import display_task1
from task2 import display_task2
from task3 import display_task3
from task4 import display_task4
from task5 import display_task5
from task6 import display_task6


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

st.title("Signal Processing GUI")

t1, signal1 = read_signal_from_file(r"Signals\Signal1.txt")
t2, signal2 = read_signal_from_file(r"Signals\Signal2.txt")

tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs([
    "Task 1: Loaded Signals Operations",
    "Task 2: Generate Signals",
    "Task 3: Quantization",
    "Task 4: Filters and Convolution",
    "Task 5: DFT & IDFT",
    "Task 6: Correlation and Time Analysis"
])
st.set_page_config(layout="wide")

with tab1:
    display_task1(t1, signal1, t2, signal2)

with tab2:
    display_task2()

with tab3:
    display_task3(t1, signal1, QuantizationTest1, QuantizationTest2)

with tab4:
    display_task4()

with tab5:
    display_task5()

with tab6:
    display_task6()