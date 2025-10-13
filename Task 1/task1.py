import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
from contextlib import redirect_stdout

from test_functions import AddSignalSamplesAreEqual, SubSignalSamplesAreEqual, MultiplySignalByConst, ShiftSignalByConst, Folding

def read_expected(filename):
    indices = []
    values = []
    with open(filename, "r") as f:
        f.readline()  # 0
        f.readline()  # 0
        n_line = f.readline().strip()  # N
        N = int(n_line)
        for _ in range(N):
            line = f.readline().strip()
            if line:
                idx_str, val_str = line.split()
                indices.append(float(idx_str))
                values.append(float(val_str))
    return indices, values

def display_task1(t1, signal1, t2, signal2):
    st.subheader("Operations on Loaded Signals")
    operation = st.selectbox(
        "Select Operation",
        ["Original", "Amplify", "Delay Right", "Fold", "Add", "Subtract"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.plot(t1, signal1, 'b')
        ax1.set_title("Original Signal 1", fontsize=12)
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Amplitude")
        ax1.grid(True)
        st.pyplot(fig1, use_container_width=True)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.plot(t2, signal2, 'r')
        ax2.set_title("Original Signal 2", fontsize=12)
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Amplitude")
        ax2.grid(True)
        st.pyplot(fig2, use_container_width=True)
        
    with col3:
        fig3, ax3 = plt.subplots(figsize=(6, 4))

        if operation == "Original":
            ax3.plot(t1, signal1, 'g')
            ax3.set_title("Signal 1 (Original)", fontsize=12)

        elif operation == "Amplify":
            factor = st.number_input("Amplification Factor", value=1.0)
            amp_signal = np.array(signal1) * factor
            ax3.plot(t1, amp_signal, 'g')
            ax3.set_title(f"Amplified (x{factor})", fontsize=12)

        elif operation == "Delay Right":
            shift = st.number_input("Shift Amount", value=1, step=1)
            shifted_t = np.array(t1) + shift
            ax3.plot(shifted_t, signal1, 'g')
            ax3.set_title(f"Shifted Right by {shift}", fontsize=12)

        elif operation == "Fold":
            t_reversed = np.array(t1[::-1]) * -1
            signal_reversed = np.array(signal1[::-1])
            ax3.plot(t_reversed, signal_reversed, 'g')
            ax3.set_title("Folded Signal", fontsize=12)

        elif operation == "Add":
            all_indices = sorted(set(t1) | set(t2))
            d1 = dict(zip(t1, signal1))
            d2 = dict(zip(t2, signal2))
            summed = [d1.get(i, 0) + d2.get(i, 0) for i in all_indices]
            ax3.plot(all_indices, summed, 'g')
            ax3.set_title("Signal 1 + Signal 2", fontsize=12)

        elif operation == "Subtract":
            all_indices = sorted(set(t1) | set(t2))
            d1 = dict(zip(t1, signal1))
            d2 = dict(zip(t2, signal2))
            subtracted = [d1.get(i, 0) - d2.get(i, 0) for i in all_indices]
            ax3.plot(all_indices, subtracted, 'g')
            ax3.set_title("Signal 1 - Signal 2", fontsize=12)

        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Amplitude")
        ax3.grid(True)
        st.pyplot(fig3, use_container_width=True)

    st.subheader("Test Cases")

    if st.button("Run Add Test"):
        all_indices = sorted(set(t1) | set(t2))
        d1 = dict(zip(t1, signal1))
        d2 = dict(zip(t2, signal2))
        your_samples = [d1.get(i, 0) + d2.get(i, 0) for i in all_indices]
        your_indices = all_indices
        f_capture = io.StringIO()
        with redirect_stdout(f_capture):
            AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", your_indices, your_samples)
        output = f_capture.getvalue()
        st.write("**Test Result:**")
        st.write(output)

        expected_file = "Task 1/Test/add.txt"
        expected_indices, expected_samples = read_expected(expected_file)

        col_y, col_e, col_err = st.columns(3)
        with col_y:
            fig_y, ax_y = plt.subplots(figsize=(6, 4))
            ax_y.plot(your_indices, your_samples, 'g')
            ax_y.set_title("Your Result", fontsize=12)
            ax_y.set_xlabel("Time (s)")
            ax_y.set_ylabel("Amplitude")
            ax_y.grid(True)
            st.pyplot(fig_y, use_container_width=True)
        with col_e:
            fig_e, ax_e = plt.subplots(figsize=(6, 4))
            ax_e.plot(expected_indices, expected_samples, 'r')
            ax_e.set_title("Expected Result", fontsize=12)
            ax_e.set_xlabel("Time (s)")
            ax_e.set_ylabel("Amplitude")
            ax_e.grid(True)
            st.pyplot(fig_e, use_container_width=True)
        with col_err:
            error_samples = [ys - es for ys, es in zip(your_samples, expected_samples)]
            fig_err, ax_err = plt.subplots(figsize=(6, 4))
            ax_err.plot(your_indices, error_samples, 'm')
            ax_err.set_title("Error (Your - Expected)", fontsize=12)
            ax_err.set_xlabel("Time (s)")
            ax_err.set_ylabel("Error")
            ax_err.grid(True)
            st.pyplot(fig_err, use_container_width=True)

    if st.button("Run Subtract Test"):
        all_indices = sorted(set(t1) | set(t2))
        d1 = dict(zip(t1, signal1))
        d2 = dict(zip(t2, signal2))
        your_samples = [d1.get(i, 0) - d2.get(i, 0) for i in all_indices]
        your_indices = all_indices
        f_capture = io.StringIO()
        with redirect_stdout(f_capture):
            SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", your_indices, your_samples)
        output = f_capture.getvalue()
        st.write("**Test Result:**")
        st.write(output)

        expected_file = "Task 1/Test/subtract.txt"
        expected_indices, expected_samples = read_expected(expected_file)

        col_y, col_e, col_err = st.columns(3)
        with col_y:
            fig_y, ax_y = plt.subplots(figsize=(6, 4))
            ax_y.plot(your_indices, your_samples, 'g')
            ax_y.set_title("Your Result", fontsize=12)
            ax_y.set_xlabel("Time (s)")
            ax_y.set_ylabel("Amplitude")
            ax_y.grid(True)
            st.pyplot(fig_y, use_container_width=True)
        with col_e:
            fig_e, ax_e = plt.subplots(figsize=(6, 4))
            ax_e.plot(expected_indices, expected_samples, 'r')
            ax_e.set_title("Expected Result", fontsize=12)
            ax_e.set_xlabel("Time (s)")
            ax_e.set_ylabel("Amplitude")
            ax_e.grid(True)
            st.pyplot(fig_e, use_container_width=True)
        with col_err:
            error_samples = [ys - es for ys, es in zip(your_samples, expected_samples)]
            fig_err, ax_err = plt.subplots(figsize=(6, 4))
            ax_err.plot(your_indices, error_samples, 'm')
            ax_err.set_title("Error (Your - Expected)", fontsize=12)
            ax_err.set_xlabel("Time (s)")
            ax_err.set_ylabel("Error")
            ax_err.grid(True)
            st.pyplot(fig_err, use_container_width=True)

    if st.button("Run Multiply by 5 Test"):
        const = 5.0
        your_indices = t1
        your_samples = [v * const for v in signal1]
        f_capture = io.StringIO()
        with redirect_stdout(f_capture):
            MultiplySignalByConst(const, your_indices, your_samples)
        output = f_capture.getvalue()
        st.write("**Test Result:**")
        st.write(output)

        expected_file = "Task 1/Test/mul5.txt"
        expected_indices, expected_samples = read_expected(expected_file)

        col_y, col_e, col_err = st.columns(3)
        with col_y:
            fig_y, ax_y = plt.subplots(figsize=(6, 4))
            ax_y.plot(your_indices, your_samples, 'g')
            ax_y.set_title("Your Result", fontsize=12)
            ax_y.set_xlabel("Time (s)")
            ax_y.set_ylabel("Amplitude")
            ax_y.grid(True)
            st.pyplot(fig_y, use_container_width=True)
        with col_e:
            fig_e, ax_e = plt.subplots(figsize=(6, 4))
            ax_e.plot(expected_indices, expected_samples, 'r')
            ax_e.set_title("Expected Result", fontsize=12)
            ax_e.set_xlabel("Time (s)")
            ax_e.set_ylabel("Amplitude")
            ax_e.grid(True)
            st.pyplot(fig_e, use_container_width=True)
        with col_err:
            error_samples = [ys - es for ys, es in zip(your_samples, expected_samples)]
            fig_err, ax_err = plt.subplots(figsize=(6, 4))
            ax_err.plot(your_indices, error_samples, 'm')
            ax_err.set_title("Error (Your - Expected)", fontsize=12)
            ax_err.set_xlabel("Time (s)")
            ax_err.set_ylabel("Error")
            ax_err.grid(True)
            st.pyplot(fig_err, use_container_width=True)

    if st.button("Run Delay Right by 3 Test"):
        shift = 3
        your_indices = [ti + shift for ti in t1]
        your_samples = signal1[:]
        f_capture = io.StringIO()
        with redirect_stdout(f_capture):
            ShiftSignalByConst(-shift, your_indices, your_samples)
        output = f_capture.getvalue()
        st.write("**Test Result:**")
        st.write(output)

        expected_file = "Task 1/Test/delay3.txt"
        expected_indices, expected_samples = read_expected(expected_file)

        col_y, col_e, col_err = st.columns(3)
        with col_y:
            fig_y, ax_y = plt.subplots(figsize=(6, 4))
            ax_y.plot(your_indices, your_samples, 'g')
            ax_y.set_title("Your Result", fontsize=12)
            ax_y.set_xlabel("Time (s)")
            ax_y.set_ylabel("Amplitude")
            ax_y.grid(True)
            st.pyplot(fig_y, use_container_width=True)
        with col_e:
            fig_e, ax_e = plt.subplots(figsize=(6, 4))
            ax_e.plot(expected_indices, expected_samples, 'r')
            ax_e.set_title("Expected Result", fontsize=12)
            ax_e.set_xlabel("Time (s)")
            ax_e.set_ylabel("Amplitude")
            ax_e.grid(True)
            st.pyplot(fig_e, use_container_width=True)
        with col_err:
            error_samples = [ys - es for ys, es in zip(your_samples, expected_samples)]
            fig_err, ax_err = plt.subplots(figsize=(6, 4))
            ax_err.plot(your_indices, error_samples, 'm')
            ax_err.set_title("Error (Your - Expected)", fontsize=12)
            ax_err.set_xlabel("Time (s)")
            ax_err.set_ylabel("Error")
            ax_err.grid(True)
            st.pyplot(fig_err, use_container_width=True)

    if st.button("Run Advance Left by 3 Test"):
        shift = 3
        your_indices = [ti - shift for ti in t1]
        your_samples = signal1[:]
        f_capture = io.StringIO()
        with redirect_stdout(f_capture):
            ShiftSignalByConst(shift, your_indices, your_samples)
        output = f_capture.getvalue()
        st.write("**Test Result:**")
        st.write(output)

        expected_file = "Task 1/Test/advance3.txt"
        expected_indices, expected_samples = read_expected(expected_file)

        col_y, col_e, col_err = st.columns(3)
        with col_y:
            fig_y, ax_y = plt.subplots(figsize=(6, 4))
            ax_y.plot(your_indices, your_samples, 'g')
            ax_y.set_title("Your Result", fontsize=12)
            ax_y.set_xlabel("Time (s)")
            ax_y.set_ylabel("Amplitude")
            ax_y.grid(True)
            st.pyplot(fig_y, use_container_width=True)
        with col_e:
            fig_e, ax_e = plt.subplots(figsize=(6, 4))
            ax_e.plot(expected_indices, expected_samples, 'r')
            ax_e.set_title("Expected Result", fontsize=12)
            ax_e.set_xlabel("Time (s)")
            ax_e.set_ylabel("Amplitude")
            ax_e.grid(True)
            st.pyplot(fig_e, use_container_width=True)
        with col_err:
            error_samples = [ys - es for ys, es in zip(your_samples, expected_samples)]
            fig_err, ax_err = plt.subplots(figsize=(6, 4))
            ax_err.plot(your_indices, error_samples, 'm')
            ax_err.set_title("Error (Your - Expected)", fontsize=12)
            ax_err.set_xlabel("Time (s)")
            ax_err.set_ylabel("Error")
            ax_err.grid(True)
            st.pyplot(fig_err, use_container_width=True)

    if st.button("Run Folding Test"):
        t_array = np.array(t1)
        sig_array = np.array(signal1)
        your_indices = list(t_array[::-1] * -1)
        your_samples = list(sig_array[::-1])
        f_capture = io.StringIO()
        with redirect_stdout(f_capture):
            Folding(your_indices, your_samples)
        output = f_capture.getvalue()
        st.write("**Test Result:**")
        st.write(output)

        expected_file = "Task 1/Test/folding.txt"
        expected_indices, expected_samples = read_expected(expected_file)

        col_y, col_e, col_err = st.columns(3)
        with col_y:
            fig_y, ax_y = plt.subplots(figsize=(6, 4))
            ax_y.plot(your_indices, your_samples, 'g')
            ax_y.set_title("Your Result", fontsize=12)
            ax_y.set_xlabel("Time (s)")
            ax_y.set_ylabel("Amplitude")
            ax_y.grid(True)
            st.pyplot(fig_y, use_container_width=True)
        with col_e:
            fig_e, ax_e = plt.subplots(figsize=(6, 4))
            ax_e.plot(expected_indices, expected_samples, 'r')
            ax_e.set_title("Expected Result", fontsize=12)
            ax_e.set_xlabel("Time (s)")
            ax_e.set_ylabel("Amplitude")
            ax_e.grid(True)
            st.pyplot(fig_e, use_container_width=True)
        with col_err:
            error_samples = [ys - es for ys, es in zip(your_samples, expected_samples)]
            fig_err, ax_err = plt.subplots(figsize=(6, 4))
            ax_err.plot(your_indices, error_samples, 'm')
            ax_err.set_title("Error (Your - Expected)", fontsize=12)
            ax_err.set_xlabel("Time (s)")
            ax_err.set_ylabel("Error")
            ax_err.grid(True)
            st.pyplot(fig_err, use_container_width=True)