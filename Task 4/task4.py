import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def read_signal_from_file(filename):
    indices = []
    values = []
    with open(filename, "r") as f:
        lines = f.readlines()
        if len(lines) < 3:
            raise ValueError("File too short")
        N = int(lines[2].strip())
        for line in lines[3:3+N]:
            idx_str, val_str = line.strip().split()
            indices.append(int(idx_str))
            values.append(float(val_str))
    return indices, values

def moving_average(signal, window_size):
    avg_indices=[]
    avg_signal = []

    N = len(signal)
    for n in range(N - window_size + 1):
        window = signal[n:n+window_size]
        avg_signal.append(sum(window)/window_size)
        avg_indices.append(n)

    return avg_indices,avg_signal


def first_derivative(signal):
    indices=[]
    first_dervative_signal=[]
    N= len(signal)
    for n in range(1,len(signal)):
        first_dervative_signal.append(signal[n]-signal[n-1])
        indices.append(n-1)
    
    return indices,first_dervative_signal


def second_derivative(signal):
    indices=[]
    second_dervative_signal=[]
    N= len(signal)
    for n in range(1,len(signal)-1):
        second_dervative_signal.append(signal[n+1]-2*signal[n]+signal[n-1])
        indices.append(n-1)

    return indices,second_dervative_signal


def convolution(indcies1,signal1,indcies2,signal2):

    indices=[]
    signal=[]

    d1 = dict(zip(indcies1, signal1))
    d2 = dict(zip(indcies2, signal2))
    y_start = min(d1.keys()) + min(d2.keys())
    y_end = max(d1.keys()) + max(d2.keys())

    for n in range(y_start,y_end+1):

        value=0
        for k in range ( min(d1.keys()),max(d1.keys())+1 ):
            value+=d1[k]*d2.get(n-k,0)

        signal.append(value)
        indices.append(n)

    return indices,signal





