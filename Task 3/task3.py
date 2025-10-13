import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
from contextlib import redirect_stdout

def read_test_input(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    N = int(lines[2].strip())
    values = []
    for line in lines[3:3 + N]:
        parts = line.strip().split()
        if len(parts) == 2:
            values.append(float(parts[1]))
    return np.array(values)

def read_expected_output(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        #skip first 3 lines
    expected_encoded = []
    expected_quantized = []
    for line in lines[3:]:
        parts = line.strip().split()
        if len(parts) == 2:
            expected_encoded.append(parts[0])
            expected_quantized.append(float(parts[1]))
    return expected_encoded, expected_quantized

def display_task3(t1, signal1, QuantizationTest1):
    st.subheader("Signal Quantization")
    
    specify_by = st.radio("Specify by:", ["Levels", "Bits"])
    num_levels = 0
    num_bits = 0
    if specify_by == "Levels":
        num_levels_input = st.number_input("Number of Levels", min_value=2, max_value=256, value=4, step=1)
        num_levels = int(num_levels_input)
        num_bits = int(np.ceil(np.log2(num_levels)))
    else:
        num_bits = st.number_input("Number of Bits", min_value=1, max_value=8, value=2, step=1)
        num_levels = 2 ** num_bits
    
    orig_signal = np.array(signal1)
    xmin = np.min(orig_signal)
    xmax = np.max(orig_signal)
    R = xmax - xmin
    
    if R == 0 or num_levels <= 1:
        quantized_signal = orig_signal.copy()
        error_signal = np.zeros_like(orig_signal)
        delta = 0
        q = np.zeros_like(orig_signal, dtype=int)
    else:
        delta = R / num_levels
        offset = delta / 2.0
        k = (orig_signal - xmin - offset) / delta
        q = np.round(k)
        q = np.clip(q, 0, num_levels - 1).astype(int)
        quantized_signal = xmin + offset + q * delta
        error_signal = orig_signal - quantized_signal
        
    st.text(f"Levels used: {num_levels}, Bits: {num_bits}, Step size (Δ): {delta:.4f}")
    
        # use signal1 as input
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_orig, ax_orig = plt.subplots(figsize=(6, 4))
        ax_orig.plot(t1, signal1, 'b')
        ax_orig.set_title("Original Signal 1", fontsize=12)
        ax_orig.set_xlabel("Time (s)")
        ax_orig.set_ylabel("Amplitude")
        ax_orig.grid(True)
        st.pyplot(fig_orig, use_container_width=True)
    
    with col2:
        fig_quant, ax_quant = plt.subplots(figsize=(6, 4))
        ax_quant.plot(t1, quantized_signal, 'g-', linewidth=2)
        ax_quant.set_title(f"Quantized Signal ({num_levels} levels)", fontsize=12)
        ax_quant.set_xlabel("Time (s)")
        ax_quant.set_ylabel("Amplitude")
        ax_quant.grid(True)
        st.pyplot(fig_quant, use_container_width=True)
    
    with col3:
        fig_error, ax_error = plt.subplots(figsize=(6, 4))
        ax_error.plot(t1, error_signal, 'm-', linewidth=2)
        ax_error.set_title("Quantization Error", fontsize=12)
        ax_error.set_xlabel("Time (s)")
        ax_error.set_ylabel("Error Amplitude")
        ax_error.grid(True)
        st.pyplot(fig_error, use_container_width=True)
    
    st.subheader("Test Cases")
    
    # test bits=3 using input signal
    if st.button("Run testcase"):
        if QuantizationTest1 is None:
            st.error("Test function not available.")
        else:
            input_file = r"Task 3\Test\Quan1_input.txt"
            expected_file = r"Task 3\Test\Quan1_Out.txt"
            
            try:
                signal_test = read_test_input(input_file)
            except Exception as e:
                st.error(f"Error reading input file: {e}")
                st.stop()
            
            t_test = list(range(len(signal_test)))
            
            xmin_test = np.min(signal_test)
            xmax_test = np.max(signal_test)
            R_test = xmax_test - xmin_test
            num_levels_test = 8
            num_bits_test = 3
            delta_test = R_test / num_levels_test
            offset_test = delta_test / 2.0
            k_test = (signal_test - xmin_test - offset_test) / delta_test
            q_test = np.round(k_test)
            q_test = np.clip(q_test, 0, num_levels_test - 1).astype(int)
            quantized_test = xmin_test + offset_test + q_test * delta_test
            encoded_test = [format(int(qi), f'0{num_bits_test}b') for qi in q_test]
            error_test = signal_test - quantized_test
            
            expected_encoded, expected_quantized = read_expected_output(expected_file)
            
            if QuantizationTest1:
                your_encoded = encoded_test
                your_quantized = quantized_test.tolist()
                f_capture = io.StringIO()
                with redirect_stdout(f_capture):
                    QuantizationTest1(expected_file, your_encoded, your_quantized)
                output = f_capture.getvalue()
                st.write("**Test Result:**")
                st.write(output)
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                fig_t1, ax_t1 = plt.subplots(figsize=(6, 4))
                ax_t1.plot(t_test, signal_test, 'b', label='Original')
                ax_t1.plot(t_test, quantized_test, 'g-', linewidth=2, label='Quantized')
                ax_t1.set_title("TestCase 1: Original vs Quantized", fontsize=12)
                ax_t1.set_xlabel("Time (s)")
                ax_t1.set_ylabel("Amplitude")
                ax_t1.legend()
                ax_t1.grid(True)
                st.pyplot(fig_t1, use_container_width=True)
            
            with col_t2:
                fig_t2, ax_t2 = plt.subplots(figsize=(6, 4))
                ax_t2.plot(t_test, error_test, 'm-', linewidth=2)
                ax_t2.set_title("TestCase 1: Quantization Error", fontsize=12)
                ax_t2.set_xlabel("Time (s)")
                ax_t2.set_ylabel("Error")
                ax_t2.grid(True)
                st.pyplot(fig_t2, use_container_width=True)
            
            st.write("Our Encoded:", encoded_test)
            st.write("Our Quantized (rounded):", [round(v, 2) for v in quantized_test.tolist()])
            st.write("Expected Encoded:", expected_encoded)
            st.write("Expected Quantized:", expected_quantized)