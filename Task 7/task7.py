import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from task4 import convolution 
from task5 import DFT,IDFT



def Compare_Signals(file_name,Your_indices,Your_samples):      
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Test case failed, your signal have different values from the expected one") 
            return
    print("Test case passed successfully")
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
            values.append(float(parts[1]))
    return indices,values



def window_Detection(StopBandAttenuation):
    if(StopBandAttenuation <= 21):
        return "Rectangular"
    
    elif(StopBandAttenuation <= 44):
        return "Hanning"
    
    elif(StopBandAttenuation <= 53):
        return "Hamming"
    
    else:
        return "Blackman"


def compute_N(window,transitionBand,fs):
    
    normalized_transitionBand= transitionBand/fs

    if(window=="Rectangular"):
        N= 0.9/ normalized_transitionBand

    elif(window=="Hanning"):
        N= 3.1/ normalized_transitionBand
    
    elif(window=="Hamming"):
        N = 3.3/ normalized_transitionBand
    
    elif(window=="Blackman"):
        N = 5.5 / normalized_transitionBand
    
    N = math.ceil(N)

    if(N % 2==0):
        N=N+1
    
    return N


def comute_fc_dash(filter,fs,transitionBand,fc1_ideal,fc2_ideal=0):

    fc1_dash=0
    fc2_dash=0

    if(filter=="Low pass"):
        fc1_dash = ( fc1_ideal+(transitionBand/2) ) / fs
    
    if(filter=="High pass"):
        fc1_dash = ( fc1_ideal-(transitionBand/2) ) /fs

    if(filter=="Band pass"):
        fc1_dash = (fc1_ideal-(transitionBand/2) ) /fs
        fc2_dash = (fc2_ideal+(transitionBand/2) ) /fs

    if(filter=="Band stop"):
        fc1_dash = ( fc1_ideal+(transitionBand/2) )/fs
        fc2_dash = ( fc2_ideal-(transitionBand/2) )/fs

    return fc1_dash,fc2_dash



def compute_filter(filter,N,fc1_dash,fc2_dash):
    
    indicies_range = math.floor(N/2)
    pi=np.pi
    values=[]
    

    if(filter=="Low pass"):

        values.append(2*fc1_dash)
        for n in range (1,indicies_range+1):
            res=(2 * fc1_dash * math.sin(n * 2 * pi * fc1_dash)) / (n * 2 * pi * fc1_dash)
            values.append(res)
    

    elif(filter=="High pass"):

        values.append( 1-(2*fc1_dash) )
        for n in range (1,indicies_range+1):
            res=(-2 * fc1_dash * math.sin(n * 2 * pi * fc1_dash)) / (n * 2 * pi * fc1_dash)
            values.append(res)
    
    elif(filter=="Band pass"):

        values.append( 2*(fc2_dash-fc1_dash) )
        for n in range (1,indicies_range+1):
            res=( (2 * fc2_dash * math.sin(n * 2 * pi * fc2_dash)) / (n * 2 * pi * fc2_dash) ) - ( (2 * fc1_dash * math.sin(n * 2 * pi * fc1_dash)) / (n * 2 * pi * fc1_dash) ) 
            values.append(res)

    elif(filter=="Band stop"):
        values.append( 1 - 2* (fc2_dash-fc1_dash) ) 
        for n in range (1,indicies_range+1):
            res= ( (2 * fc1_dash * math.sin(n * 2 * pi * fc1_dash)) / (n * 2 * pi * fc1_dash) ) - ( (2 * fc2_dash * math.sin(n * 2 * pi * fc2_dash)) / (n * 2 * pi * fc2_dash) )
            values.append(res)

    return values





