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

def read_expected_output_test2(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    expected_interval = []
    expected_encoded = []
    expected_quantized = []
    expected_error = []
    for line in lines[3:]:
        parts = line.strip().split()
        if len(parts) == 4:
            expected_interval.append(int(parts[0]))
            expected_encoded.append(parts[1])
            expected_quantized.append(float(parts[2]))
            expected_error.append(float(parts[3]))
    return expected_interval, expected_encoded, expected_quantized, expected_error

def quantize_signal(signal, num_levels):
    signal = np.array(signal)
    xmin = np.min(signal)
    xmax = np.max(signal)
    R = xmax - xmin
    if R == 0 or num_levels <= 1:
        return signal.copy(), np.zeros_like(signal), 0, np.zeros_like(signal, dtype=int)
    delta = R / num_levels
    offset = delta / 2.0
    k = (signal - xmin - offset) / delta
    q = np.round(k).astype(int)
    q = np.clip(q, 0, num_levels - 1)
    quantized = xmin + offset + q * delta
    error = signal - quantized
    return quantized, error, delta, q

def get_encoded(q, num_bits):
    return [format(int(qi), f'0{num_bits}b') for qi in q]

def display_task3(t1, signal1, QuantizationTest1, QuantizationTest2):
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
    quantized_signal, error_signal, delta, q = quantize_signal(orig_signal, num_levels)
        
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
    
    if 'show_test1' not in st.session_state:
        st.session_state.show_test1 = False
    if 'show_test2' not in st.session_state:
        st.session_state.show_test2 = False
    
    # test bits=3 using input signal
    if st.button("Run Test case 1"):
        st.session_state.show_test1 = not st.session_state.show_test1
    
    if st.session_state.show_test1:
        if QuantizationTest1 is None:
            st.error("Test function not available.")
        else:
            input_file = r"Task 3\Test\Test_1\Quan1_input.txt"
            expected_file = r"Task 3\Test\Test_1\Quan1_Out.txt"
            
            try:
                signal_test = read_test_input(input_file)
            except Exception as e:
                st.error(f"Error reading input file: {e}")
                st.stop()
            
            t_test = list(range(len(signal_test)))
            
            num_levels_test = 8
            num_bits_test = 3
            quantized_test, error_test, delta_test, q_test = quantize_signal(signal_test, num_levels_test)
            encoded_test = get_encoded(q_test, num_bits_test)
            
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

    if st.button("Run Test case 2"):
        st.session_state.show_test2 = not st.session_state.show_test2
    
    if st.session_state.show_test2:
        if QuantizationTest2 is None:
            st.error("Test function not available.")
        else:
            input_file = r"Task 3\Test\Test_2\Quan2_input.txt"
            expected_file = r"Task 3\Test\Test_2\Quan2_Out.txt"
            
            try:
                signal_test = read_test_input(input_file)
            except Exception as e:
                st.error(f"Error reading input file: {e}")
                st.stop()
            
            t_test = list(range(len(signal_test)))
            
            num_levels_test = 4
            num_bits_test = 2
            quantized_test, error_plot, delta_test, q_test = quantize_signal(signal_test, num_levels_test)
            interval_indices = (q_test + 1).tolist()
            encoded_test = get_encoded(q_test, num_bits_test)
            error_test_for_test = (quantized_test - signal_test).tolist()
            
            expected_interval, expected_encoded, expected_quantized, expected_error = read_expected_output_test2(expected_file)
            
            if QuantizationTest2:
                f_capture = io.StringIO()
                with redirect_stdout(f_capture):
                    QuantizationTest2(expected_file, interval_indices, encoded_test, quantized_test.tolist(), error_test_for_test)
                output = f_capture.getvalue()
                st.write("**Test Result:**")
                st.write(output)
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                fig_t1, ax_t1 = plt.subplots(figsize=(6, 4))
                ax_t1.plot(t_test, signal_test, 'b', label='Original')
                ax_t1.plot(t_test, quantized_test, 'g-', linewidth=2, label='Quantized')
                ax_t1.set_title("TestCase 2: Original vs Quantized", fontsize=12)
                ax_t1.set_xlabel("Time (s)")
                ax_t1.set_ylabel("Amplitude")
                ax_t1.legend()
                ax_t1.grid(True)
                st.pyplot(fig_t1, use_container_width=True)
            
            with col_t2:
                fig_t2, ax_t2 = plt.subplots(figsize=(6, 4))
                ax_t2.plot(t_test, error_plot, 'm-', linewidth=2)
                ax_t2.set_title("TestCase 2: Quantization Error", fontsize=12)
                ax_t2.set_xlabel("Time (s)")
                ax_t2.set_ylabel("Error")
                ax_t2.grid(True)
                st.pyplot(fig_t2, use_container_width=True)
            
            st.write("Our Interval Indices:", interval_indices)
            st.write("Our Encoded:", encoded_test)
            st.write("Our Quantized (rounded):", [round(v, 3) for v in quantized_test.tolist()])
            st.write("Our Error (quant - orig):", [round(v, 3) for v in error_test_for_test])
            st.write("Expected Interval:", expected_interval)
            st.write("Expected Encoded:", expected_encoded)
            st.write("Expected Quantized:", [round(v, 3) for v in expected_quantized])
            st.write("Expected Error:", [round(v, 3) for v in expected_error])