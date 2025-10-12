import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def display_task2():
    st.subheader("Signal Generation")
    
    col1, col2 = st.columns(2)
    with col1:
        wave_type = st.radio("Wave Type:", ["Sine", "Cosine"])
    with col2:
        is_discrete = st.checkbox("Discrete Representation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Signal 1")
        A1 = st.number_input("A1", value=1.0)
        f1 = st.number_input("f1 (Hz)", value=1.0)
        theta1 = st.number_input("θ1 (rad)", value=0.0)
        fs1 = st.number_input("fs1 (Hz)", value=10.0)
    
    with col2:
        st.subheader("Signal 2")
        A2 = st.number_input("A2", value=1.0)
        f2 = st.number_input("f2 (Hz)", value=1.0)
        theta2 = st.number_input("θ2 (rad)", value=0.0)
        fs2 = st.number_input("fs2 (Hz)", value=10.0)
    
    if st.button("Generate Signals"):
        duration = 2.0
        selected_wave = 'sin' if wave_type == "Sine" else 'cos'
        
        if is_discrete:
            t1_gen = np.arange(0, duration, 1 / fs1)
            t2_gen = np.arange(0, duration, 1 / fs2)
        else:
            t1_gen = np.linspace(0, duration, 1000)
            t2_gen = t1_gen.copy()
        
        omega1 = 2 * np.pi * f1
        phase_term1 = omega1 * t1_gen + theta1
        if selected_wave == 'sin':
            signal1_gen = A1 * np.sin(phase_term1)
        else:
            signal1_gen = A1 * np.cos(phase_term1)
        
        omega2 = 2 * np.pi * f2
        phase_term2 = omega2 * t2_gen + theta2
        if selected_wave == 'sin':
            signal2_gen = A2 * np.sin(phase_term2)
        else:
            signal2_gen = A2 * np.cos(phase_term2)
        
        col1, col2 = st.columns(2)
        with col1:
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            if is_discrete:
                ax1.stem(t1_gen, signal1_gen, linefmt='b', markerfmt='bo', basefmt=' ')
            else:
                ax1.plot(t1_gen, signal1_gen, 'b-', linewidth=1)
            title1 = f"Generated {wave_type} Signal 1"
            ax1.set_title(title1, fontsize=14)
            ax1.set_xlabel("Index (n)", fontsize=12)
            ax1.set_ylabel("Amplitude", fontsize=12)
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True)
        
        with col2:
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            if is_discrete:
                ax2.stem(t2_gen, signal2_gen, linefmt='r', markerfmt='ro', basefmt=' ')
            else:
                ax2.plot(t2_gen, signal2_gen, 'r-', linewidth=1)
            title2 = f"Generated {wave_type} Signal 2"
            ax2.set_title(title2, fontsize=14)
            ax2.set_xlabel("Index (n)", fontsize=12)
            ax2.set_ylabel("Amplitude", fontsize=12)
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)