def compute_window(window,N):
    
    indicies_range = math.floor(N/2)
    pi=np.pi
    values=[]

    if(window=="Rectangular"):
        for n in range(0,indicies_range+1):
            values.append(1)
    
    elif(window=="Hanning"):
        for n in range(0,indicies_range+1):
            res= 0.5+(0.5 * math.cos( (2*pi*n)/N ))
            values.append(res)
    
    elif(window=="Hamming"):
        for n in range(0,indicies_range+1):
            res= 0.54+(0.46 * math.cos( (2*pi*n)/N ))
            values.append(res)
    
    elif(window=="Blackman"):
        for n in range(0,indicies_range+1):
            res= 0.42+(0.5 * math.cos( (2*pi*n)/(N-1) )) + (0.08 * math.cos( (4*pi*n)/(N-1) ))
            values.append(res)
    
    return values




def compute_designed_filter(filter,window,N,fc1_dash,fc2_dash=0):

    indicies_range = math.floor(N/2)
    filter_values=compute_filter(filter,N,fc1_dash,fc2_dash)
    window_values=compute_window(window,N)

    indicies=[]
    values=[]
    d={}

    desinged_filter= (np.array(filter_values) * np.array(window_values)).tolist()

    for n in range(-indicies_range, indicies_range + 1):
        d[n] = desinged_filter[abs(n)]

    indicies= list(d.keys())
    values= list(d.values())

    return indicies,values


def draw_filter(act_indices,act_values,exp_indices,exp_values):
        
        col1, col2,col3 = st.columns(3) 
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 3)) 
            ax1.plot(act_indices, act_values, marker='o', color='blue')
            ax1.set_title("Actual Filter", fontsize=10)
            ax1.set_xlabel("n")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True) 
        
        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3)) 
            ax2.plot(exp_indices, exp_values, marker='o', color='green')
            ax2.set_title("Expected Filter", fontsize=10)
            ax2.set_xlabel("n")
            ax2.set_ylabel("Amplitude")
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)
        
        with col3:
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            error= error = np.round(np.array(exp_values) - np.array(act_values))
            ax3.plot(exp_indices, error, marker='o', color='red')
            ax3.set_title(f"Error", fontsize=10)
            ax3.set_xlabel("n")
            ax3.set_ylabel("Error")
            ax3.grid(True)
            st.pyplot(fig3, use_container_width=True)


def draw_signal(act_indices,act_values,exp_indices,exp_values):
        
        col1, col2,col3 = st.columns(3) 
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 3)) 
            ax1.plot(act_indices, act_values, marker='o', color='blue')
            ax1.set_title("Actual Signal", fontsize=10)
            ax1.set_xlabel("n")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)
            st.pyplot(fig1, use_container_width=True) 
        
        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3)) 
            ax2.plot(exp_indices, exp_values, marker='o', color='green')
            ax2.set_title("Expected Signal", fontsize=10)
            ax2.set_xlabel("n")
            ax2.set_ylabel("Amplitude")
            ax2.grid(True)
            st.pyplot(fig2, use_container_width=True)
        
        with col3:
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            error= error = np.round(np.array(exp_values) - np.array(act_values))
            ax3.plot(exp_indices, error, marker='o', color='red')
            ax3.set_title(f"Error", fontsize=10)
            ax3.set_xlabel("n")
            ax3.set_ylabel("Error")
            ax3.grid(True)
            st.pyplot(fig3, use_container_width=True)


def fast_convolution(signal_values, filter_values):
    N1 = len(signal_values)
    N2 = len(filter_values)
    N = N1 + N2 - 1
    
    x_padded = np.pad(signal_values, (0, N - N1), 'constant')
    h_padded = np.pad(filter_values, (0, N - N2), 'constant')
    
    X = DFT(x_padded)
    H = DFT(h_padded)
    Y = X * H
    
    y_time = IDFT(Y)
    
    return np.real(y_time).tolist()


