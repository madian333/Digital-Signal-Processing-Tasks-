import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def SignalComapreAmplitude(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalOutput):
        return False
    for i in range(len(SignalInput)):
        if abs(SignalInput[i] - SignalOutput[i]) > 0.001:
            return False
    return True

def SignalComaprePhaseShift(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalOutput):
        return False
    for i in range(len(SignalInput)):
        A = round(SignalInput[i])
        B = round(SignalOutput[i])
        if abs(A - B) > 0.0001:
            return False
    return True

def read_signal(filepath):
    indices = []
    values = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()[3:]
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            indices.append(int(parts[0]))
            val = parts[1].replace("f", "").replace("F", "")
            values.append(float(val))
    return np.array(indices), np.array(values)

def read_amplitude_phase(filepath):
    amps = []
    phases = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()[3:]
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            amp = parts[0].replace("f", "").replace("F", "")
            phase = parts[1].replace("f", "").replace("F", "")
            amps.append(float(amp))
            phases.append(float(phase))
    return np.array(amps), np.array(phases)

def DFT(x, inverse=False):
    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    sign = 1 if inverse else -1
    M = np.exp(sign * 2j * np.pi * k * n / N)
    result = np.dot(M, x)
    if inverse:
        result = result / N
    return np.real(result) if inverse else result

def IDFT(X):
    return DFT(X, inverse=True)

def wrap_to_pi(p):
    return (p + np.pi) % (2 * np.pi) - np.pi

def display_task5():
    st.subheader("Task 5: DFT & IDFT")

    choice = st.selectbox("Select Signal", ["Signal1.txt", "Signal2.txt", "Test Signal"])
    path = {"Signal1.txt": "Signals/Signal1.txt",
            "Signal2.txt": "Signals/Signal2.txt",
            "Test Signal": "Task 5/Test Cases/DFT/Input_Signal_DFT.txt"}[choice]

    indices, values = read_signal(path)
    fs = st.number_input("Sampling Frequency (Hz)", min_value=1, value=1000)

    if st.button("Compute DFT and Reconstruct"):
        X = DFT(values)
        amp = np.abs(X)
        phase = wrap_to_pi(np.angle(X))
        reconstructed = IDFT(X)
        freqs = np.fft.fftfreq(len(values), d=1/fs)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.stem(freqs[:len(values)//2], amp[:len(values)//2], basefmt=" ")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Amplitude")
            ax.set_title("Amplitude Spectrum")
            ax.grid(True)
            st.pyplot(fig)

            fig, ax = plt.subplots()
            ax.stem(freqs[:len(values)//2], phase[:len(values)//2], basefmt=" ")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Phase (rad)")
            ax.set_title("Phase Spectrum")
            ax.grid(True)
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.plot(indices, values, "bo-", label="Original")
            ax.plot(indices, reconstructed, "rx--", label="Reconstructed")
            ax.set_xlabel("Sample")
            ax.set_ylabel("Amplitude")
            ax.set_title("Original vs Reconstructed")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    st.markdown("---")
    st.subheader("Test Cases")

    if st.button("Run DFT Test Case"):
        input_file = "Task 5/Test Cases/DFT/Input_Signal_DFT.txt"
        ap_file = "Task 5/Test Cases/DFT/Output_Signal_DFT_A,Phase.txt"

        _, x = read_signal(input_file)
        exp_amp, exp_phase_raw = read_amplitude_phase(ap_file)
        exp_phase = wrap_to_pi(exp_phase_raw)

        X = DFT(x)
        comp_amp = np.abs(X)
        comp_phase = wrap_to_pi(np.angle(X))

        amp_ok = SignalComapreAmplitude(exp_amp.tolist(), comp_amp.tolist())
        phase_ok = SignalComaprePhaseShift(exp_phase.tolist(), comp_phase.tolist())

        st.write(f"**DFT Test: {'PASSED' if amp_ok and phase_ok else 'FAILED'}**")

        col1, col2, col3 = st.columns(3)
        with col1:
            fig, ax = plt.subplots()
            ax.stem(comp_amp, markerfmt="bo")
            ax.set_title("Your Amplitude")
            ax.grid(True)
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            ax.stem(exp_amp, markerfmt="go")
            ax.set_title("Expected Amplitude")
            ax.grid(True)
            st.pyplot(fig)
        with col3:
            err = np.round(exp_amp - comp_amp, 6)
            fig, ax = plt.subplots()
            ax.stem(err, markerfmt="ro")
            ax.set_title("Amplitude Error")
            ax.grid(True)
            st.pyplot(fig)

        col1, col2, col3 = st.columns(3)
        with col1:
            fig, ax = plt.subplots()
            ax.stem(comp_phase, markerfmt="bo")
            ax.set_title("Your Phase")
            ax.grid(True)
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            ax.stem(exp_phase, markerfmt="go")
            ax.set_title("Expected Phase")
            ax.grid(True)
            st.pyplot(fig)
        with col3:
            err = np.round(exp_phase - comp_phase, 6)
            fig, ax = plt.subplots()
            ax.stem(err, markerfmt="ro")
            ax.set_title("Phase Error")
            ax.grid(True)
            st.pyplot(fig)

        st.write(f"**DFT Test: {'PASSED' if amp_ok and phase_ok else 'FAILED'}**")

    if st.button("Run IDFT Test Case"):
        ap_file = "Task 5/Test Cases/IDFT/Input_Signal_IDFT_A,Phase.txt"
        orig_file = "Task 5/Test Cases/DFT/Input_Signal_DFT.txt"

        amp_in, phase_in_raw = read_amplitude_phase(ap_file)
        phase_in = wrap_to_pi(phase_in_raw)
        _, expected = read_signal(orig_file)

        X_complex = amp_in * np.exp(1j * phase_in)
        reconstructed = IDFT(X_complex)

        match = SignalComapreAmplitude(expected.tolist(), reconstructed.tolist())

        n_samples = len(expected)
        col1, col2, col3 = st.columns(3)
        with col1:
            fig, ax = plt.subplots()
            ax.plot(range(n_samples), reconstructed[:n_samples], "bo-", label="Your")
            ax.set_title("Your Reconstructed Signal")
            ax.grid(True)
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            ax.plot(range(n_samples), expected, "go-", label="Expected")
            ax.set_title("Expected Signal")
            ax.grid(True)
            st.pyplot(fig)
        with col3:
            err = np.round(expected - reconstructed[:n_samples], 6)
            fig, ax = plt.subplots()
            ax.plot(range(n_samples), err, "ro-")
            ax.set_title("Error")
            ax.grid(True)
            st.pyplot(fig)

        st.write(f"**IDFT Test: {'PASSED' if match else 'FAILED'}**")