def display_task4(indices=None, values=None):
    st.subheader("Filters and convolution")

    file = r"Task 4/testcases/Moving Average testcases/MovingAvg_input.txt"
    derv_input_file= r"Task 4/testcases/Derivative testcases/Derivative_input.txt"
    indices, values = read_signal_from_file(file)
    derv_indices,derv_values=read_signal_from_file(derv_input_file)


    window_size = st.number_input("Enter window size:", min_value=1, value=3, step=1)
    
    if st.button("Generate Moving Average"):
        avg_indices,avg_signal = moving_average(values,window_size)

        st.subheader("Moving Average Result")

        col1, col2 = st.columns(2) 
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 3)) 
            ax1.plot(indices, values, marker='o', color='blue')
            ax1.set_title("Original Signal", fontsize=10)
            ax1.set_xlabel("n")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True) 

        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3)) 
            avg_indices, avg_signal = moving_average(values, window_size)
            ax2.plot(avg_indices, avg_signal, marker='o', color='green')
            ax2.set_title(f"Moving Average (M={window_size})", fontsize=10)
            ax2.set_xlabel("n")
            ax2.set_ylabel("Amplitude")
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)

    st.subheader("Test Cases")

    if st.button("Run Averaging Test Case 1"):
        test1_file= r"Task 4/testcases/Moving Average testcases/MovingAvg_out1.txt"
        actual_indices,actual_signal= moving_average(values,3)
        expected_indices,expected_signal= read_signal_from_file(test1_file)

        col1, col2,col3= st.columns(3) 
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 3)) 
            ax1.plot(actual_indices, actual_signal, marker='o', color='blue')
            ax1.set_title("Actual Signal", fontsize=10)
            ax1.set_xlabel("n")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True) 

        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3)) 
            ax2.plot(expected_indices, expected_signal, marker='o', color='green')
            ax2.set_title(f"Expected Signal", fontsize=10)
            ax2.set_xlabel("n")
            ax2.set_ylabel("Amplitude")
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)
        
        with col3:
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            error= error = np.round(np.array(expected_signal) - np.array(actual_signal), 3)
            ax3.plot(expected_indices, error, marker='o', color='red')
            ax3.set_title(f"Error", fontsize=10)
            ax3.set_xlabel("n")
            ax3.set_ylabel("Error")
            ax3.grid(True)
            st.pyplot(fig3, use_container_width=True)
    
    if st.button("Run Averaging Test Case 2"):
        test2_file= r"Task 4/testcases/Moving Average testcases/MovingAvg_out2.txt"
        actual_indices,actual_signal= moving_average(values,5)
        expected_indices,expected_signal= read_signal_from_file(test2_file)
        
        col1, col2,col3 = st.columns(3) 
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 3)) 
            ax1.plot(actual_indices, actual_signal, marker='o', color='blue')
            ax1.set_title("Actual Signal", fontsize=10)
            ax1.set_xlabel("n")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True) 

        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3)) 
            ax2.plot(expected_indices, expected_signal, marker='o', color='green')
            ax2.set_title(f"Expected Signal", fontsize=10)
            ax2.set_xlabel("n")
            ax2.set_ylabel("Amplitude")
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)

        with col3:
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            error= error = np.round(np.array(expected_signal) - np.array(actual_signal), 3)
            ax3.plot(expected_indices, error, marker='o', color='red')
            ax3.set_title(f"Error", fontsize=10)
            ax3.set_xlabel("n")
            ax3.set_ylabel("Error")
            ax3.grid(True)
            st.pyplot(fig3, use_container_width=True)

    if st.button("Run First Dervative Test case"):
        first_derv_output= r"Task 4/testcases/Derivative testcases/1st_derivative_out.txt"

        act_first_derv_indices,act_first_derv_values=first_derivative(derv_values)
        exp_first_derv_indices,exp_first_derv_values=read_signal_from_file(first_derv_output)

        col1, col2,col3 = st.columns(3) 

        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 3)) 
            ax1.plot(act_first_derv_indices, act_first_derv_values, marker='o', color='blue')
            ax1.set_title("Actual Signal", fontsize=10)
            ax1.set_xlabel("n")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True) 

        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3)) 
            ax2.plot(exp_first_derv_indices, exp_first_derv_values, marker='o', color='green')
            ax2.set_title(f"Expected Signal", fontsize=10)
            ax2.set_xlabel("n")
            ax2.set_ylabel("Amplitude")
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)
        
        with col3:
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            error= error = np.round(np.array(exp_first_derv_values) - np.array(act_first_derv_values), 3)
            ax3.plot(exp_first_derv_indices, error, marker='o', color='red')
            ax3.set_title(f"Error", fontsize=10)
            ax3.set_xlabel("n")
            ax3.set_ylabel("Error")
            ax3.grid(True)
            st.pyplot(fig3, use_container_width=True)
    

    if st.button("Run Second Dervative Test case"):
        second_derv_output= r"Task 4/testcases/Derivative testcases/2nd_derivative_out.txt"
        act_second_derv_indices,act_second_derv_values=second_derivative(derv_values)
        exp_second_derv_indices,exp_second_derv_values=read_signal_from_file(second_derv_output)

        col1, col2,col3= st.columns(3) 
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 3)) 
            ax1.plot(act_second_derv_indices, act_second_derv_values, marker='o', color='blue')
            ax1.set_title("Actual Signal", fontsize=10)
            ax1.set_xlabel("n")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True) 
        
        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3)) 
            ax2.plot(exp_second_derv_indices, exp_second_derv_values, marker='o', color='green')
            ax2.set_title(f"Expected Signal", fontsize=10)
            ax2.set_xlabel("n")
            ax2.set_ylabel("Amplitude")
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)
        
        with col3:
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            error= error = np.round(np.array(exp_second_derv_values) - np.array(act_second_derv_values), 3)
            ax3.plot(exp_second_derv_indices, error, marker='o', color='red')
            ax3.set_title(f"Error", fontsize=10)
            ax3.set_xlabel("n")
            ax3.set_ylabel("Error")
            ax3.grid(True)
            st.pyplot(fig3, use_container_width=True)

    if st.button("Run Convolution Test case"):
        input1_conv=r"Task 4/testcases/Convolution testcases/Signal 1.txt"
        input2_conv=r"Task 4/testcases/Convolution testcases/Signal 2.txt"
        out_conv=r"Task 4/testcases/Convolution testcases/Conv_output.txt"

        indices1,values1=read_signal_from_file(input1_conv)
        indices2,values2=read_signal_from_file(input2_conv)

        act_indices_conv, act_signal_conv =convolution(indices1,values1,indices2,values2)
        exp_indices_conv, exp_signal_conv =read_signal_from_file(out_conv)

        col1, col2,col3= st.columns(3) 
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 3)) 
            ax1.plot(act_indices_conv, act_signal_conv, marker='o', color='blue')
            ax1.set_title("Actual Signal", fontsize=10)
            ax1.set_xlabel("n")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True) 

        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3)) 
            ax2.plot(exp_indices_conv, exp_signal_conv, marker='o', color='green')
            ax2.set_title(f"Expected Signal", fontsize=10)
            ax2.set_xlabel("n")
            ax2.set_ylabel("Amplitude")
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)

        with col3:
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            error= error = np.round(np.array(exp_signal_conv) - np.array(act_signal_conv), 3)
            ax3.plot(exp_indices_conv, error, marker='o', color='red')
            ax3.set_title(f"Error", fontsize=10)
            ax3.set_xlabel("n")
            ax3.set_ylabel("Error")
            ax3.grid(True)
            st.pyplot(fig3, use_container_width=True)