def display_task7():
    
    st.subheader("User Input")

    file = st.selectbox(
    "Select file",
    ["Task 7\Practical Task\FIR test cases\Testcase 2\ecg400.txt"] )

    filter = st.selectbox(
    "Select filter type",
    ["Low pass", "High pass", "Band pass", "Band stop"] )

    fs = st.number_input("Sampling Frequency (Hz)", min_value=1.0, value=8000.0)
    StopBandAttenuation = st.number_input("Stop Band Attenuation (dB)", min_value=0.0, value=50.0)
    transitionBand = st.number_input("Transition Band (Hz)", min_value=1.0, value=500.0)

    if filter in ["Low pass", "High pass"]:
        fc1 = st.number_input("Cutoff Frequency Fc (Hz)", min_value=1.0, value=1000.0)
        fc2 = 0
    else:
        fc1 = st.number_input("Lower Cutoff Frequency Fc1 (Hz)", min_value=1.0, value=1000.0)
        fc2 = st.number_input("Upper Cutoff Frequency Fc2 (Hz)", min_value=1.0, value=2000.0)
    
    window = window_Detection (StopBandAttenuation)
    N = compute_N (window,transitionBand,fs)
    fc1_dash,fc2_dash= comute_fc_dash(filter,fs,transitionBand,fc1,fc2)

    filter_indices,filter_values = compute_designed_filter(filter,window,N,fc1_dash,fc2_dash)

    signal_indices,signal_values=read_signal(file)

    filtered_signal_ind,filtered_signal_val=convolution(signal_indices,signal_values,filter_indices,filter_values)

    if st.button("Generate Filtered Signal"):

        fig, ax = plt.subplots(figsize=(4, 3)) 
        ax.plot(filtered_signal_ind, filtered_signal_val, marker='o', color='blue')
        ax.set_title("Filtered Signal", fontsize=10)
        ax.set_xlabel("n")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
        st.pyplot(fig, use_container_width=True) 

        save_path="Task 7\Practical Task\Test.txt"
        with open(save_path, "w") as f:
            for i, v in zip(filter_indices, filter_values):
                f.write(f"{i} {v}\n")


    st.subheader("Low Pass Filter")

    if st.button("Test Case 1"):
        
        filter="Low pass"
        fs= 8000
        StopBandAttenuation = 50
        fc_ideal = 1500
        transitionBand = 500

        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc_dash,_= comute_fc_dash(filter,fs,transitionBand,fc_ideal)

        act_indices,act_values = compute_designed_filter(filter,window,N,fc_dash)

        path="Task 7\Practical Task\FIR test cases\Testcase 1\LPFCoefficients.txt"
        exp_indices,exp_values=read_signal(path)

        draw_filter(act_indices,act_values,exp_indices,exp_values)

        if(Compare_Signals(path,act_indices,act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")
    

    if st.button("Test Case 2 (Convolution)"):
        
        filter="Low pass"
        fs= 8000
        StopBandAttenuation = 50
        fc_ideal = 1500
        transitionBand = 500
        
        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc_dash,_= comute_fc_dash(filter,fs,transitionBand,fc_ideal)

        filter_indices,filter_values = compute_designed_filter(filter,window,N,fc_dash)

        path1="Task 7\Practical Task\FIR test cases\Testcase 2\ecg400.txt"
        signal_indices,signal_values= read_signal(path1)

        path2="Task 7\Practical Task\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt"
        exp_indices,exp_values=read_signal(path2)

        act_indices,act_values = convolution(signal_indices,signal_values,filter_indices,filter_values)

        draw_signal(act_indices,act_values,exp_indices,exp_values)

        if(Compare_Signals(path2,act_indices,act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")
    

    if st.button("Test Case 2 (Fourier)"):

        filter="Low pass"
        fs= 8000
        StopBandAttenuation = 50
        fc_ideal = 1500
        transitionBand = 500
        
        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc_dash,_= comute_fc_dash(filter,fs,transitionBand,fc_ideal)

        filter_indices,filter_values = compute_designed_filter(filter,window,N,fc_dash)
        
        path1="Task 7\Practical Task\FIR test cases\Testcase 2\ecg400.txt"
        path2="Task 7\Practical Task\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt"
        
        signal_indices, signal_values = read_signal(path1)
        exp_indices, exp_values = read_signal(path2)

        act_values = fast_convolution(signal_values, filter_values)
        act_indices = list(range(len(act_values)))

        draw_signal(act_indices, act_values, exp_indices, exp_values)

        if(Compare_Signals(path2, act_indices, act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")



    st.subheader("High Pass Filter")
    if st.button("Test Case 3"):
        
        filter="High pass"
        fs= 8000
        StopBandAttenuation = 70
        fc_ideal = 1500
        transitionBand = 500

        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc_dash,_= comute_fc_dash(filter,fs,transitionBand,fc_ideal)


        act_indices,act_values = compute_designed_filter(filter,window,N,fc_dash)

        path="Task 7\Practical Task\FIR test cases\Testcase 3\HPFCoefficients.txt"
        exp_indices,exp_values=read_signal(path)

        draw_filter(act_indices,act_values,exp_indices,exp_values)

        if(Compare_Signals(path,act_indices,act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")


    if st.button("Test Case 4 (Convolution)"):
        
        filter="High pass"
        fs= 8000
        StopBandAttenuation = 70
        fc_ideal = 1500
        transitionBand = 500

        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc_dash,_= comute_fc_dash(filter,fs,transitionBand,fc_ideal)


        filter_indices,filter_values = compute_designed_filter(filter,window,N,fc_dash)

        path1="Task 7\Practical Task\FIR test cases\Testcase 4\ecg400.txt"
        signal_indices,signal_values= read_signal(path1)

        path2="Task 7\Practical Task\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt"
        exp_indices,exp_values=read_signal(path2)

        act_indices,act_values = convolution(signal_indices,signal_values,filter_indices,filter_values)

        draw_signal(act_indices,act_values,exp_indices,exp_values)

        if(Compare_Signals(path2,act_indices,act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")


    if st.button("Test Case 4 (Fourier)"):
        
        filter="High pass"
        fs= 8000
        StopBandAttenuation = 70
        fc_ideal = 1500
        transitionBand = 500

        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc_dash,_= comute_fc_dash(filter,fs,transitionBand,fc_ideal)


        filter_indices,filter_values = compute_designed_filter(filter,window,N,fc_dash)
        
        path1="Task 7\Practical Task\FIR test cases\Testcase 4\ecg400.txt"
        path2="Task 7\Practical Task\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt"
        
        signal_indices, signal_values = read_signal(path1)
        exp_indices, exp_values = read_signal(path2)

        act_values = fast_convolution(signal_values, filter_values)
        act_indices = list(range(len(act_values)))

        draw_signal(act_indices, act_values, exp_indices, exp_values)

        if(Compare_Signals(path2, act_indices, act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")



    st.subheader("Band Pass Filter")
    if st.button("Test Case 5"):
        
        filter="Band pass"
        fs= 1000
        StopBandAttenuation = 60
        fc1_ideal = 150
        fc2_ideal = 250
        transitionBand = 50

        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc1_dash,fc2_dash = comute_fc_dash(filter,fs,transitionBand,fc1_ideal,fc2_ideal)

        act_indices,act_values=compute_designed_filter(filter,window,N,fc1_dash,fc2_dash)

        path="Task 7\Practical Task\FIR test cases\Testcase 5\BPFCoefficients.txt"
        exp_indices,exp_values=read_signal(path)

        draw_filter(act_indices,act_values,exp_indices,exp_values)

        if(Compare_Signals(path,act_indices,act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")


    if st.button("Test Case 6 (Convolution)"):

        filter="Band pass"
        fs= 1000
        StopBandAttenuation = 60
        fc1_ideal = 150
        fc2_ideal = 250
        transitionBand = 50

        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc1_dash,fc2_dash = comute_fc_dash(filter,fs,transitionBand,fc1_ideal,fc2_ideal)

        filter_indices,filter_values = compute_designed_filter(filter,window,N,fc1_dash,fc2_dash)

        path1="Task 7\Practical Task\FIR test cases\Testcase 6\ecg400.txt"
        signal_indices,signal_values= read_signal(path1)

        path2="Task 7\Practical Task\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt"
        exp_indices,exp_values=read_signal(path2)

        act_indices,act_values = convolution(signal_indices,signal_values,filter_indices,filter_values)

        draw_signal(act_indices,act_values,exp_indices,exp_values)

        if(Compare_Signals(path2,act_indices,act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")
    

    if st.button("Test Case 6 (Fourier)"):

        filter="Band pass"
        fs= 1000
        StopBandAttenuation = 60
        fc1_ideal = 150
        fc2_ideal = 250
        transitionBand = 50

        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc1_dash,fc2_dash = comute_fc_dash(filter,fs,transitionBand,fc1_ideal,fc2_ideal)

        filter_indices,filter_values = compute_designed_filter(filter,window,N,fc1_dash,fc2_dash)
        
        path1="Task 7\Practical Task\FIR test cases\Testcase 6\ecg400.txt"
        path2="Task 7\Practical Task\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt"
        
        signal_indices, signal_values = read_signal(path1)
        exp_indices, exp_values = read_signal(path2)

        act_values = fast_convolution(signal_values, filter_values)
        act_indices = list(range(len(act_values)))

        draw_signal(act_indices, act_values, exp_indices, exp_values)

        if(Compare_Signals(path2, act_indices, act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")




    st.subheader("Band Stop Filter")
    if st.button("Test Case 7"):

        filter="Band stop"
        fs= 1000
        StopBandAttenuation = 60
        fc1_ideal = 150
        fc2_ideal = 250
        transitionBand = 50
        
        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc1_dash,fc2_dash = comute_fc_dash(filter,fs,transitionBand,fc1_ideal,fc2_ideal)

        act_indices,act_values=compute_designed_filter(filter,window,N,fc1_dash,fc2_dash)

        path="Task 7\Practical Task\FIR test cases\Testcase 7\BSFCoefficients.txt"
        exp_indices,exp_values=read_signal(path)

        draw_filter(act_indices,act_values,exp_indices,exp_values)

        if(Compare_Signals(path,act_indices,act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")


    if st.button("Test Case 8 (Convolution)"):

        filter="Band stop"
        fs= 1000
        StopBandAttenuation = 60
        fc1_ideal = 150
        fc2_ideal = 250
        transitionBand = 50
        
        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc1_dash,fc2_dash = comute_fc_dash(filter,fs,transitionBand,fc1_ideal,fc2_ideal)

        filter_indices,filter_values = compute_designed_filter(filter,window,N,fc1_dash,fc2_dash)

        path1="Task 7\Practical Task\FIR test cases\Testcase 8\ecg400.txt"
        path2="Task 7\Practical Task\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt"
        signal_indices,signal_values= read_signal(path1)

        
        exp_indices,exp_values=read_signal(path2)

        act_indices,act_values = convolution(signal_indices,signal_values,filter_indices,filter_values)

        draw_signal(act_indices,act_values,exp_indices,exp_values)

        if(Compare_Signals(path2,act_indices,act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")
    

    if st.button("Test Case 8 (Fourier)"):

        filter="Band stop"
        fs= 1000
        StopBandAttenuation = 60
        fc1_ideal = 150
        fc2_ideal = 250
        transitionBand = 50
        
        window= window_Detection (StopBandAttenuation)
        N=compute_N (window,transitionBand,fs)
        fc1_dash,fc2_dash = comute_fc_dash(filter,fs,transitionBand,fc1_ideal,fc2_ideal)

        filter_indices,filter_values = compute_designed_filter(filter,window,N,fc1_dash,fc2_dash)
        
        path1="Task 7\Practical Task\FIR test cases\Testcase 8\ecg400.txt"
        path2="Task 7\Practical Task\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt"
        
        signal_indices, signal_values = read_signal(path1)
        exp_indices, exp_values = read_signal(path2)

        act_values = fast_convolution(signal_values, filter_values)
        act_indices = list(range(len(act_values)))

        draw_signal(act_indices, act_values, exp_indices, exp_values)

        if(Compare_Signals(path2, act_indices, act_values)):
            st.write("Test case passed successfully")
        else:
            st.write("Test case failed")